"""
The s3install module has the purpose of installing data and packages
from S3 (compatible) resources. In enables the following workflow:

- Run ``init()`` using a special token that resolves to a url to a config file.
  That config file contains credentials and is stored on the local file system.
- Run ``sync()`` to synchronize data and package files.
- Run ``upgrade()`` or ``install()`` to invoke pip.

The config file can have the following fields:

- host: The S3 (compatible) provbider, e.g. "s3.amazonaws.com".
- access_key: The access key id.
- secret_key: The secret part of the credentials.
- always_install: A list of packages to install by default when install/upgrade is used.
- config_location: The "bucketname/prefix" where "config.json" is located.
- package_locations: A dictionary that maps local directories to "bucketname/prefix".
- data_locations: A dictionary that maps local directories to "bucketname/prefix".

"""

import os
import sys
import time
import json
import base64
import hashlib
import shutil
import datetime
import subprocess
from urllib.request import urlopen
from distutils.version import LooseVersion as LV

import minio


def get_application_dir(name):
    return os.path.join(os.path.expanduser('~'), '.' + name)


def url2token(url):
    """ Turn a url into a (terminal-friendly) token.
    """
    # The part containing the sign contains terminal unfriendly chars, like "&".
    # Let's just base64-encode it to make sure the token is terminal-safe.
    url = url.split('//', 1)[-1]  # remove http:// part
    leftpart = url.split("/config.json")[0]  # The domain part
    rightpart = url.split('?', 1)[-1]  # The sign part
    rightpart = base64.encodebytes(rightpart.encode()).decode().replace("\n", "")
    return leftpart + "?" + rightpart


def token2url(token):
    """ Turn a token back into url.
    """
    if "?" not in token:
        raise RuntimeError("Invalid token provided: " + str(token))
    leftpart, rightpart = token.split('?', 1)
    try:
        rightpart = base64.decodebytes(rightpart.encode()).decode()
    except ValueError:
        raise RuntimeError("Invalid token provided: " + str(token))
    return "https://{}/config.json?{}".format(leftpart, rightpart)


