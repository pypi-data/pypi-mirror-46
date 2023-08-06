from typing import *

import ftplib
from ftplib import FTP
from pathlib import Path

from .LoggingUtils import LoggingUtils


class FTPUtils:

    logger = LoggingUtils.get_logger("FTPUtils")

    @classmethod
    def delete_path(cls, ftp: FTP, path: Path) -> NoReturn:
        """
        Deletes a directory or file on the ftp server, recursively deleting all contents of the directory.
        :param ftp: the FTP instance.
        :requires: ftp connection already established
        :param path: the path to the directory or file to upload
        :requires: the path exists.
        """
        if path.is_file():
            ftp.delete(path.name)
        else:  # path.is_dir()
            ftp.cwd(path.name)
            for subpath in path.iterdir():  # TODO: this is wrong. do ls on ftp side
                cls.delete_path(ftp, subpath)
            # end for
            ftp.cwd("../")
            ftp.rmd(path.name)
        # end if
        return

    @classmethod
    def upload_path(cls, ftp: FTP, path: Path) -> NoReturn:
        """
        Uploads a directory or file to the ftp server, recursively uploading all contents of the directory.
        :param ftp: the FTP instance.
        :requires: ftp connection already established
        :param path: the path to the directory or file to upload
        :requires: the path exists.
        """
        if path.is_file():
            cls.upload_file(ftp, path)
        else:  # path.is_dir()
            # Delete if directory already exists on server
            try:
                ftp.mkd(path.name)
            except ftplib.error_perm as e:
                if e.args[0].startswith("550"):
                    cls.delete_path(ftp, path)
                    ftp.mkd(path.name)
                else:
                    raise e
                # end if
            # end try
            ftp.cwd(path.name)

            for subpath in path.iterdir():
                cls.upload_path(ftp, subpath)
            # end for

            ftp.cwd("..")
        # end if

    @classmethod
    def upload_file(cls, ftp: FTP, file: Path) -> NoReturn:
        """
        Uploads a single file to the ftp server in text format.
        Uses STOR command.
        :param ftp: the FTP instance.
        :requires: ftp connection already established
        :param file: the file to upload
        """
        if not file.is_file():  raise IOError(f"Has to be a file: {file}")

        try:
            with open(str(file), "rb") as fp:
                resp = ftp.storlines("STOR " + file.name, fp)
                if not resp.startswith("226 Transfer complete"):
                    cls.logger.error(f"Upload failed: {file}")
                    raise IOError(f"Upload failed: {file}")
                # end if
        except ftplib.all_errors as e:
            raise IOError(f"Upload failed: {file}") from e
        # end try
        return

