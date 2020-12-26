#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
RFX Socket

Based on Sebastian Sjoholm work https://github.com/ssjoholm/rfxcmd_gc
Copyright 2012-2014 Sebastian Sjoholm, sebastian.sjoholm@gmail.com
Licensed under the GNU General Public License, Version 3.0
Copyright 2018-2021 by Nicolas BEGUIER, nicolas_beguier@hotmail.com

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

from logging import getLogger
from queue import Queue
from socketserver import TCPServer, StreamRequestHandler
from threading import Thread

LOGGER = getLogger('rfxcmd')
TCPServer.allow_reuse_address = True
MESSAGEQUEUE = Queue()

# ------------------------------------------------------------------------------

class NetRequestHandler(StreamRequestHandler):

    def handle(self):
        LOGGER.debug("Client connected to [%s:%d]" % self.client_address)
        lg = self.rfile.readline()
        MESSAGEQUEUE.put(lg)
        LOGGER.debug("Message read from socket: %s", lg.strip())

        self.net_adapter_client_connected = False
        LOGGER.info("Client disconnected from [%s:%d]" % self.client_address)

class RFXcmdSocketAdapter(StreamRequestHandler):
    def __init__(self, address='localhost', port=55000):
        self.address = address
        self.port = port
        self.net_adapter = TCPServer((self.address, self.port), NetRequestHandler)
        if self.net_adapter:
            self.net_adapter_registered = True
            Thread(target=self.loopNetServer, args=()).start()

    def loopNetServer(self):
        LOGGER.info("LoopNetServer Thread started")
        LOGGER.info("Listening on: [%s:%d]" % (self.address, self.port))
        self.net_adapter.serve_forever()
        LOGGER.info("LoopNetServer Thread stopped")

# ------------------------------------------------------------------------------
# END
# ------------------------------------------------------------------------------
