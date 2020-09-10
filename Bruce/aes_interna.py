import numpy as np
from .gf import GF2M


class AES:
	"""
	# AES
	This class implements the basic functions used by the AES algorithm. You should not create an object of this class, but use one of the child classes like AES_ECB instead, because this class does not implement the encrypt or decrypt function which differ on the used mode.
	"""
	_sBoxData = np.array([
		99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171,
		118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156,
		164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241,
		113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226,
		235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179,
		41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57,
		74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127,
		80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218,
		33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167,
		126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238,
		184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211,
		172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108,
		86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198,
		232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246,
		14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217,
		142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191,
		230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
	]).reshape((16, 16))

	_sBoxDataInv = np.array([
		82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215,
		251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222,
		233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66,
		250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109,
		139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204,
		93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70,
		87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228,
		88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175,
		189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242,
		207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133,
		226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197,
		137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210,
		121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136,
		7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25,
		181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77,
		174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126,
		186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125
	]).reshape((16, 16))

	def _sBox(self, number):
		"""
		# S-Box
		This function computes the output of the S-Box (substitution-box) of the AES algorithm. It uses an already computet lookup table.
		## parameter
		### number
		The input of this function needs to be one byte or an integer between 0 and 255.
		## return
		This function returns the output of the S-Box as one byte or an interger between 0 and 255.
		"""
		numberHex = f'{int(number):02x}'
		x = numberHex[0]
		y = numberHex[1]
		return self._sBoxData[int(x, 16)][int(y, 16)]

	def _sBoxInv(self, number):
		"""
		# S-Box (inverted)
		This function computes the output of the inverted S-Box (substitution-box) of the AES algorithm. It uses an already computet lookup table.
		## parameter
		### number
		The input of this function needs to be one byte or an integer between 0 and 255.
		## return
		This function returns the output of the S-Box as one byte or an interger between 0 and 255.
		"""
		numberHex = f'{int(number):02x}'
		x = numberHex[0]
		y = numberHex[1]
		return self._sBoxDataInv[int(x, 16)][int(y, 16)]

	
	def _createKey(self, length):
		"""
		# create key
		This function creates a random key to be used as the private key for encryption and decryption.
		## parameter
		### length
		The bit length or security level that should be used for encryption. The only bit lengths that are supported by AES are 128, 192 and 256.
		## return
		This function returns a random key as a numpy array where each entry is one byte.
		"""
		if length == 128:
			return np.random.randint(0, 256, (16, ))
		elif length == 192:
			return np.random.randint(0, 256, (24, ))
		elif length == 256:
			return np.random.randint(0, 256, (32, ))


	def _validKey(self, key, bitLength):
		"""
		# valid key
		This function tests if the key is a valid AES key.
		## parameter
		### key
		The key that should be tested.
		### bitLength
		The bit length the key should have.
		## return
		This function returns True or False.
		"""
		if type(key) != list and type(key) != np.ndarray:
			return False
		key = np.array(key)
		if key.ndim != 1:
			return False
		if key.dtype != int:
			return False
		if np.any(key > 255) or np.any(key < 0):
			return False
		if bitLength == 128 and key.size != 16:
			return False
		elif bitLength == 192 and key.size != 24:
			return False
		elif bitLength == 256 and key.size != 32:
			return False
		return True

	def __init__(self, bitLength=128, key=None):
		"""
		# Constructor
		This constructor initialized all the internal AES parameters.
		## parameter
		### bitLength
		The bit length or security level that should be used for encryption and decryption. The only bit lengths that are supported by AES are 128, 192 and 256. If no bit length is specified then 128 is used.
		### key
		the private key that should be used for encryption and decreyption. If one is provided it has to be a list or a numpy array of bytes or integers between 0 and 255. Its dimention also has to match the bit length. For 128 the shape needs to be (16,), for 192 (24,) and for 256 the shape needs to be (32,). If no key is specified than a random key is generated.
		"""
		if bitLength not in [128,192,256]:
			raise ValueError("the only allowed bit lengths are 128, 192 and 256")
		self._bitLength = bitLength

		if self._bitLength == 128:
			self._rounds = 10
		elif self._bitLength == 192:
			self._rounds = 12
		elif self._bitLength == 256:
			self._rounds = 14

		if key is None:
			self._privateKey = self._createKey(self._bitLength)
			print('New AES with random key generated and mode', self._modeOfOperation)
		else:
			if (not self._validKey(key, self._bitLength)):
				raise ValueError("invalid key")
			self._privateKey = np.array(key)
			print('New AES with custom key generated and mode', self._modeOfOperation)

		self._state = np.zeros((4, 4), dtype=int)

	def getKey(self):
		"""
		# get key
		This function just returns the private key.
		## return
		This function returns the key as a numpy array where each entry is one byte and the number of entry relates to the used bit length.
		"""
		return self._privateKey

	def _addKey(self, roundKey):
		"""
		# key addition
		This function implements the key addition layer of the AES algorithm used in both encryption and decryption. In this layer, the XOR of curent state and the current round key is calculated.
		## parameter
		### roundKey
		The round key that should be used.
		"""
		self._state = (self._state ^ roundKey)

	def _byteSub(self):
		"""
		# byte sub layer
		This function implements the byte substitution layer used in AES encryption. In this layer, the S-Box is applied to every entry of the state.
		"""
		sBoxVectorize = np.vectorize(self._sBox)
		self._state = sBoxVectorize(self._state)

	def _byteSubInv(self):
		"""
		# byte substitution layer (inverted)
		This function implements the inverted byte sub layer that replaces the byte sub layer in AES decryption. In this layer, the inverted S-Box is applied to every entry of the state.
		"""
		sBoxVectorize = np.vectorize(self._sBoxInv)
		self._state = sBoxVectorize(self._state)

	def _shiftRows(self):
		"""
		# shift rows layer
		This function implements the shift row layer used in AES encryptioon. In this layer every row of the state is rotated by a fixed amount to the right.
		"""
		self._state[1] = np.roll(self._state[1], 3)
		self._state[2] = np.roll(self._state[2], 2)
		self._state[3] = np.roll(self._state[3], 1)

	def _shiftRowsInv(self):
		"""
		# shift rows layer (inverted)
		This function implements the inverted shift row layer that replaces the shift row layer in AES decryption. In this layer every row of the state is rotated by a fixed amount to the right.
		"""
		self._state[1] = np.roll(self._state[1], 1)
		self._state[2] = np.roll(self._state[2], 2)
		self._state[3] = np.roll(self._state[3], 3)

	def _mixCol(self):
		"""
		# mix columns
		This function implements the inverted mix column layer used in AES encryption. In this layer the bytes in every column of the state are scrambled, resulting to every byte in a column affecting all the other bytes in the same column.
		"""
		self.__mixColIntern([2, 3, 1, 1])

	def _mixColInv(self):
		"""
		# mix columns (inverted)
		This function implements the inverted mix column layer of the AES algorithm that replaces the mix column layer in AES decryption. In this layer, the bytes in every column of the state are scrambled, resulting to every byte in a column affecting all the other bytes in the same column.
		"""
		self.__mixColIntern([14, 11, 13, 9])
	
	def __mixColIntern(self, arr):
		resultState = np.zeros((4, 4), dtype=int)
		for c in range(0, 4):
			# for each column in the state
			col = self._state[:, c:c + 1].reshape(4, )
			for r in range(0, 4):
				# for each row in the state
				row = np.roll(arr, r)
				result = 0
				for e in range(0, 4):
					# for each cell/entry in the selected row
					elementFromColum = col[e]
					elementFromRow = row[e]

					p = GF2M([1, 0, 0, 0, 1, 1, 0, 1, 1])
					res = GF2M(int(elementFromColum)).multiplyConst(int(elementFromRow), p).getData()
					res = ''.join(map(str,res))
					if res == "":
						res = "0"
					res = int(res, 2)
					result ^= res
				resultState[r][c] = result
		self._state = np.copy(resultState)

	def _roundConsts(self):
		"""
		# round constants
		This function generates all the round constants that are used in the g-function of the sub key generation schedule.
		## return
		This function returns a numpy array with all the round constants.
		"""
		roundConst = np.zeros((14, ), dtype=int)
		for i in range(1, 14):
			if (i == 1):
				roundConst[i] = 1
			else:
				roundConst[i] = 2 * roundConst[i - 1]
				if roundConst[i] > 255:
					roundConst[i] ^= 283
		return roundConst

	def _gFunc(self, inputData, roundConst):
		"""
		# g-function
		This function implements the g-function used in the sub key generation algorithm (calcRoundKeys()).
		## parameter
		### inputData
		The input data for the g-function.
		### roundConst
		The current round constant.
		## return
		This function returns a numpy array.
		"""
		result = np.roll(inputData, 3)
		sBoxVectorize = np.vectorize(self._sBox)
		result = sBoxVectorize(result)
		result[0] = result[0] ^ roundConst
		return result

	def _hFunc(self, inputData):
		"""
		# h-function
		This function implements the h-functin used in the sub key generation algorithm (calcRoundKeys()). It is only used in the key schedule for 256-bit-keys.
		## parameter
		### inputData
		The input data for the h-function.
		## return
		This function returns a numpy array.
		"""
		sBoxVectorize = np.vectorize(self._sBox)
		result = sBoxVectorize(inputData)
		return result

	def _calcRoundKeys(self, key, bitLength):
		"""
		# calculate Keys
    	In AES, the keys used in the key addition layer differ each round. This function calculates the round keys based on the chosen or randomly generated main key and the AES key schedule used for a key of the given length. Encryption and decryption in AES use the same keys in the opposite order, meaning that this function does not need to be inverted.
		"""    
		subKeys = []

		roundConst = self._roundConsts()

		words = []
		for i in range(int(key.size / 4)):
			words.append(key[4 * i:4 * i + 4])

		if bitLength == 128:
			for i in range(10):
				words.append(words[-4] ^ self._gFunc(words[-1], roundConst[i + 1]))
				words.append(words[-4] ^ words[-1])
				words.append(words[-4] ^ words[-1])
				words.append(words[-4] ^ words[-1])
		elif bitLength == 192:
			for i in range(8):
				if i == 7:
					words.append(words[-6] ^ self._gFunc(words[-1], roundConst[i + 1]))
					words.append(words[-6] ^ words[-1])
					words.append(words[-6] ^ words[-1])
					words.append(words[-6] ^ words[-1])
				else:
					words.append(words[-6] ^ self._gFunc(words[-1], roundConst[i + 1]))
					words.append(words[-6] ^ words[-1])
					words.append(words[-6] ^ words[-1])
					words.append(words[-6] ^ words[-1])
					words.append(words[-6] ^ words[-1])
					words.append(words[-6] ^ words[-1])
		elif bitLength == 256:
			for i in range(7):
				if i == 6:
					words.append(words[-8] ^ self._gFunc(words[-1], roundConst[i + 1]))
					words.append(words[-8] ^ words[-1])
					words.append(words[-8] ^ words[-1])
					words.append(words[-8] ^ words[-1])
				else:
					words.append(words[-8] ^ self._gFunc(words[-1], roundConst[i + 1]))
					words.append(words[-8] ^ words[-1])
					words.append(words[-8] ^ words[-1])
					words.append(words[-8] ^ words[-1])
					words.append(words[-8] ^ self._hFunc(words[-1]))
					words.append(words[-8] ^ words[-1])
					words.append(words[-8] ^ words[-1])
					words.append(words[-8] ^ words[-1])
		for i in range(int(len(words) / 4)):
			subKeys.append(words[4 * i:4 * i + 4])
		return np.array(subKeys)

	def _encryptIntern(self):
		"""
		# encryptIntern
		This function encrypts a single 128-bit-block of plaintext with the given key of  bitlength 128, 192 or 256 with the appropiate AES schedule.
		"""   
		roundKeys = self._calcRoundKeys(self._privateKey, self._bitLength)
		for j in range(0, self._rounds + 1):
			if (j == 0):
				self._addKey(roundKeys[0].T)
			else:
				self._byteSub()
				self._shiftRows()
				if j != self._rounds:
					self._mixCol()
				self._addKey(roundKeys[j].T)

	def _decryptIntern(self):
		"""
		# decryptIntern
		This function decrypts a single 128-bit-block of cyphertext with the given key of bitlength 128, 192 or 256 with the appropiate AES schedule.
		"""
		roundKeys = self._calcRoundKeys(self._privateKey, self._bitLength)
		for j in range(0, self._rounds + 1):
			k = self._rounds - j
			if (j == self._rounds):
				self._addKey(roundKeys[0].T)
			else:
				self._addKey(roundKeys[k].T)
				if (j != 0):
					self._mixColInv()
				self._shiftRowsInv()
				self._byteSubInv()