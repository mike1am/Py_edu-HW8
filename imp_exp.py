def parseCSVData(data):
    resList = []
    for sList in data:
        resList.append(parseCSV(sList))
    return resList


def parseCSV(sList):
    resList = []
    keys = sList[0].split(";")
    sList = sList[1:]
    for impStr in sList:
        if impStr != "":
            resList.append({key: value for key, value in zip(keys, impStr.split(";"))})
    return resList


def convertCSVData(data):
    resList = []
    for dataList in data:
        resList.append(convertCSV(dataList))
    return resList


def convertCSV(dataList):
    if not dataList: return []
    resList = [";".join(dataList[0].keys())]
    for dataItem in dataList:
        resList.append(";".join([str(val) if isinstance(val, int) else val for val in dataItem.values()]))
    return resList
