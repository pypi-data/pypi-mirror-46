
class Type():

    def tryParseInt(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def tryParseFloat(self, value):
        try:
            float(value)
            return True
        except:
            return False
            