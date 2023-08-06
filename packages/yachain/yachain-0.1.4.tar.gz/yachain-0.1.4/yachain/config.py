# -*- coding: utf-8 -*-
"""This module provides access to configuration files in YAML markup."""

import yaml
import re
from os import path


class NoDataError(Exception):
    """ No config data available """


class Config(object):
    """Config - handle configfiles in yaml markup.

    Absolute / Relative
    -------------------
    All attributes in the config ending with 'path' or 'file' in their
    name AND were specified with a relative path, will be altered
    automatically by prepending the prefix.

    This option allows using the same configfiles operating with or
    without a virtual environment.

    Example
    -------

    Say, we run our app in a virtual environment. Using the statement
    below the application knows when it runs in a virtual environment
    or not.

    In case we have real_prefix we run in a virtual env and the prefix
    is sys.prefix.

    >>> PREFIX = "/" if not hasattr(sys, 'real_prefix') else sys.prefix
    >>> CONFIG_FILE = os.path.join(PREFIX, "etc/app/app.cfg")

    If the config specifies:
        app:
          logfile: var/log/myapp.log   # relative, gets prefix
          database_path: var/app       # relative, gets prefix
          some_config: var/app/db.txt  # relative, gets no prefix
          database: /var/app/db.txt    # absolute, gets no prefix

    then under a virtual environment this will be prefixed automatically:

    >>> import yachain
    >>> c = yachain.Config(prefix=PREFIX)
    >>> c.load(CONFIG_FILE)
    >>> print(c["app::logfile"])
    /path/of/virtualenv/var/log/myapp.log
    >>> print(c["app::database"])
    /var/app/db.txt

    The same, but now with a prefix passed:

    >>> c2 = Config(prefix="/some/virtualenv")
    >>> c2.load(CONFIG_FILE)
    >>> print(c["app::logfile"])
    /some/virtualenv/var/log/myapp.log
    >>> print(c["app::database"])
    /var/app/db.txt

    The same, but now with a prefix and a tokenseparator:

    >>> c2 = Config(prefix="/some/virtualenv", tokenseparator=".")
    >>> c2.load(CONFIG_FILE)
    >>> print(c["app.logfile"])
    /some/virtualenv/var/log/myapp.log
    >>> print(c["app.database"])
    /var/app/db.txt

    If no data is available, a NoDataError will be raised.
    """

    def __init__(self, configdata=None, prefix=None, tokenseparator="::",
                 reflags=re.IGNORECASE, yamlLoader=yaml.SafeLoader):
        """Instantiate a Config instance.

        Parameters
        ----------
        prefix : string
            when specifying a prefix, relative paths will get this
            prepended.

        tokenseparator : string
            specify the way you want to separate token. This only affects
            the way you reference config items in your application.
            By default it is set to '::'.

        configdata : string
            instead of loading config data from a file it is possible
            to pass it as a string.


        If no data is available, a NoDataError will be raised
        """
        self.data = None
        self.prefix = prefix
        self.reflags = reflags
        self.tokenseparator = tokenseparator
        self._yamlLoader = yamlLoader
        if configdata:
            self.data = configdata

    def load(self, filename):
        """read configdata from file.

        Parameters
        ----------
        filename : string
            the name of the YAML formatted config file.

        """
        self.filename = filename
        with open(filename) as CFG:
            self.data = yaml.load(CFG.read(), Loader=self._yamlLoader)

        return self

    def __getitem__(self, k):
        """return a configuration item by key."""

        def _gv_(data, keywords):
            # recursively traverse the data structure untill the last key
            # if it is a file or path prepend the prefix if there is a prefix
            currentKey = keywords.pop(0)
            if keywords:
                return _gv_(data[currentKey], keywords)
            else:
                rv = data[currentKey]
                if self.prefix and re.match("^.*(file|path)$",
                                            currentKey, self.reflags):
                    if not data[currentKey].startswith('/'):
                        return path.join(self.prefix, data[currentKey])

                return rv

        if not self.data:
            raise NoDataError("")

        return _gv_(self.data, k.split(self.tokenseparator))
