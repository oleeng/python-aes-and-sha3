import numpy as np
from .aes_interna import AES
from progress.bar import ChargingBar


class AES_ECB(AES):
	"""
	# AES_ECB
	This class implements AES in ECB (electronic codebook) mode. Since AES can only encrypt 128 bits of plaintext at a time (regardless of AES-128, -192 or -256 being used), to allow encryption of data of any given length it needs to be run in a specific mode that determines the way subsequent 128-bit-blocks are being encrypted. ECB mode is the simplest of those, as it encrypts each block individually. This will lead to identical blocks of plaintext being encrypted to identical blocks of cyphertext.
	"""
	def __init__(self, bitLength=128, key=None):
		self._modeOfOperation = "ECB"
		super().__init__(bitLength, key)

	def encrypt(self, data):
		"""
		# encrypt
		This function encrypts the given data by seperately encrypting each 128-bit-block of the (plaintext) input using the AES encryption protocol and the object's key.
		"""  
		if type(data) == str:
			byteData = bytearray(data, "utf-8")
		else:
			byteData = bytearray(data)

		padding = 16 - (len(byteData) % 16)
		for i in range(padding):
				byteData.append(padding)

		resultEnc = []

		bar = ChargingBar('Processing', max=(int(len(byteData) / 16)))

		for i in range(0, int(len(byteData) / 16)):
			self._state = np.array(byteData[16 * i:16 * (i + 1)]).reshape((4, 4)).T
			self._encryptIntern()
			bar.next()
			resultEnc.append(np.copy(self._state))
		bar.finish()

		resultByte = bytearray()

		for i in resultEnc:
			t = i.T.reshape(16, )
			for j in t:
				resultByte.append(j)

		return resultByte

	def decrypt(self, data):
		"""
		# decrypt
		This function decrypts the given data by seperately decrypting each 128-bit-block of the (cyphertext) input using the AES decryption protocol and the object's key.
		"""  
		if type(data) != bytearray:
			raise ValueError("only byte array is allowed")

		resultDec = []

		bar = ChargingBar('Processing', max=(int(len(data) / 16)))

		for i in range(0, int(len(data) / 16)):
			self._state = np.array(data[16 * i:16 * (i + 1)]).reshape((4, 4)).T
			
			self._decryptIntern()

			resultDec.append(np.copy(self._state))
			bar.next()
		bar.finish()
		resultByte = bytearray()
		for i in resultDec:
			t = i.T.reshape(16, )
			for j in t:
				resultByte.append(j)
		
		lastByte = resultByte[-1]
		resultByte = resultByte[:-lastByte]

		return resultByte


class AES_CBC(AES):
	"""
	# AES_ECB
	This class implements AES in CBC (cipher block chaining) mode. Since AES can only encrypt 128 bits of plaintext at a time (regardless of AES-128, -192 or -256 being used), to allow encryption of data of any given length it needs to be run in a specific mode that determines the way subsequent 128-bit-blocks are being encrypted. In CBC mode, the XOR of the current block and the cyphertext of the last block is being calculated before entering AES, using an initialization vector insted of the cyphertext for the first block to encrypt. This way, CBC encrypts identical blocks of plaintext to different blocks of cyphertext.
	"""    
	def __init__(self, bitLength=128, key=None):
		self._modeOfOperation = "CBC"
		super().__init__(bitLength, key)

	def encrypt(self, data):
		"""
		# encrypt
		This function encrypts the given (plaintext) data by dividing them into 128-bit-blocks. The first block is encrypted using the given main key and the standard AES enrcyption schedule after being XORed with a random initialization vector. The consecutive blocks are XORed with the last encrypted block's cyphertext before encryption.
		"""    
		NonceIV = np.random.randint(0, 256, (4, 4))

		if type(data) == str:
			byteData = bytearray(data, "utf-8")
		else:
			byteData = bytearray(data)

		padding = 16 - (len(byteData) % 16)
		for i in range(padding):
				byteData.append(padding)

		resultEnc = []

		lastIVorY = np.copy(NonceIV)

		bar = ChargingBar('Processing', max=int(len(byteData) / 16))

		for i in range(0, int(len(byteData) / 16)):
			self._state = np.array(byteData[16 * i:16 * (i + 1)]).reshape((4, 4)).T
			self._state = self._state ^ lastIVorY
			
			self._encryptIntern()
			
			lastIVorY = np.copy(self._state)
			resultEnc.append(np.copy(self._state))

			bar.next()
		bar.finish()

		resultByte = bytearray()

		for i in resultEnc:
			t = i.T.reshape(16, )
			for j in t:
				resultByte.append(j)

		return [resultByte, NonceIV]

	def decrypt(self, data):
		"""
		# decrypt
		This function decrypts the given (cyphertext) data by dividing them into 128-bit-blocks. The first block is decrypted using the given main key and the standard AES enrcyption schedule and then XORed with the initialization vector that was used for encryption. The consecutive blocks are XORed with the last decrypted block's cyphertext (!) after encryption.
		"""    
		NonceIV = data[1]
		data = data[0]

		if type(data) != bytearray:
			raise ValueError("only byte array is allowed")
		if type(NonceIV) != np.ndarray:
			raise ValueError("IV must be np array")
		if NonceIV.shape != (4, 4):
			raise ValueError("IV has to have a shape of (4,4)")

		resultDec = []

		lastIVorY = np.copy(NonceIV)

		bar = ChargingBar('Processing', max=(int(len(data) / 16)))

		for i in range(0, int(len(data) / 16)):
			self._state = np.array(data[16 * i:16 * (i + 1)]).reshape((4, 4)).T
			tmpY = np.copy(self._state)
			
			self._decryptIntern()
			
			self._state = self._state ^ lastIVorY
			lastIVorY = np.copy(tmpY)
			resultDec.append(np.copy(self._state))
			bar.next()
		bar.finish()
		resultByte = bytearray()
		for i in resultDec:
			t = i.T.reshape(16, )
			for j in t:
				resultByte.append(j)

		lastByte = resultByte[-1]
		resultByte = resultByte[:-lastByte]

		return resultByte
