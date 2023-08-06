from ProportionMath.Type import Type

class Validator():

    typer = Type()

    def isValueX(self, value):
        if(value.lower() == 'x'):
            return True
        return False

    def isValueNumeric(self, value):
        if(self.typer.tryParseInt(value) or self.typer.tryParseFloat(value)):
            return True
        return False

    def tryDivide(self, numberOne, numberTwo):
        if(numberTwo != 0):
            return numberOne / numberTwo
        else:
            return 0