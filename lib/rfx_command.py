#!/usr/bin/env python3
# coding=UTF-8
"""
RFX Command

Based on Sebastian Sjoholm work https://github.com/ssjoholm/rfxcmd_gc
Copyright 2012-2014 Sebastian Sjoholm, sebastian.sjoholm@gmail.com
Licensed under the GNU General Public License, Version 3.0
Copyright 2018-2020 by Nicolas BEGUIER, nicolas_beguier@hotmail.com

#
#   NOTES
#
#   RFXCOM is a Trademark of RFSmartLink.
#
# ------------------------------------------------------------------------------
#
#                          Protocol License Agreement
#
# The RFXtrx protocols are owned by RFXCOM, and are protected under applicable
# copyright laws.
#
# ==============================================================================
# It is only allowed to use this protocol or any part of it for RFXCOM products
# ==============================================================================
#
# The above Protocol License Agreement and the permission notice shall be
# included in all software using the RFXtrx protocols.
#
# Any use in violation of the foregoing restrictions may subject the user to
# criminal sanctions under applicable laws, as well as to civil liability for
# the breach of the terms and conditions of this license.
#
# ------------------------------------------------------------------------------
"""

__author__ = "Sebastian Sjoholm"
__copyright__ = "Copyright 2012-2014, Sebastian Sjoholm"
__license__ = "GPL"
__version__ = "2.0.1"
__maintainer__ = "Nicolas Béguier"
__date__ = "$Date: 2019-06-12 08:05:33 +0100 (Thu, 12 Jun 2019) $"

import logging
import subprocess
import threading

LOGGER = logging.getLogger('rfxcmd')

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            LOGGER.debug("Thread started, timeout = %s", str(timeout))
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            LOGGER.debug("Return code: %s", str(self.process.returncode))
            LOGGER.debug("Thread finished")
            self.timer.cancel()

        def timer_callback():
            LOGGER.debug("Thread timeout, terminate it")
            if self.process.poll() is None:
                try:
                    self.process.kill()
                except OSError as error:
                    LOGGER.error("Error: %s " % error)
                LOGGER.debug("Thread terminated")
            else:
                LOGGER.debug("Thread not alive")

        thread = threading.Thread(target=target)
        self.timer = threading.Timer(int(timeout), timer_callback)
        self.timer.start()
        thread.start()

# ----------------------------------------------------------------------------
