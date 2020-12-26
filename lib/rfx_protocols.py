#!/usr/bin/env python3
# coding=UTF-8
"""
RFX Protocols

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

import logging
logger = logging.getLogger("rfxcmd")

# ------------------------------------------------------------------------------

import sys
import xml.dom.minidom as minidom

# ------------------------------------------------------------------------------

def print_protocolfile(protocol_file):
    """
    Print the contents of the protocol configuration file to stdout
    """

    logger.debug("Open protocol file and read it, file: %s" % str(protocol_file))
    try:
        xmldoc = minidom.parse( protocol_file )
        logger.debug("XML file OK")
    except:
        print("Error in %s file" % str(protocol_file))
        sys.exit(1)

    try:
        data = xmldoc.documentElement.getElementsByTagName("protocol")
    except Exception as err:
        logger.error("Error: %s" % str(err))
        sys.exit(1)

    logger.debug("Read protocol tags in file")
    counter = 0

    print("Protocol.xml configuration")
    print("-----------------------------------")

    for protocol in data:
        try:
            id = int(protocol.getElementsByTagName("id")[0].childNodes[0].nodeValue)
        except Exception as err:
            logger.error("Error: %s" % str(err))
            sys.exit(1)

        if id != counter:
            print("Error: The id number is not in order")
            sys.exit(1)

        try:
            name = protocol.getElementsByTagName("name")[0].childNodes[0].nodeValue
        except Exception as err:
            logger.error("Error: %s" % str(err))
            sys.exit(1)

        try:
            state = int(protocol.getElementsByTagName("state")[0].childNodes[0].nodeValue)
            if state == 1:
                state_str = "Enabled"
            else:
                state_str = "Disabled"
        except Exception as err:
            logger.error("Error: %s" % str(err))
            sys.exit(1)

        if state != 0 and state != 1:
            print("Error: The state is either 0 or 1, in protocol %s" % str(name))
            sys.exit(1)

        print("%-25s %-15s" % (str(name), str(state_str)))
        logger.debug("Id: %s, State: %s, Counter: %s, Name: %s " % (str(id), str(state), str(counter), str(name)))
        counter += 1

    logger.debug("Tags total: %s" % str(counter))

    if counter != 24:
        logger.error("Error: There is not 24 protocol tags in protocol file")
        print("Error: There is not 24 protocol tags in protocol file")
        sys.exit(1)
    else:
        logger.debug("All tags found")

    return

# ------------------------------------------------------------------------------
def set_protocolfile(protocol_file):
    """
    Create the data message out of the protocol configuration file and return the packet
    """

    logger.debug("Open protocol file and read it, file: %s" % str(protocol_file))
    try:
        xmldoc = minidom.parse( protocol_file )
        logger.debug("XML file OK")
    except:
        print("Error in %s file" % str(protocol_file))
        sys.exit(1)

    try:
        data = xmldoc.documentElement.getElementsByTagName("protocol")
    except Exception as err:
        logger.error("Error: %s" % str(err))
        sys.exit(1)

    logger.debug("Read protocol tags in file")
    counter = 0

    msg = []
    msg3 = []
    msg4 = []
    msg5 = []

    for protocol in data:
        try:
            id = int(protocol.getElementsByTagName("id")[0].childNodes[0].nodeValue)
        except Exception as err:
            logger.error("Error: %s" % str(err))
            sys.exit(1)

        if id != counter:
            print("Error: The id number is not in order")
            sys.exit(1)

        try:
            name = protocol.getElementsByTagName("name")[0].childNodes[0].nodeValue
        except Exception as err:
            logger.error("Error: %s" % str(err))
            sys.exit(1)

        try:
            state = int(protocol.getElementsByTagName("state")[0].childNodes[0].nodeValue)
        except Exception as err:
            logger.error("Error: %s" % str(err))
            sys.exit(1)

        if state != 0 and state != 1:
            print("Error: The state is either 0 or 1, in protocol %s" % str(name))
            sys.exit(1)

        logger.debug("Id: %s, State: %s, Counter: %s, Name: %s " % (str(id), str(state), str(counter), str(name)))
        msg.insert(id, state)
        counter += 1

    logger.debug("Tags total: %s" % str(counter))

    if counter != 24:
        logger.error("Error: There is not 24 protocol tags in protocol file")
        print("Error: There is not 24 protocol tags in protocol file")
        sys.exit(1)
    else:
        logger.debug("All tags found")

    msg3 = msg[0:8]
    msg4 = msg[8:16]
    msg5 = msg[16:24]

    # Complete message
    try:
        msg3_bin = str(msg[0]) + str(msg[1]) + str(msg[2]) + str(msg[3]) + str(msg[4]) + str(msg[5]) + str(msg[6]) + str(msg[7])
        msg3_int = int(msg3_bin,2)
        msg3_hex = hex(msg3_int)[2:].zfill(2)
        msg4_bin = str(msg[8]) + str(msg[9]) + str(msg[10]) + str(msg[11]) + str(msg[12]) + str(msg[13]) + str(msg[14]) + str(msg[15])
        msg4_int = int(msg4_bin,2)
        msg4_hex = hex(msg4_int)[2:].zfill(2)
        msg5_bin = str(msg[16]) + str(msg[17]) + str(msg[18]) + str(msg[19]) + str(msg[20]) + str(msg[21]) + str(msg[22]) + str(msg[23])
        msg5_int = int(msg5_bin,2)
        msg5_hex = hex(msg5_int)[2:].zfill(2)
    except Exception as err:
        logger.error("Error: %s" % str(err))
        sys.exit(1)

    logger.debug("msg3: %s / %s" % (str(msg3), msg3_hex))
    logger.debug("msg4: %s / %s" % (str(msg4), msg4_hex))
    logger.debug("msg5: %s / %s" % (str(msg5), msg5_hex))

    command = "0D000000035300%s%s%s00000000" % (msg3_hex, msg4_hex, msg5_hex)
    logger.debug("Command: %s" % command.upper())

    return command

# ------------------------------------------------------------------------------
# EOF
# ------------------------------------------------------------------------------
