from PIL import Image
import numpy as np

"""
This is a collection of helper function that are used in the mian.py file
"""

def image2bytearray(path):
	"""
	This function creates a bytearray from an image that is provided as a path string.
	"""
	img = Image.open(path).resize((32, 32))
	img = np.asarray(img)[:, :, 0:1]
	return bytearray(img)

def bytearray2image(data):
	"""
	This function creates an image array from a bytearray.
	"""
	return np.array(data).reshape((32, 32))

def bytearray2hexstring(data):
	"""
	This function converts a bytearray to a hex string.
	"""
	resStr = ""
	for i in data:
		resStr += f"{i:02x}"
	return resStr