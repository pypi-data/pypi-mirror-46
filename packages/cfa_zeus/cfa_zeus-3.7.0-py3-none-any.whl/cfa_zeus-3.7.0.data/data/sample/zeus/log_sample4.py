#!/usr/bin/env python3
# coding: utf8
#-----------------------------------------------------------------
# zeus: log_sample4.py
#
# log testing, set_stdout_level method test
#
# Copyright (C) 2016-2018, Christophe Fauchard
#-----------------------------------------------------------------

import sys
import logging
import zeus

print("zeus version %s" % (zeus.__version__))
log = zeus.log.Log("./tmp/log_sample4.log", frequence='m')
log.logger.info("%s %s", "sample4", "message1")
log.set_level(logging.INFO)
log.set_stdout_level(logging.DEBUG)
log.logger.debug("%s %s", "sample4", "message2")
