from GUI import *
import sys
import numpy as np
import re

def Open_fisrt_field():
    ui.groupBox.setEnabled(False)
    ui.LabelColumns.setEnabled(True)
    ui.LabelRows.setEnabled(True)
    ui.SpinBoxRows.setEnabled(True)
    ui.SpinBoxColumns.setEnabled(True)
    ui.PushButtonCreateMatrix.setEnabled(True)
    prevTextMatrIn = str(ui.LabelMatrixIn.text())
    prevTextMatrInSys = str(ui.LabelMatrixInSys.text())
    prevTextMatrSys = str(ui.LabelMatrixSys.text())
    if createType:
        prevTextMatrIn = prevTextMatrIn.replace('#', 'G')
        #print(prevTextMatrIn[0])
        ui.LabelMatrixIn.setText(prevTextMatrIn)
        prevTextMatrInSys = prevTextMatrInSys.replace('#', 'G')
        ui.LabelMatrixInSys.setText(prevTextMatrInSys)
        prevTextMatrSys = prevTextMatrSys.replace('!', 'H')
        ui.LabelMatrixSys.setText(prevTextMatrSys)
    else:
        prevTextMatrIn = prevTextMatrIn.replace('#', 'H')
        # print(prevTextMatrIn[0])
        ui.LabelMatrixIn.setText(prevTextMatrIn)
        prevTextMatrInSys = prevTextMatrInSys.replace('#', 'H')
        ui.LabelMatrixInSys.setText(prevTextMatrInSys)
        prevTextMatrSys = prevTextMatrSys.replace('!', 'G')
        ui.LabelMatrixSys.setText(prevTextMatrSys)
def Matrix_is_create():
    Open_fisrt_field()
def Matrix_is_test():
    global createType
    createType = False
    Open_fisrt_field()
def Matrix_transformation():
    global rows, columns
    ui.LabelColumns.setEnabled(False)
    ui.LabelRows.setEnabled(False)
    ui.SpinBoxRows.setEnabled(False)
    ui.SpinBoxColumns.setEnabled(False)
    ui.PushButtonCreateMatrix.setEnabled(False)
    ui.PushButtonStart.setEnabled(True)
    ui.LabelMatrixIn.setEnabled(True)
    ui.TableWidgetMatrixIn.setEnabled(True)
    rows = int(ui.SpinBoxRows.value())
    columns = int(ui.SpinBoxColumns.value())
    ui.TableWidgetMatrixIn.setRowCount(rows)
    ui.TableWidgetMatrixIn.setColumnCount(columns)
    ui.TableWidgetMatrixIn.horizontalHeader().setVisible(False)
    ui.TableWidgetMatrixIn.verticalHeader().setVisible(False)
def Select_way_to_work():
    global createType, matrixIn
    ui.PushButtonStart.setEnabled(False)
    ui.LabelLengthCW.setEnabled(True)
    ui.LabelLengthIW.setEnabled(True)
    ui.LabelMatrixInSys.setEnabled(True)
    ui.TableWidgetMatrixInSys.setEnabled(True)
    ui.LabelMatrixSys.setEnabled(True)
    ui.TableWidgetMatrixSys.setEnabled(True)
    ui.LabelTableCW.setEnabled(True)
    ui.TableWidgetTableCW.setEnabled(True)
    ui.LabelTableHWMin.setEnabled(True)
    ui.LabelTableFindEr.setEnabled(True)
    ui.LabelTableCountCorEr.setEnabled(True)
    ui.LabelTableSE.setEnabled(True)
    ui.TableWidgetTableSE.setEnabled(True)
    ui.LabelWordInput.setEnabled(True)
    ui.TextEditWordInput.setEnabled(True)
    ui.PushButtonDecode.setEnabled(True)
    draftMatrix = [[int(ui.TableWidgetMatrixIn.item(row, column).text()) for column in range(columns)] for row in range(rows)]
    matrixIn = np.asarray(draftMatrix)
    if createType: Creation_matrix_way()
    else: Testing_matrix_way()
