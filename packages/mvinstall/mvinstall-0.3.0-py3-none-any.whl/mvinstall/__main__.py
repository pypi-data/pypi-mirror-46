"""
CLI for mvinstall
"""

import sys
import argparse

from mvinstall import mvinstaller, __version__

description = """

Install Movandi packages and dependencies. When you have received an
initialization token, run the two following lines. The latter line can also
be run when you want to update your packages and data to the latest version:

    $ mvinstall --init the_given_token
    $ mvinstall --sync --upgrade
"""

epilog = """
"""


def getdoc(ob):
    return ob.__doc__.replace("    ", "").strip()


def main(argv=None):

    assert sys.version_info.major == 3, "This script needs to run with Python 3."

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="mvinstall", description=description, epilog=epilog,
                                     add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='store_true', help="Print version.")
    parser.add_argument('--init', metavar='token', action='store', help=getdoc(mvinstaller.init))
    parser.add_argument('--reinit', action='store_true', help=getdoc(mvinstaller.reinit))
    parser.add_argument('--token', action='store_true', help=getdoc(mvinstaller.token))
    parser.add_argument('--sync', action='count', help=getdoc(mvinstaller.sync))
    parser.add_argument('--sync-latest', action='count', help=getdoc(mvinstaller.sync_latest))
    parser.add_argument('--upgrade', action='store_true', help=getdoc(mvinstaller.upgrade))
    parser.add_argument('--install', metavar='arg', nargs='*', action='store',
                        help=getdoc(mvinstaller.install))

    if not argv or len(argv) == 1 and argv[0] in ('-h', '--help'):
        return parser.print_help()

    args = parser.parse_args(argv)

    try:

        if args.version:
            print("mvinstall v" + __version__)
        if args.init:
            print("=== Initializing with mvinstall v" + __version__)
            mvinstaller.init(args.init)
        if args.reinit:
            print("=== Re-initializing with mvinstall v" + __version__)
            mvinstaller.reinit()
        if args.token:
            print("=== Getting token with mvinstall v" + __version__)
            token = mvinstaller.token()
            doc = mvinstaller.token.__doc__.replace("Get ", "Here is ").replace("    ", "")
            print(doc.strip() + "\n\n" + token)
        if args.sync:
            print("=== Syncing with mvinstall v" + __version__)
            mvinstaller.sync(args.sync > 1)
        if args.sync_latest:
            print("=== Syncing latest with mvinstall v" + __version__)
            mvinstaller.sync_latest(args.sync_latest > 1)
        if args.upgrade:
            print("=== Upgrading with mvinstall v" + __version__)
            mvinstaller.upgrade()
        if args.install is not None:
            print("=== Installing with mvinstall v" + __version__)
            mvinstaller.install(*args.install)

    except RuntimeError as err:
        # In s3install, RunTimeError is raised in situations that can
        # sufficiently be described with the error message. Other
        # exceptions fall through, and their traceback is printed.
        sys.exit(str(err))


if __name__ == '__main__':
    main()