class S3Installer:
    """ The S3Installer API.
    """

    def __init__(self, service):

        # Create appdatadir for this service
        self._appdatadir = get_application_dir(service)
        if not os.path.isdir(self._appdatadir):
            os.mkdir(self._appdatadir)

    def _get_config(self):
        """ Get config (containing credentials) from the local file system.
        """
        filename = os.path.join(self._appdatadir, 'config.json')
        if not os.path.isfile(filename):
            raise RuntimeError('No config found; you should probably initialize first.')

        with open(filename, 'rb') as f:
            return json.loads(f.read().decode())

    def init(self, token):
        """ Initialize and configure using a given token.
        """

        # The credentials are put in the user-specific bucket, in a
        # file called "config.json". This function downloads the file using
        # a presigned url (encoded as a token) and stores it locally.

        # Parse token and construct url
        url = token2url(token)

        # Try to download
        print("Downloading and installing credentials ... ", end='')
        try:
            with urlopen(url, timeout=5) as f:
                config_str = f.read().decode()
        except Exception as err:
            if '403' in str(err):
                raise RuntimeError("The token appears to be invalid (403)")
            raise  # pragma: no cover - e.g. no internet

        # Make sure that it can be deserialized and has most important keys
        config = json.loads(config_str)
        for key in ('access_key', 'secret_key', 'host'):
            if not config.get(key):  # pragma: no cover
                raise RuntimeError("Loaded config does not have key {}".format(key))

        # Write to local file system
        with open(os.path.join(self._appdatadir, 'config.json'), 'wb') as f:
            f.write(config_str.encode())

        print("done")
        print('You may want to sync and upgrade now.')

    def reinit(self):
        """ Re-initialize the configuration.
        """
        token = self.token()
        return self.init(token)

    def token(self):
        """ Get a token to initialize on another machine.
        The token is valid for 24 hours. Only share as appropriate.
        """

        config = self._get_config()
        s3 = minio.Minio(config['host'], config['access_key'], config['secret_key'], secure=True)

        bucketname, _, prefix = config["config_location"].strip('/').partition("/")
        prefix = prefix + '/' if prefix else ""

        exp = datetime.timedelta(days=1)
        url = s3.presigned_get_object(bucketname, prefix + "config.json", exp)
        return url2token(url)

    def sync(self, reset=False):
        """ Synchronize data and all the packages.
        """
        return self._sync(reset, False)

    def sync_latest(self, reset=False):
        """ Synchronize the data and the latest versions of the packages (faster).
        """
        return self._sync(reset, True)

    def _sync(self, reset, latest_only):

        config = self._get_config()
        s3 = minio.Minio(config['host'], config['access_key'], config['secret_key'], secure=True)
        all_dirs = set()
        uptodate = True

        for case in ('package_locations', 'data_locations'):

            for dname, remote in config.get(case, {}).items():

                all_dirs.add(dname)
                dirname = os.path.join(self._appdatadir, dname)
                if not os.path.isdir(dirname):
                    os.mkdir(dirname)
                print("Checking", dirname)

                bucketname, _, prefix = remote.strip('/').partition("/")
                prefix = prefix + '/' if prefix else ""

                # List local and remote files
                local_files = set(fname for fname in os.listdir(dirname))
                remote_files = set()
                etags = {}
                for ob in s3.list_objects(bucketname, None, True):
                    if ob.object_name.startswith(prefix):
                        fname = ob.object_name[len(prefix):]
                        remote_files.add(fname)
                        etags[fname] = ob.etag  # This is the MD5 hash

                # Filtering
                if case == "package_locations":
                    # Filter package files (ignore files placed by pip)
                    local_files = set(
                        fname for fname in local_files if fname.endswith((".whl", ".zip")))
                    remote_files = set(
                        fname for fname in remote_files if fname.endswith((".whl", ".zip")))
                if latest_only and case == "package_locations":
                    # Filter latest packages?
                    versions = {}
                    for fname in remote_files:
                        name, *_ = fname.split("-")
                        if name not in versions or LV(versions[name]) < LV(fname):
                            versions[name] = fname
                    remote_files = set(versions.values())
                    local_files = local_files & remote_files  # don't remove old

                # Determine what to remove and what to download
                to_remove = local_files - remote_files
                to_download = remote_files - local_files
                if reset:
                    to_remove = local_files
                    to_download = remote_files
                # Double-check data that we already have - it may have changed
                if case == "data_locations":
                    for fname in sorted(remote_files - to_download):
                        with open(os.path.join(dirname, fname), "rb") as f:
                            local_hash = hashlib.md5(f.read()).hexdigest()
                            if local_hash != etags[fname]:
                                to_download.add(fname)

                # Apply
                if to_remove or to_download:
                    uptodate = False
                # Remove packages/data that are not remote (anymore)
                for fname in sorted(to_remove):
                    print("  Removing", fname, "... ", end='')
                    try:
                        os.remove(os.path.join(dirname, fname))
                    except OSError:  # pragma: no cover - ok, will be removed another time
                        print("fail")
                    else:
                        print("done")
                # Download packages/data that are missing here
                # fget_object() does a good job at downloading to a temp file and replacing atomically when done.
                for fname in sorted(to_download):
                    print('  Downloading', fname, '... ', end='')
                    s3.fget_object(bucketname, prefix + fname, os.path.join(dirname, fname))
                    print('done')

        # Remove any "old dirs" that do not start with an underscore
        for dname in os.listdir(self._appdatadir):
            dirname = os.path.join(self._appdatadir, dname)
            if os.path.isdir(dirname) and dname not in all_dirs and not dname.startswith("_"):
                print("Removing directory", dname, "... ", end='')
                try:
                    shutil.rmtree(dirname)
                except Exception:  # pragma: no cover - ok, will be removed another time
                    print("fail")
                else:
                    print("done")

        # Touch a stub file for which we can check the mtime to see last sync
        with open(os.path.join(self._appdatadir, 'lastsync'), 'wb'):
            pass

        if uptodate:
            print("Package and data directories are up to date")

    def upgrade(self):
        """ Upgrade relevant packages (using pip).
        """
        self.install('--upgrade')

    def install(self, *args):
        """ Install specific versions of packages (as with pip).
        """

        config = self._get_config()

        # Show a warning if there was not a sync for a long time
        stubfile = os.path.join(self._appdatadir, 'lastsync')
        if not os.path.isfile(stubfile):
            print('Warning: it looks like there has not been a sync yet. Maybe sync first"?')
            time.sleep(1)
        elif os.path.getmtime(stubfile) < time.time() - 7 * 86400:  # 7 days
            print('Warning: the last sync was a while ago. Maybe sync first?')

        # Add packages to the list if not already present (in some form) in args
        always_install = [
            name for name in config.get("always_install", [])
            if not any(name in arg for arg in args)
        ]

        # Add location where pip can look for packages
        locations = []
        for location in config.get("package_locations", {}).keys():
            locations.extend(["--find-links", os.path.join(self._appdatadir, location)])

        print("Calling ~ pip install " + " ".join(always_install + list(args)))

        # Install
        cmd = [sys.executable, "-m", "pip", "install"] + locations + always_install + list(args)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            raise RuntimeError('Pip failed')