def Create_table_CW(matrixGSys):
    listTableCW = [[], [], []]
    for digit in range(2 ** k): listTableCW[0].append('0' * (k - len(str(bin(digit))[2:])) + str(bin(digit))[2:])
    for IW in listTableCW[0]:
        indices = [match.start() for match in re.finditer('1', IW)]
        if not indices:
            listTableCW[1].append('0' * matrixGSys.shape[1])
            listTableCW[2].append(0)
        elif len(indices) == 1:
            listTableCW[1].append(''.join(map(str, matrixGSys[int(indices[0]), :])))
            listTableCW[2].append(''.join(map(str, matrixGSys[int(indices[0]), :])).count('1'))
        else:
            iteartionResult = '0' * matrixGSys.shape[1]
            for index in indices:
                iteartionResult = ''.join(map(str, [(ord(current) ^ ord(old)) for current, old in zip(''.join(map(str, matrixGSys[int(index), :])), iteartionResult)]))
            listTableCW[1].append(iteartionResult)
            listTableCW[2].append(iteartionResult.count('1'))
    return listTableCW
def Create_table_SE(matrixHSysT, countCorrectableErrors):
    listTableSE = [[], []]
    digit = 0
    while True:
        currentString = '0' * (n - len(str(bin(digit))[2:])) + str(bin(digit))[2:]
        if currentString.count('1') <= countCorrectableErrors:
            listTableSE[1].append(currentString)
            indices = [match.start() for match in re.finditer('1', currentString)]
            if not indices:
                listTableSE[0].append('0' * matrixHSysT.shape[1])
            elif len(indices) == 1:
                listTableSE[0].append(''.join(map(str, matrixHSysT[int(indices[0]), :])))
            else:
                iteartionResult = '0' * matrixHSysT.shape[1]
                for index in indices:
                    iteartionResult = ''.join(map(str, [(ord(current) ^ ord(old)) for current, old in
                                                        zip(''.join(map(str, matrixHSysT[int(index), :])),
                                                            iteartionResult)]))
                listTableSE[0].append(iteartionResult)
        if currentString[:countCorrectableErrors] == '1' * countCorrectableErrors: break
        digit += 1
    return listTableSE
def General_calculations(matrixGSys, matrixHSys):
    global listTableCW, listTableSE
    listTableCW = Create_table_CW(matrixGSys)
    ui.TableWidgetTableCW.setRowCount(len(listTableCW[0]))
    ui.TableWidgetTableCW.setColumnCount(3)
    ui.TableWidgetTableCW.setHorizontalHeaderLabels(('i', 'C', 'd'))
    ui.TableWidgetTableCW.verticalHeader().setVisible(False)
    for counter in range(len(listTableCW[0])):
        ui.TableWidgetTableCW.setItem(counter, 0, QtWidgets.QTableWidgetItem(str(listTableCW[0][counter])))
        ui.TableWidgetTableCW.setItem(counter, 1, QtWidgets.QTableWidgetItem(str(listTableCW[1][counter])))
        ui.TableWidgetTableCW.setItem(counter, 2, QtWidgets.QTableWidgetItem(str(listTableCW[2][counter])))
    HWMin = min(listTableCW[2][1:])
    HWMinString = str(ui.LabelTableHWMin.text())[:str(ui.LabelTableHWMin.text()).index(' = ') + 3] + str(HWMin) + str(
        ui.LabelTableHWMin.text())[str(ui.LabelTableHWMin.text()).index(' = ') + 3:]
    ui.LabelTableHWMin.setText(HWMinString)
    countDetectableErrors = HWMin - 1
    countDetectableErrorsString = str(ui.LabelTableFindEr.text()) + str(countDetectableErrors)
    ui.LabelTableFindEr.setText(countDetectableErrorsString)
    countCorrectableErrors = 0
    while True:
        if HWMin >= 2 * countCorrectableErrors + 1: countCorrectableErrors += 1
        else:
            countCorrectableErrors -= 1
            break
    countCorrectableErrorsString = str(ui.LabelTableCountCorEr.text()) + str(countCorrectableErrors)
    ui.LabelTableCountCorEr.setText(countCorrectableErrorsString)
    matrixHSysT = matrixHSys.transpose()
    listTableSE = Create_table_SE(matrixHSysT, countCorrectableErrors)
    ui.TableWidgetTableSE.setRowCount(len(listTableSE[0]))
    ui.TableWidgetTableSE.setColumnCount(2)
    ui.TableWidgetTableSE.setHorizontalHeaderLabels(('S', 'e'))
    ui.TableWidgetTableSE.verticalHeader().setVisible(False)
    for counter in range(len(listTableSE[0])):
        ui.TableWidgetTableSE.setItem(counter, 0, QtWidgets.QTableWidgetItem(str(listTableSE[0][counter])))
        ui.TableWidgetTableSE.setItem(counter, 1, QtWidgets.QTableWidgetItem(str(listTableSE[1][counter])))
