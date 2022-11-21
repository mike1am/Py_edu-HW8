from model import formDepOut, formEmplOut, addImpData, prepExpData, addDep, addEmpl,\
    modifyEmplData, delEmpls, delDep
from ui import menu, showDeps, showEmployees, inputDeps, inputImpFilename, inputExpFileName,\
    inputDepName, inputEmplData, errorMsg, getNewEmplData, requestToDel
from file_ops import readDataFiles, writeDataFiles
from imp_exp import parseCSVData, convertCSVData


def prepWriteData(dataToWrite):
    if not dataToWrite[0] and not dataToWrite[1]:
        errorMsg("Нет данных для экспорта.")
        return
    fNames = inputExpFileName()
    if not fNames: return ""
    return {
        'fNames': fNames,
        'fData': dataToWrite
    }


# сохранение данных при выходе
def prepSaveData(dataToWrite):
    return {
        'fNames': ["departments.bd", "employees.bd"],
        'fData': dataToWrite
    }


def exitProgram(_=None):
    exit()


ACTIONS = {
    1: {'desc': "Вывести список отделов", 'handlers': [formDepOut, showDeps]},
    2: {'desc': "Вывести список сотрудников отделов", 'handlers': [inputDeps, formEmplOut, showEmployees]},
    3: {'desc': "Добавить отдел", 'handlers': [inputDepName, addDep]},
    4: {'desc': "Добавить сотрудника", 'handlers': [inputEmplData, addEmpl]},
    5: {'desc': "Редактировать данные сотрудника", 'handlers': [inputEmplData, formEmplOut, showEmployees,
        getNewEmplData, modifyEmplData]},
    6: {'desc': "Уволить сотрудников", 'handlers': [inputEmplData, formEmplOut, showEmployees, requestToDel, delEmpls]},
    7: {'desc': "Удалить отдел (отдел не должен содержать сотрудников)", 'handlers': [inputDepName, delDep]},
    8: {'desc': "Экспорт отделов в CSV", 'handlers': [inputDeps, prepExpData, convertCSVData, prepWriteData, writeDataFiles]},
    9: {'desc': "Импорт данных из CSV", 'handlers': [inputImpFilename, readDataFiles, parseCSVData, addImpData]},
    0: {'desc': "Выход", 'handlers': [prepExpData, convertCSVData, prepSaveData, writeDataFiles, exitProgram]},
}    


def mainLoop():
    while True:
        operNum = menu()
        resData = None
        for action in ACTIONS[operNum]['handlers']:
            resData = action(resData)
            if not resData:
                break
