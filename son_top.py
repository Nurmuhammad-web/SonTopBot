from random import randint


def sonTopUser(son: int, result: dict) -> dict:
    result['attempt'] += 1
    if son == result['number']:
        result['ok'] = True
    elif son > result['number']:
        result['big'] = False
    elif son < result['number']:
        result['big?'] = True
    return result


def generateNumber() -> int:
    return randint(1, 10)


def updateResult(result: dict) -> str:
    result['ok'] = False
    result['attempt'] = 0
    result['big?'] = None
    result['number'] = generateNumber()
    return "Values are updated"


def compGenerateNumber(sign: str, result: dict) -> dict:
    if sign == '+':
        result['a'] = result['number'] + 1
    elif sign == '-':
        result['b'] = result['number'] - 1
    elif sign == 't':
        result['ok'] = True
    a = result['a']
    b = result['b']
    if a > b:
        result['honest'] = False
        return result
    result['number'] = randint(a, b)
    result['attempt'] += 1
    return result


def updateCompResult(result: dict) -> str:
    result['attempt'] = 0
    result['ok'] = False
    result['honest'] = True
    result['a'] = 1
    result['b'] = 10
    result['number'] = generateNumber()
    return "Values are updated!"
