from ui import errorMsg

def writeFile(expList, fName):
    try:
        with open(fName, "w") as file:
            for fileStr in expList:
                file.write(fileStr + "\n")
    except IOError:
        errorMsg("Ошибка записи в файл.")


# Разворачивает структуру expData для записи файлов экспорта
def writeDataFiles(expData):
    for fName, expList in zip(expData['fNames'], expData['fData']):
        writeFile(expList, fName)
    return ({}) # для вызова при выходе из программы (сохранение)


def readFile(fName):
    readList = []
    try:
        with open(fName, "r") as file:
            for fileStr in file:
                readList.append(fileStr.rstrip("\n"))
    except IOError:
        errorMsg("Ошибка чтения из файла.")
    finally:
        return readList


# Читает 2 файла в соответствии с кортежем из 2х имён файлов (отделов и сотрудников)
# возвращает список из 2х списков строк
def readDataFiles(fList):
    resList = []
    for fName in fList:
        readList = readFile(fName)
        if readList:
            resList.append(readFile(fName))
    return resList
