

def objectsEqual(first, second):
    if type(first) != type(second):
        return False
    if isinstance(first, str):
        return first == second
    if isinstance(first, int):
        return first == second
    if isinstance(first, list):
        return listEqual(first, second)

def _numTimesItemIsInList(item, list):
    ret = 0
    for x in list:
        if objectsEqual(x,item):
            ret += 1
    return ret

def _makeHashable(item):
    if isinstance(item, list):
        return "LIS:" + str(item) #not great but good enough
    return item

def listEqual(first, second):
    if len(first) != len(second):
        return False
    data = {}
    for x in first:
        data[_makeHashable(x)] = {
            "item": x,
            "times_in_first": 0,
            "times_in_second": 0
        }
    for x in second:
        data[_makeHashable(x)] = {
            "item": x,
            "times_in_first": 0,
            "times_in_second": 0
        }

    for x in data:
        data[x]["times_in_first"] = _numTimesItemIsInList(data[x]["item"],first)
        data[x]["times_in_second"] = _numTimesItemIsInList(data[x]["item"],second)
        if data[x]["times_in_first"] != data[x]["times_in_second"]:
            return False

    return True
