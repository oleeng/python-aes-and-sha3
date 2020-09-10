import Bruce
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(formatter={'int':hex})

showGF = False
showAES = True
showSHA3 = False


if showGF:
	# create some dumy GFs to show the different function that are available
	gf1 = Bruce.GF2M([1, 0, 0, 0, 1, 1, 0, 1, 1])
	gf2 = Bruce.GF2M(169)
	gf3 = Bruce.GF2M(np.array([1,0,0,0,1,1,0,1]))

	print(gf1)
	print(gf1.getData())
	print(gf2)
	print(gf2.getData())

	result = gf1.multiplyConst(169, gf3)
	print(result)
	result = gf1.add(gf2)
	print(result)
	result = gf1.multiply(gf2, gf3)
	print(result)

if showAES:
	# encrypt a string to demonstrate the .encrypt and .decrypt function
	
	aes = Bruce.AES_ECB(bitLength=256)
	key = Bruce.bytearray2hexstring(aes.getKey())
	enc = aes.encrypt("Das ist ein Test, ob AES funktioniert")
	print(key)
	print(Bruce.bytearray2hexstring(enc))
	dec = aes.decrypt(enc)
	print(dec.decode("utf-8"))

	# encrypt to images (one has one bitflip) to show the difference between ECB and CBC

	imgData = Bruce.image2bytearray("input/schneier2.jpg")
	imgDataBitflip = bytearray(np.copy(imgData))
	imgDataBitflip[0] ^= 1

	plt.imshow(Bruce.bytearray2image(imgData))
	plt.savefig("output/imageBeforeEncryption.png")

	cbc = Bruce.AES_CBC()
	ecb = Bruce.AES_ECB()

	encImgCBC = cbc.encrypt(imgData)
	encImgBitflipCBC = cbc.encrypt(imgDataBitflip)

	encImgECB = ecb.encrypt(imgData)
	encImgBitflipECB = ecb.encrypt(imgDataBitflip)

	diffECB = Bruce.bytearray2image(encImgECB[:-16]) - Bruce.bytearray2image(encImgBitflipECB[:-16])
	diffCBC = Bruce.bytearray2image(encImgCBC[0][:-16]) - Bruce.bytearray2image(encImgBitflipCBC[0][:-16])

	plt.subplot(1, 2, 1)
	plt.imshow(diffECB)

	plt.subplot(1, 2, 2)
	plt.imshow(diffCBC)

	plt.savefig("output/difference.png")

	imgDec = ecb.decrypt(encImgECB)

	plt.subplot(1, 1, 1)
	plt.imshow(Bruce.bytearray2image(imgDec))
	plt.savefig("output/imageAfterDecryption.png")

if showSHA3:
	# hash a string to demostrate the hash function
	sha = Bruce.SHA3(outputLength=512)
	hash = sha.hash("Das ist ein Test")
	print(hash)


# aes keys for testing
	#key128 = [224, 105, 0, 184, 132, 38, 225, 82, 29, 6, 55, 128, 110, 37, 86, 224]
	#key192 = [142, 115, 176, 247, 218,  14, 100,  82, 200,  16, 243,  43, 128, 144, 121, 229, 98, 248, 234, 210,  82,  44, 107, 123]
	#key256 = [ 69, 105, 110, 102, 117, 101, 104, 114, 117, 110, 103,  32, 105, 110,  32, 100, 105, 101,  32,  75, 114, 121, 112, 116, 111, 103, 114,  97, 112, 104, 105, 101]