def Creation_matrix_way():
    global rows, columns, n, k, matrixIn, matrixInSys, matrixSys
    n = columns
    nString = str(ui.LabelLengthCW.text()) + ' ' + str(n)
    k = rows
    kString = str(ui.LabelLengthIW.text()) + ' ' + str(k)
    ui.LabelLengthCW.setText(nString)
    ui.LabelLengthIW.setText(kString)
    matrixInSys = matrixIn.copy()
    matrixI = np.eye(matrixInSys.shape[0])
    counterPos = 0
    for step in range(matrixInSys.shape[0]):
        if np.array_equal(matrixInSys[:, :matrixInSys.shape[0]], matrixI): break
        if np.array_equal(matrixInSys[:, counterPos], matrixI[:, counterPos]):
            counterPos += 1
        else:
            for searchColumn in range(counterPos, matrixInSys.shape[1]):
                if np.array_equal(matrixInSys[:, searchColumn], matrixI[:, counterPos]):
                    matrixInSys[:, searchColumn] = matrixInSys[:, counterPos]
                    matrixInSys[:, counterPos] = matrixI[:, counterPos]
                    counterPos += 1
                    break
    ui.TableWidgetMatrixInSys.setRowCount(rows)
    ui.TableWidgetMatrixInSys.setColumnCount(columns)
    ui.TableWidgetMatrixInSys.horizontalHeader().setVisible(False)
    ui.TableWidgetMatrixInSys.verticalHeader().setVisible(False)
    for row in range(rows):
        for column in range(columns):
            ui.TableWidgetMatrixInSys.setItem(row, column, QtWidgets.QTableWidgetItem(str(matrixInSys[row][column])))
    matrixSys = matrixInSys[:, matrixInSys.shape[0]:].copy().transpose()
    matrixSys = np.concatenate([matrixSys, np.eye(columns - rows)], axis=1).astype('int')
    ui.TableWidgetMatrixSys.setRowCount(columns - rows)
    ui.TableWidgetMatrixSys.setColumnCount(columns)
    ui.TableWidgetMatrixSys.horizontalHeader().setVisible(False)
    ui.TableWidgetMatrixSys.verticalHeader().setVisible(False)
    for row in range(columns - rows):
        for column in range(columns):
            ui.TableWidgetMatrixSys.setItem(row, column, QtWidgets.QTableWidgetItem(str(matrixSys[row][column])))
    General_calculations(matrixInSys, matrixSys)
