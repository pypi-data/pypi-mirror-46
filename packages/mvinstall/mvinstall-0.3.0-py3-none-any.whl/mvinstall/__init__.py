"""
mvinstall - install data and packages from S3.
"""

# flake8: noqa - prevent "imported but unused" linting errors

from .s3install import S3Installer

mvinstaller = S3Installer("mvinstall")

__version__ = "0.3.0"
