import numpy as np

class SHA3:
	def __init__(self, outputLength=256):
		if type(outputLength) != int:
			raise ValueError("the output length must be of type int")
		if outputLength not in [224,256,384,512]:
			raise ValueError("The only valid output length are 224, 256, 384 and 512")
		self._b = 1600
		self._outputLength = outputLength
		self._c = int(2*outputLength)
		self._r = int(1600 - self._c)
		self._nr = 24
		self._state = np.zeros((5,5),dtype=np.uint64)

	def hash(self, data=""):
		"""
		This function creates the hash for the input data.
		"""
		if type(data) == str:
			byteData = bytearray(data, "utf-8")
		else:
			byteData = bytearray(data)

		# reverse bits in bytes
		byteDataRev = bytearray()
		for i in byteData:
			byteTmp = f"{i:08b}"[::-1]
			byteTmp = int(byteTmp, 2)
			byteDataRev.append(byteTmp)
		byteData = byteDataRev
		
		# add padding
		byteData = self._padding(byteData)

		if (len(byteData)*8) % self._r != 0:
			raise ValueError("some error while doing the padding")
		
		steps = int(len(byteData)*8/self._r)

		rInByte = int(self._r / 8)

		for i in range(steps):
			# take in each round a block of r bits from the input
			sponge_XOR_block = byteData[i*rInByte:i*rInByte+rInByte]
			for j in range(int(rInByte / 8)):
				# for every byte in this block
				tmpLane = np.uint64(0)
				for o in range(8):
					# for every 64 bit
					tmpLane = np.bitwise_xor(np.left_shift(tmpLane, np.uint64(8)), np.uint64(sponge_XOR_block[8*j+o]))
				tmpLane = f"{tmpLane:064b}"[::-1]
				tmpLane = np.uint64(int(tmpLane, 2))
				self._state[j%5][int((j-j%5)/5)] = np.bitwise_xor(self._state[j%5][int((j-j%5)/5)], tmpLane)
			self._fFunc()

		output = bytearray()

		for y in range(5):
			for x in range(5):
				laneTmp = self._state[x][y]
				for o in range(8):
					output.append(np.bitwise_and(laneTmp, np.uint64(int("ff",16))))
					laneTmp = np.right_shift(laneTmp, np.uint64(8))

		#create hash from bytearray
		output = output[:int(self._outputLength/8)]
		outputStr = ""
		for i in output:
			outputStr+=f"{i:02x}"
		return outputStr

	def _padding(self, data):
		"""
		This function creates the padding for the input data.
		"""
		if (len(data)*8) % self._r == self._r - 8:
			data.append(int("01100001",2))
			return data
		
		data.append(int("01100000",2))
		
		while (len(data)*8) % self._r != self._r - 8:
			data.append(0)
			
		data.append(int("00000001",2))
		return data

	def _fFunc(self):
		"""
		This function calculates the output of the f-function
		"""
		for i in range(self._nr):
			self._theta()
			self._rhoANDpi()
			self._chi()
			self._jota(i)
	
	def _theta(self):
		"""
		This state calculates:

		c[x] = state[x][0] xor state[x][1] xor state[x][2] xor state[x][3] xor state[x][4]
		d[x] = c[x-1] xor rot(c[x+1], 1)
		state[x][y] = state[x][y] xor d[x]
		"""
		compressedState = np.zeros((5,), dtype=np.uint64)
		for x in range(5):
			for y in range(5):
				compressedState[x] = np.bitwise_xor(compressedState[x], self._state[x][y])
		
		for y in range(5):
			for x in range(5):
				self._state[x][y] = np.bitwise_xor(np.bitwise_xor(compressedState[(x-1)%5], np.bitwise_xor(np.left_shift(compressedState[(x+1)%5], np.uint64(1)), np.right_shift(compressedState[(x+1)%5], np.uint(63)))), self._state[x][y])

	def _rhoANDpi(self):
		"""
		This step mixes and rotates the lanes.
		
		newState[y][2x+3y] = rot(state[x][y], rotTable[x][y])
		"""
		rotTable = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]

		newState = np.zeros((5,5),dtype=np.uint64)

		for y in range(5):
			for x in range(5):
				newState[y][(2*x+3*y)%5] = np.bitwise_xor(np.left_shift(self._state[x][y], np.uint64(rotTable[x][y])), np.right_shift(self._state[x][y], np.uint64(64 - rotTable[x][y])))
				
		self._state = np.copy(newState)
	
	def _chi(self):
		"""
		This function calculates:

		newState[x][y] = state[x][y] xor (not state[x+1][y] and state[x+2][y])
		"""
		newState = np.zeros((5,5),dtype=np.uint64)
		for y in range(5):
			for x in range(5):
				tmp = np.bitwise_xor(self._state[(x+1)%5][y] , np.uint64(int("ffffffffffffffff", 16)))
				tmp = np.bitwise_and(tmp, self._state[(x+2)%5][y])
				newState[x][y] = np.bitwise_xor(self._state[x][y], tmp)
		self._state = np.copy(newState)
	
	def _jota(self, round):
		"""
		This function adds a round constant to the lane self._state[0][0]
		"""
		roundConst = [
			"0000000000000001",
			"0000000000008082",
			"800000000000808A",
			"8000000080008000",
			"000000000000808B",
			"0000000080000001",
			"8000000080008081",
			"8000000000008009",
			"000000000000008A",
			"0000000000000088",
			"0000000080008009",
			"000000008000000A",
			"000000008000808B",
			"800000000000008B",
			"8000000000008089",
			"8000000000008003",
			"8000000000008002",
			"8000000000000080",
			"000000000000800A",
			"800000008000000A",
			"8000000080008081",
			"8000000000008080",
			"0000000080000001",
			"8000000080008008"]
		self._state[0][0] = np.bitwise_xor(self._state[0][0], np.uint64(int(roundConst[round], 16)))
	