def Testing_matrix_way():
    global rows, columns, n, k, matrixIn, matrixInSys
    n = columns
    nString = str(ui.LabelLengthCW.text()) + ' ' + str(n)
    k = n - rows
    kString = str(ui.LabelLengthIW.text()) + ' ' + str(k)
    ui.LabelLengthCW.setText(nString)
    ui.LabelLengthIW.setText(kString)
    matrixInSys = matrixIn.copy()
    matrixI = np.eye(matrixIn.shape[0])
    counterPos = 0
    if np.array_equal(matrixInSys[:, -matrixIn.shape[0]:], matrixI): pass
    else:
        if np.array_equal(matrixInSys[:, -matrixInSys.shape[0] - counterPos], matrixI[:, counterPos]): counterPos += 1
        else:
            for searchColumn in range(matrixInSys.shape[1] - matrixInSys.shape[0]):
                if np.array_equal(matrixInSys[:, searchColumn], matrixI[:, counterPos]):
                    matrixInSys[:, searchColumn] = matrixInSys[:, -matrixInSys.shape[0] + counterPos]
                    matrixInSys[:, -matrixInSys.shape[0] + counterPos] = matrixI[:, counterPos]
                    counterPos += 1
    ui.TableWidgetMatrixInSys.setRowCount(rows)
    ui.TableWidgetMatrixInSys.setColumnCount(columns)
    ui.TableWidgetMatrixInSys.horizontalHeader().setVisible(False)
    ui.TableWidgetMatrixInSys.verticalHeader().setVisible(False)
    for row in range(rows):
        for column in range(columns):
            ui.TableWidgetMatrixInSys.setItem(row, column, QtWidgets.QTableWidgetItem(str(matrixInSys[row][column])))
    matrixSys = matrixInSys[:, :-matrixInSys.shape[0]].copy().transpose()
    matrixSys = np.concatenate([np.eye(matrixSys.shape[0]), matrixSys], axis=1).astype('int')
    ui.TableWidgetMatrixSys.setRowCount(k)
    ui.TableWidgetMatrixSys.setColumnCount(columns)
    ui.TableWidgetMatrixSys.horizontalHeader().setVisible(False)
    ui.TableWidgetMatrixSys.verticalHeader().setVisible(False)
    for row in range(k):
        for column in range(columns):
            ui.TableWidgetMatrixSys.setItem(row, column, QtWidgets.QTableWidgetItem(str(matrixSys[row][column])))
    General_calculations(matrixSys, matrixInSys)
def Decoding():
    global listTableSE, listTableCW, matrixSys, createType, matrixInSys
    ui.LabelSyndrom.setEnabled(True)
    ui.LabelErrorVector.setEnabled(True)
    ui.LabelCW.setEnabled(True)
    ui.LabelIW.setEnabled(True)
    if createType: matrixHSysT = matrixSys.copy().transpose()
    else: matrixHSysT = matrixInSys.copy().transpose()
    wordInput = ui.TextEditWordInput.toPlainText()
    indices = [match.start() for match in re.finditer('1', wordInput)]
    if not indices:
        syndrom = '0' * matrixHSysT.shape[1]
    elif len(indices) == 1:
        syndrom = ''.join(map(str, matrixHSysT[int(indices[0]), :]))
    else:
        iteartionResult = '0' * matrixHSysT.shape[1]
        for index in indices:
            iteartionResult = ''.join(map(str, [(ord(current) ^ ord(old)) for current, old in
                                                zip(''.join(map(str, matrixHSysT[int(index), :])), iteartionResult)]))
        syndrom = iteartionResult
    syndromString = 'S = ' + syndrom
    ui.LabelSyndrom.setText(syndromString)
    errorVector = listTableSE[1][listTableSE[0].index(syndrom)]
    ui.LabelErrorVector.setText('e = ' + errorVector)
    CW = ''.join(map(str, [(ord(inputWord) ^ ord(errorVect)) for inputWord, errorVect in zip(wordInput, errorVector)]))
    ui.LabelCW.setText('C = ' + CW)
    IW = listTableCW[0][listTableCW[1].index(CW)]
    ui.LabelIW.setText('i = ' + IW)

createType = True
rows, columns, n, k = 0, 0, 0, 0
matrixIn, matrixInSys = np.array([]), np.array([])
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
ui.RadioButtonCreate.clicked.connect(Matrix_is_create)
ui.RadioButtonTest.clicked.connect(Matrix_is_test)
ui.PushButtonCreateMatrix.clicked.connect(Matrix_transformation)
ui.PushButtonStart.clicked.connect(Select_way_to_work)
ui.PushButtonDecode.clicked.connect(Decoding)
sys.exit(app.exec_())
