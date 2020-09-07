import numpy as np

class AES:
  # done
  @staticmethod
  def createKey(length):
    return np.random.randint(0,256,(4,4))

  # done
  @staticmethod
  def sBox(number):
    data = np.array([99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]).reshape((16,16))
    numberHex = f'{int(number):02x}'
    x = numberHex[0]
    y = numberHex[1]
    return data[int(x, 16)][int(y, 16)]

  # done
  @staticmethod
  def sBoxInv(number):
    data = np.array([82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]).reshape((16,16))
    numberHex = f'{int(number):02x}'
    x = numberHex[0]
    y = numberHex[1]
    return data[int(x, 16)][int(y, 16)]

  #done
  @staticmethod
  def validKey(key, length):
    if(type(key) is not np.ndarray):
      return False
    if(np.any(key>255) or np.any(key<0) or key.shape != (4,4)):
      return False
    return True

  # maybe done
  def __init__(self, key=None):
    self.bitlen = 128

    if self.bitlen == 128:
      self.rounds = 10
    elif self.bitlen == 192:
      self.rounds = 12
    elif self.bitlen == 256:
      self.rounds = 14

    if key is None:
      self.key = self.createKey(self.bitlen)
      print('New AES with random key generated')
    else:
      if(not self.validKey(key, self.bitlen)):
        raise ValueError("invalid key")
      self.key = key
      print('New AES with custom key generated')
    
    self.state = np.zeros((4,4), dtype=int)

  # done
  def getKey(self):
    return self.key

  # done
  def setKey(self,key):
    if(not self.validKey(key, self.bitlen)):
      raise ValueError("invalid key")
    self.key = key
  
  # done
  def byteSub(self):
    sBoxVectorize = np.vectorize(self.sBox)
    self.state = sBoxVectorize(self.state)

  # done
  def shiftRows(self):
    self.state[1] = np.roll(self.state[1], 3)
    self.state[2] = np.roll(self.state[2], 2)
    self.state[3] = np.roll(self.state[3], 1)

  # done
  def mixCol(self):
    resultState = np.zeros((4,4))
    for c in range(0,4):
      # for each column in the state
      col = self.state[:,c:c+1].reshape(4,)
      for r in range(0,4):
        # for each row in the state
        row = np.roll([2,3,1,1], r)
        result = 0
        for e in range(0,4):
          # for each cell/entry in the selected row
          binNumber = f'{int(col[e]):08b}'
          binNumber = binNumber[::-1]
          if row[e] == 1:
            resBin = binNumber
          if row[e] == 2:
            resBin = ""
            resBin += binNumber[7]
            resBin += "0" if binNumber[0] == binNumber[7] else "1"
            resBin += binNumber[1]
            resBin += "0" if binNumber[2] == binNumber[7] else "1"
            resBin += "0" if binNumber[3] == binNumber[7] else "1"
            resBin += binNumber[4]
            resBin += binNumber[5]
            resBin += binNumber[6]
          if row[e] == 3:
            resBin = ""
            resBin += "0" if binNumber[0] == binNumber[7] else "1"
            resBin += "0" if binNumber[0] == ("0" if binNumber[1] == binNumber[7] else "1") else "1"
            resBin += "0" if binNumber[1] == binNumber[2] else "1"
            resBin += "0" if binNumber[2] == ("0" if binNumber[3] == binNumber[7] else "1") else "1"
            resBin += "0" if binNumber[3] == ("0" if binNumber[4] == binNumber[7] else "1") else "1"
            resBin += "0" if binNumber[4] == binNumber[5] else "1"
            resBin += "0" if binNumber[5] == binNumber[6] else "1"
            resBin += "0" if binNumber[6] == binNumber[7] else "1"
          resBin = resBin[::-1]
          result = result ^ int(resBin, 2)
        resultState[r][c] = result
    self.state = np.copy(resultState)

  # done
  def roundConsts(self, maxRounds):
    # rConst = np.array([141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154])
    roundConst = np.array(np.zeros(maxRounds+1), dtype = int)
    for i in range (1,maxRounds+1,1):
        if(i == 1):
            roundConst[i] = 1
        elif(i > 1 and roundConst[i-1] < 128):
            roundConst[i] = 2*roundConst[i-1]
        else:
            roundConst[i] = (2*roundConst[i-1])^283
    return roundConst

  # done
  def gfunc(self, last32bits, roundConst):
    result = np.roll(last32bits,3)
    sBoxVectorize = np.vectorize(self.sBox)
    result = sBoxVectorize(result)
    result[0] = result[0]^roundConst
    return result

  # done
  def calcKeys(self, key, maxRounds):
    key = np.zeros((4,4), dtype=int)
    subKeys = [np.copy(key)]
    roundConst = self.roundConsts(maxRounds)
    for i in range (1, maxRounds +1):
        nextKey = np.copy(subKeys[i-1])
        nextKey[:,0:1] = nextKey[:,0:1]^self.gfunc(nextKey[:,3:4].reshape((4,)), roundConst[i]).reshape((4,1))
        nextKey[:,1:2] = nextKey[:,0:1]^nextKey[:,1:2]
        nextKey[:,2:3] = nextKey[:,1:2]^nextKey[:,2:3]
        nextKey[:,3:4] = nextKey[:,2:3]^nextKey[:,3:4]
        subKeys.append(nextKey)
    return np.array(subKeys)

  # done
  def addKey(self, roundKey):
    self.state = (self.state + roundKey) % 256

  # done
  def addKey(self, roundKey):
    self.state = (self.state - roundKey) % 256
  
  #def changeMode() change bitLength


class AES_ECB(AES):
  def encrypt(self, data):
    if type(data) == str:
      byteData = bytearray(data, "utf-8")
    else:
      byteData = bytearray(data)
    
    padding = 16-(len(byteData) % 16)
    for i in range(padding):
      byteData.append(0)
      
  def decrypt(self, data):
    print("test")



con = AES_ECB()

#con = AES_ECB(AES.createKey(128))

con.encrypt("Ähallo")

#print(con.getKey())

#con = AES(key)

#con.getKey()

#con.setKey()

#con.encrypt(string)

#con.decrypt()

