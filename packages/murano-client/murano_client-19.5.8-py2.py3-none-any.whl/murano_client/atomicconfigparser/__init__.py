"""
A subclass of the Configuration file parser that support atomic updates.

That is, if a write to a configuration file on a POSIX compatible file system
and the write is interrupted (e.g. by a power failure), the file will either
have the original contents or the updated contents.  The file will not be
corrupted.
"""

import tempfile as _tempfile
import os as _os
import fnmatch as _fn
from sys import stderr
import logging
import six
from murano_client import logger
if six.PY2:
    import ConfigParser as _cfg
    from ConfigParser import NoOptionError, NoSectionError
elif six.PY3:
    import configparser as _cfg
    from configparser import NoOptionError, NoSectionError

LOG = logger.getLogger('atomicconfigparser')

class atomicconfigparser(_cfg.RawConfigParser):
    """
        The atomicconfigparser is for ensuring atomic writes to files
        when on jffs2 and ubifs filesystems.
    """
    def __init__(self, **kwargs):
        _cfg.RawConfigParser.__init__(self, **kwargs)
        # preserving the case sensitivity
        self.optionxform = str

    def write(self, filename):
        """Write an .ini-format representation of the configuration state atomically."""

        # The configuration state is written to a temporary file in the same
        # directory as filename.  That assures us that the files will be on the
        # same file system.  Once the state is succesively written, the
        # temporary file will be renamed to filename.

        # Get the path for the desired filename.  The temporary file will be
        # created in this location.
        path = _os.path.dirname(_os.path.abspath(filename))

        # Create a temp file in the directory that will not be deleted when
        # it's closed.
        with _tempfile.NamedTemporaryFile(
            'w',
            prefix='atomic-',
            suffix='-cfg',
            dir=path,
            delete=False) as tmpf:
            # Call base class write routine to create the file
            _cfg.RawConfigParser.write(self, tmpf)

            # Flush the data to the temporary file
            tmpf.flush()

            # Sync the file contents to disk
            _os.fsync(tmpf.fileno())

            # Save the name  so that we can rename the file later
            tempname = tmpf.name

        # Rename the file from its temporary name to the actual name.  This
        # action, on a POSIX system, is atomic.
        _os.rename(tempname, filename)

        # Open the directory containing the temporary file and sync it as well
        # to make sure the rename operation has made it to storage.
        dirfd = _os.open(path, _os.O_DIRECTORY)
        _os.fsync(dirfd)
        _os.close(dirfd)

        # Clean up any old temporary configuration files that may exist.  They
        # will match the filename pattern 'atomic-*-cfg'.  This can happen
        # if a write is interrupted by a power cycle.
        for _file in _os.listdir(path):
            if _fn.fnmatch(_file, 'atomic-*-cfg'):
                try:
                    _os.unlink(_file)
                except OSError as err:
                    stderr.write("atomicconfigparser: could not unlink {0}: {1}\n"
                                 .format(_file, err), stderr)
                    stderr.write("atomicconfigparser: does file exist? {}\n"
                                 .format(_os.path.exists(_file)))
                except Exception as err: # pylint: disable=W0703
                    print("atomicconfigparser: unknown error: {0}".format(err), stderr)

