import numpy as np


class GF2M:
	"""
	# Galois field - GF(2^m)
	This class implements the core operations of Galois fields or finite field that are used by the AES algoritm.
	"""
	def __init__(self, data):
		"""
		# Constructor
		This constructor takes an array or an int as the inputparameter to create a GF. If an array is provided its shape must be (n,) and every entry must be either 0 or 1. the leftmost entry is the most significant bit of the binary representation and the rightmost entry the least significant bit. If an int is provided it will be interpreted as the decimal representation of an binary number.
		"""
		if type(data) == int:
			dataBin = f'{data:b}'
			res = []
			for i in dataBin:
				res.append(int(i))
			data = res
		if (type(data) != list and type(data) != np.ndarray):
			raise ValueError("invalid datatype of input parameter")
		data = np.array(data)
		if data.ndim != 1:
			raise ValueError("invalid dimension of  inputarray")
		if data.dtype != int:
			raise ValueError("at least one entry in the input array is not of type int")
		if np.any(data < 0) or np.any(data > 1):
			raise ValueError( "at least one number inside the array is outside of the valid range of [0,1]")

		# remove leading zeros
		d = []
		zero = True
		for i in data:
			if zero and i == 0:
				continue
			else:
				zero = False
				d.append(i)
		self._data = np.array(d)

	def getData(self):
		"""
		# get data
		This function returns the data of the GF as an array of ones and zeros.
		"""
		return self._data

	def add(self, GF_Function):
		"""
		# add
		This function adds a GF to itself. For this no reduction GF is needed.
		"""
		if (type(GF_Function) != GF2M):
			raise ValueError("invalid input")

		if self._data.size > GF_Function._data.size:
			a = self._data
			b = GF_Function._data
		else:
			a = GF_Function._data
			b = self._data

		a = np.flip(a)
		b = np.flip(b)

		res = []

		for i in a:
			res.append(i)
		for i in range(b.size):
			res[i] ^= b[i]

		res = np.flip(res)

		return GF2M(res)

	def multiply(self, GF_Factor, GF_Modus):
		"""
		# multiply
		This function multiplies a GF to itself. For this a reduction GF is needed to ensure that the result stays inside the finite field.
		"""
		if (type(GF_Factor) != GF2M):
			raise ValueError("invalid input")
		if (type(GF_Modus) != GF2M):
			raise ValueError("invalid input")

		if self._data.size > GF_Factor._data.size:
			a = self._data
			b = GF_Factor._data
		else:
			a = GF_Factor._data
			b = self._data

		a = np.flip(a)
		b = np.flip(b)

		res = np.zeros((a.size + b.size, ), dtype=int)

		for i in range(a.size):
			if a[i] == 0:
				continue
			for j in range(b.size):
				if b[j] == 0:
					continue
				res[i + j] ^= 1

		res = np.flip(res)

		p = GF_Modus._data

		length = res.size
		lengthModus = p.size

		for i in range(0, length - lengthModus + 1):
			if res[i] == 1:
				for j in range(lengthModus):
					res[i + j] ^= p[j]

		return GF2M(res)

	def multiplyConst(self, number, GF_Modus):
		"""
		# multiply constant
		This function multiplies a constant to itself. For this a reduction GF is needed to ensure that the result stays inside the finite field.
		"""
		if (type(GF_Modus) != GF2M):
			raise ValueError("invalid input")
		if (type(number) != int):
			raise ValueError("invalid data")
		numberBin = f'{number:b}'
		res = []
		for i in numberBin:
			res.append(int(i))
		factor = GF2M(res)
		return self.multiply(factor, GF_Modus)

	def __repr__(self):
		"""
		This function is used to create a custom print() output.
		"""
		length = self._data.size
		resultString = ""
		for i in range(length):
			if self._data[i] == 1:
				if i == length - 1:
					resultString += "1"
				elif i == length - 2:
					resultString += "x+"
				else:
					resultString += "x^" + str(length - 1 - i) + "+"
		return "function: " + resultString.strip("+")

	def __str__(self):
		return self.__repr__()
