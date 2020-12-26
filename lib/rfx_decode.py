#!/usr/bin/env python3
# coding=UTF-8
"""
RFX Decode

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

from lib.rfx_utils import ByteToHex, clearBit, testBit

# ----------------------------------------------------------------------------

def decode_temperature(message_high, message_low):
    """
    Decode temperature bytes.
    """
    temp_high = ByteToHex(message_high)
    temp_low = ByteToHex(message_low)
    polarity = testBit(int(temp_high, 16), 7)

    if polarity == 128:
        polarity_sign = "-"
    else:
        polarity_sign = ""

    temp_high = clearBit(int(temp_high, 16), 7)
    temp_high = temp_high << 8
    temperature = (temp_high + int(temp_low, 16)) * 0.1
    temperature_str = polarity_sign + str(temperature)

    return temperature_str

# ----------------------------------------------------------------------------

def decode_signal(message):
    """
    Decode signal byte.
    """
    signal = int(ByteToHex(message), 16) >> 4
    return signal

# ----------------------------------------------------------------------------

def decode_battery(message):
    """
    Decode battery byte.
    """
    battery = int(ByteToHex(message), 16) & 0xf
    return battery

# ----------------------------------------------------------------------------

def decode_power(message_1, message_2, message_3):
    """
    Decode power bytes.
    """
    power_1 = ByteToHex(message_1)
    power_2 = ByteToHex(message_2)
    power_3 = ByteToHex(message_3)

    power_1 = int(power_1, 16)
    power_1 = power_1 << 16
    power_2 = int(power_2, 16) << 8
    power_3 = int(power_3, 16)
    power = (power_1 + power_2 + power_3)
    power_str = str(power)

    return power_str

# ----------------------------------------------------------------------------
