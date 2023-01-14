import out

def numInput(text, limit):
    num = input(text)
    return checkValidNumber(num, limit)

def checkValidNumber(num, limit):
    validNum = False
    numInt = None
    while not validNum:
        try:
            numInt = int(num)
            if limit > numInt > 0:
                validNum = True
            else:
                num = input(out.INVALID_INPUT.format(str(limit)))
        except ValueError:
            num = input(out.INVALID_INPUT.format(str(limit)))
    return numInt