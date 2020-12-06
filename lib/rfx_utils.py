#!/usr/bin/env python3
# coding=UTF-8
"""
RFX Utils

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

from binascii import hexlify

# --------------------------------------------------------------------------

def stripped(str):
	"""
	Strip all characters that are not valid
	Credit: http://rosettacode.org/wiki/Strip_control_codes_and_extended_characters_from_a_string
	"""
	return "".join([i for i in str if ord(i) in range(32, 127)])

# --------------------------------------------------------------------------

def ByteToHex( byteStr ):
	"""
	Convert a byte string to it's hex string representation e.g. for output.
	http://code.activestate.com/recipes/510399-byte-to-hex-and-hex-to-byte-string-conversion/

	Added str() to byteStr in case input data is in integer
	"""
	try:
		return hexlify(byteStr).decode("utf-8")
	except:
		return "{0:#0{1}x}".format(byteStr, 4).split("0x")[1]
	return "00"

# ----------------------------------------------------------------------------

def dec2bin(x, width=8):
	"""
	Base-2 (Binary) Representation Using Python
	http://stackoverflow.com/questions/187273/base-2-binary-representation-using-python
	Brian (http://stackoverflow.com/users/9493/brian)
	"""
	return ''.join(str((x>>i)&1) for i in range(width-1,-1,-1))

# ----------------------------------------------------------------------------

def testBit(int_type, offset):
	"""
	testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
	http://wiki.python.org/moin/BitManipulation
	"""
	mask = 1 << offset
	return(int_type & mask)

# ----------------------------------------------------------------------------

def clearBit(int_type, offset):
	"""
	clearBit() returns an integer with the bit at 'offset' cleared.
	http://wiki.python.org/moin/BitManipulation
	"""
	mask = ~(1 << offset)
	return(int_type & mask)

# ----------------------------------------------------------------------------

def split_len(seq, length):
	"""
	Split string into specified chunks.
	"""
	return [seq[i:i+length] for i in range(0, len(seq), length)]

# ----------------------------------------------------------------------------
