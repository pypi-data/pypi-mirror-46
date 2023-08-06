import numpy
from abc import ABC, abstractmethod


class Mask(ABC):

    def __init__(self, name, boardSize=4, maxTile=15):
        self.name = name
        self.boardSize = boardSize
        self.maxTile = maxTile

    @abstractmethod
    def getNumTuples(self):
        pass

    @abstractmethod
    def getMaxTupleNum(self):
        pass

    @abstractmethod
    def getTupleNums(self, state):
        pass

    def getTag(self):
        return self.name

    def getBoardSize(self):
        return self.boardSize


class Mask_rxcx4(Mask):

    def __init__(self, name='4x4x4', boardSize=4, maxTile=15):
        super().__init__(name, boardSize, maxTile)
        self.row_flag = 0
        self.column_flag = 1
        self.square_flag = 2

    def getNumTuples(self):
        return 2*self.boardSize + (self.boardSize-1)**2

    def getMaxTupleNum(self):
        return self.stateToTupleNum(numpy.full((self.boardSize,
                                    self.boardSize), self.maxTile),
                                    self.square_flag,(self.boardSize-1)**2-1)

    def getTupleNums(self, state):
        tupleNums = numpy.zeros(self.getNumTuples(), dtype=numpy.int)
        index = 0
        for tupleType in range(self.square_flag+1):
            if tupleType < self.square_flag:
                maxNum = self.boardSize
            else:
                maxNum = (self.boardSize - 1)**2
            for tupleIndex in range(maxNum):
                tupleNums[index] = self.stateToTupleNum(state, tupleType, tupleIndex)
                index += 1
        return tupleNums

    def stateToTupleNum(self, state, tupleType, tupleIndex):
        hexString = ''.join(['{:x}'.format(tupleType), '{:x}'.format(tupleIndex)])
        if(tupleType == self.row_flag):
            hexString += ''.join(['{:x}'.format(state[tupleIndex][col]) for col
                                  in range(self.boardSize)])
        elif(tupleType == self.column_flag):
            hexString += ''.join(['{:x}'.format(state[row][tupleIndex]) for row
                                  in range(self.boardSize)])
        elif(tupleType == self.square_flag):
            basex = tupleIndex % (self.boardSize - 1)
            basey = int(tupleIndex / (self.boardSize - 1))
            hexString += ''.join(['{:x}'.format(state[basex + i][basey + j])
                                  for i in range(2) for j in range(2)])
        return int(hexString, base=16)
