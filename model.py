# Хранилища данных - списки словарей
# departments:
# id - уникальный ид. отдела
# name - наименование отдела
# nbgId - ид. руководителя
# employees:
# id - уникальный ид. сотрудника
# fio - ФИО сотрудника
# depId - ид. отдела 
departments = []
employees = []


# Возвращает выборку из списка словарей по заданным кретериям
# mask - словарь, содержаний поля для поиска
# compareFunc - функция сравнения элементов маски и словаря
def getDataList(mask, dataList, compareFunc=lambda maskVal, dictVal: maskVal == dictVal):
    resList = []
    for objDict in dataList:
        matchFl = True
        for key, val in mask.items():
            if not compareFunc(val, objDict[key]):
                matchFl = False
                break
        if matchFl: resList.append(objDict)

    return resList


def formDepOut(_=None):
    outList = []
    for dep in departments:
        mngList = getDataList({'id': dep['mngId']}, employees)
        outList.append({
            'name': dep['name'],
            'mng_fio': mngList[0]['fio'] if len(mngList) else ""
        })
    if not outList: outList = ({}) # для вывода сообщения
    return outList


def formEmplOut(emplData=None):
    if not emplData: emplData = ("", "")
    
    # Формирование списка отделов в соответсвие с заданным именем
    if not (depList := getDataList({'name': emplData[0]}, departments,
            lambda depName, name: depName.lower() in name.lower())):
        return ({})

    # Формирование списка сотрудников, входящих в список отделов и соответсвующих маске (соотв. ФИО и принадлежность к отделу)
    # если список отделов не задан, выбираются сотрудники только по имени
    if emplData[0]:
        emplList = []
        for dep in depList:
            emplList += getDataList({'fio': emplData[1], 'depId': dep['id']}, employees,
            lambda maskEl, emplEl: maskEl == emplEl if isinstance(emplEl, int)
                    else maskEl.lower() in emplEl.lower())
    else:
        emplList = getDataList({'fio': emplData[1]}, employees,
            lambda maskEl, emplEl: maskEl.lower() in emplEl.lower())

    # Формирование выходного списка сотрудников с номерами отделов
    outList = []
    for empl in emplList:
        depList = getDataList({'id': empl['depId']}, departments)
        outList.append({
                'id': empl['id'], # для последующего редактирования
                'fio': empl['fio'],
                'depName': depList[0]['name'] if len(depList) else ""
        })
    
    if not outList: outList = ({}) # для вывода сообщения
    return outList


# data - список из 2х эл. - [0] - список отделов, [1] - список сотрудников
def addImpData(data):
    storeLists = (departments, employees)
    
    if data[0]: departments.clear() # импорт только в режиме полного замещения
    if data[1]: employees.clear()
    
    for ind, dataList in enumerate(data):
        for item in dataList:
            for key in item.keys():
                if key[-2:].lower() == "id": item[key] = int(item[key]) # преобразование id в int
            
            storeLists[ind].append(item)


# Формирует список из 2х списков для экспорта - отделы и сотрудники
# expNames - кортеж из 2х строк - имя отдела и имя сотрудника
# используется только имя отдела, как маска поиска
def prepExpData(expNames=None):
    if not expNames: expNames = ("", "") # экспорт всех данных
    depList = getDataList({'name': expNames[0]}, departments,
            lambda depName, name: depName.lower() in name.lower())
    if expNames[0]:
        emplList = []
        for depId in [dep['id'] for dep in depList]:
            emplList += getDataList({'depId': depId}, employees)
    else:
        emplList = employees # если отдел не указан, экспорт всех сотрудников
    return [depList, emplList]


def addDep(depName):
    existDeps = getDataList({'name': depName}, departments)
    if not existDeps:
        if departments:
            newId = max([dep['id'] for dep in departments]) + 1
        else: newId = 1
       
        departments.append({'id': newId, 'name': depName, 'mngId': 0})


def addEmpl(emplData):
    if employees:
        newId = max([empl['id'] for empl in employees]) + 1
    else: newId = 1
    depList = getDataList({'name': emplData[0]}, departments)
    employees.append({
        'id': newId,
        'fio': emplData[1],
        'depId': depList[0]['id'] if depList else 0
    })


def modifyEmplData(emplDic):
    empl = getDataList({'id': emplDic['id']}, employees)[0] # возможно, понадобится проверка на длину возвр. списка
    empl['fio'] = emplDic['fio']
    
    # поиск подходящих отделов и присваивание id, если таковой найден и единственный
    depList = getDataList({'name': emplDic['depName']}, departments,
            lambda depName, name: depName.lower() in name.lower())
    if len(depList) == 1:
        empl['depID'] = depList[0]['id']

    # поиск отдела по depId и установка id руководителя (если задан)
    if empl['depId'] and emplDic['mngFl']:
        getDataList({'id': empl['depId']}, departments)[0]['mngId'] = empl['id']


def delEmpls(emplList):
    for emplDic in emplList:
        # Обнуление mngId, если сотрудник - руководитель
        if (mngList := getDataList({'mngId': emplDic['id']}, departments)):
            mngList[0]['mngId'] = 0
        
        for emplInd, empl in enumerate(employees):
            if empl['id'] == emplDic['id']:
                employees.pop(emplInd)
    

def delDep(depName):
    depList = getDataList({'name': depName}, departments,\
            lambda depName, name: depName.lower() == name.lower())
    if len(depList) == 1 and not getDataList({'depId': depList[0]['id']}, employees): # отдел единственный и без сотрудников
        for depInd, dep in enumerate(departments):
            if dep['id'] == depList[0]['id']:
                departments.pop(depInd)
