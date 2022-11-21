from controller import mainLoop
from file_ops import readDataFiles
from imp_exp import parseCSVData
from model import addImpData

if impList := readDataFiles(["departments.bd", "employees.bd"]):
    addImpData(parseCSVData(impList))

mainLoop()