# -----------------------------------------------------------------
# zeus: log.py
#
# Define zeus logging tools
#
# Copyright (C) 2016-2018, Christophe Fauchard
# -----------------------------------------------------------------

"""
Submodule: log.file

wrap python standard logging module

Copyright (C) 2016-2018, Christophe Fauchard
"""

import os
import logging
import logging.handlers
import zeus


class Log():

    """
    wrapper for standard Python logger module

    if file_name is None, console print only
    if frequence is None and file_name is not None => 1MB size rotation

    number         : file retention (default 7)
    frequence      : 'S', 'M', 'H', 'D', 'W0'-'W6':
                     second, minute, hour, day, day of week (0=Monday)

    basic usage    : create a pool of 7 1MB log files

    log = zeus.log.Log(file_name="test.log")
    log.logger.debug("%s %s", "test", "debug message")
    log.logger.info("%s %s", "test", "info message")
    log.logger.warning("%s %s", "test", "warning message")
    log.logger.error("%s %s", "test", "error message")
    log.logger.critical("%s %s", "test", "critical message")
    """

    def __init__(self,
                 file_name=None,
                 number=7,
                 size=1024 * 1024,
                 frequence=None,
                 stdout='Yes',
                 level=logging.INFO,
                 stdout_level=logging.INFO
                 ):
        self.file_name = file_name
        if file_name is not None:
            self.dirname = zeus.file.Path(os.path.dirname(file_name))
        self.frequence = frequence
        self.number = number
        self.size = size
        self.stdout = stdout
        self.level = level
        self.stdout_level = stdout_level

        #
        # create the logger
        #
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        #
        # create formatter log
        #
        self.formatter = logging.Formatter(
            '%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')

        if self.file_name is not None:
            if frequence is None:

                #
                # create size based rotation log
                #
                self.file_handler = logging.handlers.RotatingFileHandler(
                    self.file_name,
                    'a',
                    self.size,
                    self.number)
                self.file_handler.setFormatter(self.formatter)
                self.logger.addHandler(self.file_handler)
                self.file_handler.setLevel(self.level)

            else:

                #
                # create date based rotation log
                #
                self.file_handler = logging.handlers.TimedRotatingFileHandler(
                    self.file_name,
                    when=self.frequence,
                    interval=1,
                    backupCount=self.number)
                self.file_handler.setFormatter(self.formatter)
                self.logger.addHandler(self.file_handler)
                self.file_handler.setLevel(self.level)

        #
        # create stdout handler
        #
        self.stream_handler = logging.StreamHandler()
        self.logger.addHandler(self.stream_handler)
        self.stream_handler.setLevel(self.stdout_level)

    #
    # log levels:
    #
    # logging.DEBUG
    # logging.INFO
    # logging.WARNING
    # logging.ERROR
    # logging.CRITICAL
    #
    def set_stdout_level(self, level):
        self.stdout_level = level
        self.stream_handler.setLevel(self.stdout_level)

    def set_level(self, level):
        self.level = level
        if self.file_name is not None:
            self.file_handler.setLevel(self.level)
        # self.stream_handler.setLevel(self.level)
