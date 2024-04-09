import numpy as np
import re

# matrixInSys = np.array([[1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 1, 1, 0, 0], [0, 1, 1, 0, 0, 1, 1]])
# k, n = 4, 7
# listTableCW = [[], [], []]
# print(matrixInSys, '\n{:*^60}'.format('*'))
# matrixI = np.eye(matrixInSys.shape[0])
# counterPos = 0
# if np.array_equal(matrixInSys[:, -matrixInSys.shape[0]:], matrixI): print('Alright! let`s go')
# else:
#     for step in range(matrixInSys.shape[0]):
#         if np.array_equal(matrixInSys[:, -matrixInSys.shape[0] - counterPos], matrixI[:, counterPos]): counterPos += 1
#         else:
#             for searchColumn in range(matrixInSys.shape[1] - matrixInSys.shape[0]):
#                 if np.array_equal(matrixInSys[:, searchColumn], matrixI[:, counterPos]):
#                     matrixInSys[:, searchColumn] = matrixInSys[:, -matrixInSys.shape[0] + counterPos]
#                     matrixInSys[:, -matrixInSys.shape[0] + counterPos] = matrixI[:, counterPos]
#                     counterPos += 1
# print(matrixInSys, '\n{:*^120}'.format('*'))
# matrixSys = matrixInSys[:, :-matrixInSys.shape[0]].copy().transpose()
# matrixSys = np.concatenate([np.eye(matrixSys.shape[0]), matrixSys], axis = 1).astype('int')
# print(matrixSys, '\n{:*^120}'.format('*'))
# for digit in range(2 ** k): listTableCW[0].append('0' * (k - len(str(bin(digit))[2:])) + str(bin(digit))[2:])
# print(listTableCW, '\n{:*^120}'.format('*'))
# for IW in listTableCW[0]:
#     indices = [match.start() for match in re.finditer('1', IW)]
#     if not indices:
#         listTableCW[1].append('0' * matrixSys.shape[1])
#         listTableCW[2].append(0)
#     elif len(indices) == 1:
#         listTableCW[1].append(''.join(map(str, matrixSys[int(indices[0]), :])))
#         listTableCW[2].append(''.join(map(str, matrixSys[int(indices[0]), :])).count('1'))
#     else:
#         iteartionResult = '0' * matrixSys.shape[1]
#         for index in indices:
#             iteartionResult = ''.join(map(str, [(ord(current) ^ ord(old)) for current, old in zip(''.join(map(str, matrixSys[int(index), :])), iteartionResult)]))
#         listTableCW[1].append(iteartionResult)
#         listTableCW[2].append(iteartionResult.count('1'))
# print(listTableCW[0])
# print(listTableCW[1])
# print(listTableCW[2])
# print(min(listTableCW[2][1:]), '\n{:*^120}'.format('*'))
# matrixInSysT = matrixInSys.transpose()
# print(matrixInSysT, '\n{:*^120}'.format('*'))
# listTableSE = [[], []]
# countCorrectableErrors = 1
# digit = 0
# while True:
#     currentString = '0' * (n - len(str(bin(digit))[2:])) + str(bin(digit))[2:]
#     if currentString.count('1') <= countCorrectableErrors:
#         listTableSE[1].append(currentString)
#         indices = [match.start() for match in re.finditer('1', currentString)]
#         if not indices: listTableSE[0].append('0' * matrixInSysT.shape[1])
#         elif len(indices) == 1: listTableSE[0].append(''.join(map(str, matrixInSysT[int(indices[0]), :])))
#         else:
#             iteartionResult = '0' * matrixInSysT.shape[1]
#             for index in indices:
#                 iteartionResult = ''.join(map(str, [(ord(current) ^ ord(old)) for current, old in zip(''.join(map(str, matrixInSysT[int(index), :])), iteartionResult)]))
#             listTableSE[0].append(iteartionResult)
#     if currentString[:countCorrectableErrors] == '1' * countCorrectableErrors: break
#     digit += 1
# print(listTableSE, '\n{:*^120}'.format('*'))
# wordInput, syndrom = '1100110', ''
# indices = [match.start() for match in re.finditer('1', wordInput)]
# if not indices: syndrom = '0' * matrixInSysT.shape[1]
# elif len(indices) == 1: syndrom = ''.join(map(str, matrixInSysT[int(indices[0]), :]))
# else:
#     iteartionResult = '0' * matrixInSysT.shape[1]
#     for index in indices:
        iteartionResult = ''.join(map(str, [(ord(current) ^ ord(old)) for current, old in zip(''.join(map(str, matrixInSysT[int(index), :])), iteartionResult)]))
#     syndrom = iteartionResult
# print(syndrom, '\n{:*^120}'.format('*'))
# errorVector = listTableSE[1][listTableSE[0].index(syndrom)]
# print(errorVector, '\n{:*^120}'.format('*'))
# CW = ''.join(map(str, [(ord(inputWord) ^ ord(errorVect)) for inputWord, errorVect in zip(wordInput, errorVector)]))
# print(CW, '\n{:*^120}'.format('*'))
# IW = listTableCW[0][listTableCW[1].index(CW)]
# print(IW)

# Порождающая
matrixIn = np.array([[1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 1, 1, 0, 0], [0, 1, 1, 0, 0, 1, 1]])
rows, columns = 3, 7
print(matrixIn, '\n{:*^120}'.format('*'))
matrixInSys = matrixIn.copy()
matrixI = np.eye(matrixInSys.shape[0])
counterPos = 0
for step in range(matrixInSys.shape[0]):
    if np.array_equal(matrixInSys[:, :matrixInSys.shape[0]], matrixI): break
    if np.array_equal(matrixInSys[:, counterPos], matrixI[:, counterPos]): counterPos += 1
    else:
        for searchColumn in range(counterPos, matrixInSys.shape[1]):
            if np.array_equal(matrixInSys[:, searchColumn], matrixI[:, counterPos]):
                matrixInSys[:, searchColumn] = matrixInSys[:, counterPos]
                matrixInSys[:, counterPos] = matrixI[:, counterPos]
                counterPos += 1
                break
print(matrixInSys, '\n{:*^120}'.format('*'))
matrixSys = matrixInSys[:, matrixInSys.shape[0]:].copy().transpose()
matrixSys = np.concatenate([matrixSys, np.eye(columns - rows)], axis = 1).astype('int')
print(matrixSys, '\n{:*^120}'.format('*'))