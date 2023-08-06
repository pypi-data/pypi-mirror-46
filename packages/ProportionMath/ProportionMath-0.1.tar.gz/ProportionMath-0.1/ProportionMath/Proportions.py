from ProportionMath.InputValidator import Validator

class Proportion():

    __proportion = [['a','b'], ['c','d']]
    __posOfX = []
    __validator = Validator()

    def Proportion(self, a, b, c, d):
        self.__proportion[0][0] = self.__setValue(a)
        self.__proportion[0][1] = self.__setValue(b)
        self.__proportion[1][0] = self.__setValue(c)
        self.__proportion[1][1] = self.__setValue(d)
        self.__checkMultipleX()
        self.__findZeroInArray()
        return self.__solve()

    def __setValue(self, value):
        if(self.__validator.isValueNumeric(value)):
            return value
        elif(self.__validator.isValueX(value)):
            return 'x'
        else:
            raise Exception('x character and numeric imput only')

    def __solve(self):
        if(self.__posOfX == (0,0)):
            return self.__solveEquationForX(self.__proportion[0][1], self.__proportion[1][0], self.__proportion[1][1])
        if(self.__posOfX == (0,1)):
            return self.__solveEquationForX(self.__proportion[0][0], self.__proportion[1][1], self.__proportion[1][0])
        if(self.__posOfX == (1,0)):
            return self.__solveEquationForX(self.__proportion[0][0], self.__proportion[1][1], self.__proportion[0][1])
        if(self.__posOfX == (1,1)):
            return self.__solveEquationForX(self.__proportion[0][1], self.__proportion[1][0], self.__proportion[0][0])  
        
    def __solveEquationForX(self, a, b, c):
        d = a * b
        return self.__validator.tryDivide(d,c)

    def __findZeroInArray(self):
        for sublist in self.__proportion:
            if 'x' in sublist or 'X' in sublist:
                self.__posOfX = (self.__proportion.index(sublist), sublist.index('x'))

    def __checkMultipleX(self):
        cnt = 0
        for sublist in self.__proportion:
            for num in sublist:
                if(num == 'x' or num == 'X'):
                    cnt += 1
        if cnt > 1:
            raise Exception("Can only have 1 variable x")