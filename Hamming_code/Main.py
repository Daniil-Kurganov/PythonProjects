import math
import random
from PyQt5.QtWidgets import QMessageBox
from GUI import *

def calculation_of_correction_bits(int_n: int, list_positions_of_correction_bits: list, list_code_underword: list, bool_check: bool) -> str:
    '''Вычисление корректирующих битов в кодовых подсловах'''
    # print(list_positions_of_correction_bits)
    if bool_check: int_position_of_error_bit = 0
    for int_position_of_correction_bit in list_positions_of_correction_bits:
        int_current_correction_bit = 0
        for int_position_of_tail_bit in range(int_position_of_correction_bit * 2, int_n, (int_position_of_correction_bit + 1) * 2):
            for int_bit_subblock_position in range (int_position_of_tail_bit - int_position_of_correction_bit, int_position_of_tail_bit + 1):
                if list_code_underword[int_bit_subblock_position][0] != 'b':
                    int_current_correction_bit = int(ord(str(int_current_correction_bit)) ^ ord(str(list_code_underword[int_bit_subblock_position])))
        if not bool_check: list_code_underword[int_position_of_correction_bit] = str(int_current_correction_bit)
        elif int_current_correction_bit: int_position_of_error_bit += int_position_of_correction_bit + 1
    # print(list_code_underword)
    if bool_check:string_output = str(int_position_of_error_bit - 1)
    else: string_output = ''.join(list_code_underword)
    return string_output
def changing_the_bit(string_bit: str) -> str:
    '''Заменяет бит на противоположный'''
    if int(string_bit): return '0'
    else: return '1'
def cutting_code_subword_to_information_word(string_code_underword: str) -> str:
    '''Выбивание корректирующих битов из кодовых подслов и преобразование их в информационные'''
    list_current_information_underword = []
    # print(string_code_underword)
    for int_position_of_bit in range(1, int_n + 1):
        if (int_position_of_bit & (int_position_of_bit - 1) == 0): pass
        else: list_current_information_underword.append(string_code_underword[int_position_of_bit - 1])
    return ''.join(list_current_information_underword)
def starting_the_codec() -> None:
    '''Запуск основного блока программы'''
    global int_n
    int_r = int(ui.SpinBoxR.value())
    if int_r < 2: return
    int_n, int_k = 2 ** int_r - 1, 2 ** int_r - 1 - int_r
    ui.LabelR.setText('r = {}'.format(int_r))
    ui.LabelN.setText('n = {}'.format(int_n))
    ui.LabelK.setText('k = {}'.format(int_k))
    string_input_text_real = ui.TextEditInputText.toPlainText()
    string_input_text_binary = bin(int.from_bytes(string_input_text_real.encode(), 'big'))[2:]
    ui.TextEditOutputBinaryTextIn.setText(string_input_text_binary)
    list_informaion_underwords, list_code_underwords = [], []
    int_count_of_zeros = 0
    if len(string_input_text_binary) > int_k:
        for iteration in range(1, math.ceil(len(string_input_text_binary) / int_k)):
            list_informaion_underwords.append(string_input_text_binary[iteration * int_k - int_k:iteration * int_k])
        if len(string_input_text_binary) % int_k != 0:
            int_count_of_zeros = int_k - (len(string_input_text_binary) - (int_k * (len(string_input_text_binary) // int_k)))
            list_informaion_underwords.append(('0' * int_count_of_zeros) + string_input_text_binary[-(int_k - int_count_of_zeros):])
        else: list_informaion_underwords.append(string_input_text_binary[-int_k:])
    else:
        try:
            int_count_of_zeros = int_k - len(string_input_text_binary)
            list_informaion_underwords.append(('0' * int_count_of_zeros) + string_input_text_binary)
        except:
            message_error = QMessageBox()
            message_error.setIcon(QMessageBox.Critical)
            message_error.setText("Ошибка переполнения памяти.")
            message_error.setInformativeText('Сбавьте обороты...')
            message_error.setWindowTitle("Ошибка!")
            message_error.exec_()
            return 0
    for string_information_underword in list_informaion_underwords:
        list_code_underword, list_positions_of_correction_bits = [], []
        int_posotion_of_bits = 0
        for int_position_of_bit in range(1, int_n + 1):
            if (int_position_of_bit & (int_position_of_bit - 1) == 0):
                list_code_underword.append('b' + str(int_position_of_bit))
                list_positions_of_correction_bits.append(len(list_code_underword) - 1)
            else:
                list_code_underword.append(string_information_underword[int_posotion_of_bits])
                int_posotion_of_bits += 1
        list_code_underwords.append(calculation_of_correction_bits(int_n, list_positions_of_correction_bits, list_code_underword, False))
    ui.TableWidgetCodeSubwordsOrigins.setRowCount(1)
    ui.TableWidgetCodeSubwordsOrigins.setColumnCount(len(list_code_underwords))
    ui.TableWidgetCodeSubwordsOrigins.verticalHeader().setVisible(False)
    ui.TableWidgetCodeSubwordsOrigins.horizontalHeader().setVisible(False)
    for int_counter_iteration in range(len(list_code_underwords)):
        ui.TableWidgetCodeSubwordsOrigins.setItem(0, int_counter_iteration,
                                                  QtWidgets.QTableWidgetItem(str(list_code_underwords[int_counter_iteration])))
    list_informaion_underwords.clear()
    list_code_underwords_with_errors = []
    for string_code_underword in list_code_underwords:
        int_position_of_error = random.randint(0, len(string_code_underword) - 1)
        string_code_underword = (string_code_underword[:int_position_of_error] + changing_the_bit(string_code_underword[int_position_of_error]) +
                                 string_code_underword[int_position_of_error + 1:])
        list_code_underwords_with_errors.append(string_code_underword)
        int_position_of_error = int(calculation_of_correction_bits(int_n, list_positions_of_correction_bits,
                                                                   list(string_code_underword), True))
        string_code_underword = (string_code_underword[:int_position_of_error] + changing_the_bit(string_code_underword[int_position_of_error]) +
                                 string_code_underword[int_position_of_error + 1:])
        string_current_information_underword = cutting_code_subword_to_information_word(string_code_underword)
        list_informaion_underwords.append(string_current_information_underword)
    ui.TableWidgetCodeSubwordsErrors.setRowCount(1)
    ui.TableWidgetCodeSubwordsErrors.setColumnCount(len(list_code_underwords_with_errors))
    ui.TableWidgetCodeSubwordsErrors.verticalHeader().setVisible(False)
    ui.TableWidgetCodeSubwordsErrors.horizontalHeader().setVisible(False)
    for int_counter_iteration in range(len(list_code_underwords_with_errors)):
        ui.TableWidgetCodeSubwordsErrors.setItem(0, int_counter_iteration,
                                                  QtWidgets.QTableWidgetItem(str(list_code_underwords_with_errors[int_counter_iteration])))
    if int_count_of_zeros > 0: list_informaion_underwords[-1] = list_informaion_underwords[-1][int_count_of_zeros:]
    string_output_text_binary = ''.join(list_informaion_underwords)
    ui.TextEditOutputBinaryTextOut.setText(string_output_text_binary)
    string_output_text = int(string_output_text_binary, 2).to_bytes((int(string_output_text_binary, 2).bit_length() + 7) // 8,
                                                                    'big').decode()
    ui.TextEditOutputText.setText(string_output_text)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
ui.PushButtonStart.clicked.connect(starting_the_codec)
sys.exit(app.exec_())