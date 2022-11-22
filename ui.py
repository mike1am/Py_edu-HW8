from os.path import isfile
import controller


# chkFunc - функция, осуществляющая проверку ввода, если возвращает False - ввод некорректен
# возвращает введённую строку
def userInput(prompt, chkFunc=lambda _: True, errMsg="Некорректный ввод."):
    while True:
        try:
            uInput = input(prompt)
            if not chkFunc(uInput):
                raise ValueError
        except ValueError:
            print(errMsg)
        else:
            return uInput


def userBinChoice (prompt):
    uAnswer = userInput(prompt + " [Y/N] ",
            lambda uInput: len(uInput) == 1 and uInput in "YNynДНдн")
    return uAnswer in "YyДд"


def errorMsg(msg):
    print(f"!!! {msg}")


# Возвращает список именов файлов
def inputImpFilename(_=None):
    fName = userInput("Введите имя файла для импорта (Enter - отказ): ",
            lambda uInp:
                not uInp or isfile(uInp + "_dep.csv") and isfile(uInp + "_emp.csv"), # упрощённая проверка - для ДЗ
            "Не найден подходящий файл для импорта.")
    if fName == "": return ""
    return (fName + "_dep.csv", fName + "_emp.csv")


def inputExpFileName(_=None):
    fName = userInput("Введите имя файла для экспорта (Enter - отказ): ")
    if fName == "": return ""
    return (fName + "_dep.csv", fName + "_emp.csv")


def inputDeps(_=None):
    depName = userInput("Введите наименование отдела или его часть (Enter - все): ")
    return (depName, "")


def inputDepName(_=None): # для создания и удаления одела
    return userInput("Введите наименование отдела: ")


def inputEmplData(_=None):
    emplFio = userInput("Введите ФИО сотрудника: ")
    if not emplFio: return
    emplDep = userInput("Введите отдел сотрудника: ")
    return (emplDep, emplFio)


def menu():
    print()
    for itemNum, itemDict in controller.ACTIONS.items():
        print(f"{itemNum}. {itemDict['desc']}")
    return int(userInput("Введите пункт меню: ", 
            lambda uInp: 0 <= int(uInp) < len(controller.ACTIONS)))


def showDeps(depList):
    if depList[0] != {}:
        for dep in depList:
            print(f"\nНаименование: {dep['name']}\nРуководитель: {dep['mng_fio']}")
    else:
        print("\nСписок отделов пуст.")


def showEmployees(emplList):
    if emplList[0] != {}:
        for empl in emplList:
            print(f"\nФИО: {empl['fio']}\nОтдел: {empl['depName']}")

        return emplList # если предстоит редактирование контакта
    else:
        print("\nСотрудники не найдены")


def getEmplData(emplList):
    if len(emplList) != 1:
        errorMsg("Данные сотрудников можно редактировать только по одному.")
        return
    
    newData = inputEmplData()
    if newData[1]: emplList[0]['fio'] = newData[1]
    if newData[0]: emplList[0]['depName'] = newData[0]
    
    if userBinChoice("Сделать сотрудника руководителем отдела?"):
        emplList[0]['mngFl'] = True
    else: emplList[0]['mngFl'] = False

    return (emplList[0])


def requestToDel(emplList):
    if userBinChoice("Вы действительно хотите уволить этих сотрудников?"):
        return emplList