"""The converter module is used to convert a number into a padless base64 string and back.
Padless base64 are used for short urls: http://www.mydomain.com/MTQy for instance.
Base64 strings are normally organized by groups of 4 characters and right padded if necessary with =
Padless base64 means that = characters are removed"""

import base64

def encodeB64Padless(number):
	"""Encode an integer into a padless base64 string"""
	return base64.b64encode(str(number)).replace("=", "")

def decodeB64Padless(str):
	"""Decode a padless base64 string into an integer"""
	nbOfBlocks = len(str)/4
	for i in range(4 - len(str[nbOfBlocks*4:])): str += "="
	try:
		return int(base64.b64decode(str))
	except:
		return None # This means that str was not a valid padless b64