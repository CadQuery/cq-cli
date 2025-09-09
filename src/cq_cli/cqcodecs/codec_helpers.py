from contextlib import contextmanager, redirect_stderr, redirect_stdout
from os import devnull
import tempfile
import shutil
import logging

@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    logging.info("STDOUT and STDERR are send to devnull.")
    with open(devnull, "w") as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


class temp_dir():
    def __init__(self):
        """
        A function to create temp codec files inside temporary directories, and
        enable multiple codec processing, preventing file writing racing conditions.
        Returns
        -------
        str, Temporary directory path.
        """
        self.path = tempfile.mkdtemp()
        logging.debug(f"temp_dir: {self.path}")
        
    def dlt(self):
        """
        Safe temp_dir deletion and path invalidation.
        Returns
        -------
        None.

        """
        if self.path:
            shutil.rmtree(self.path)
            self.path = None
            logging.debug("temp_dir.path: deleted")
            return True
        else:
            logging.error("temp_dir.path: does not exist.")
            return False