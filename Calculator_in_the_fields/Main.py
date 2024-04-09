import sys
from PyQt5.QtWidgets import QMessageBox
from GUI import *

def wrong_input_data_error(string_error_text_key: str) -> None:
    '''Вывод ошибок о некорректном вводе данных'''
    dictionary_error_texts = {'wrong_message': 'Проверьте корректность вводимого выражения.',
                              'wrong_field_dimension': 'Введённая размерность поля не является простым числом.',
                              'division_by_zero': 'В выражении присутствует операция деления на 0.',
                              'division_by_one': 'В выражении присутствует деление на 1.'}
    message_error = QMessageBox()
    message_error.setIcon(QMessageBox.Critical)
    message_error.setText("Ошибка: некорректные входные данные.")
    message_error.setInformativeText(dictionary_error_texts[string_error_text_key] + ' Для уточнения правил ввода, обратитесь к документации' +
                                     ' и повторите попытку ввода.')
    message_error.setWindowTitle("Ошибка!")
    message_error.exec_()
    ui.TextEditOutputResults.clear()
    return 0
def checking_a_number_for_primality(int_number: int) -> bool:
    '''Проверка числа на простоту'''
    if int_number % 2 == 0:
        return int_number == 2
    int_divider = 3
    while int_divider * int_divider <= int_number and int_number % int_divider != 0:
        int_divider += 2
    return int_divider * int_divider > int_number
def number_to_field_converter(int_number: int) -> int:
    '''Перевод числа в заданное поле'''
    global int_field_dimension
    if int_number < 0:
        if int_number == -int_field_dimension: return 0
        else: return int_number + ((abs(int_number) // int_field_dimension) + 1) * int_field_dimension
    elif int_number < int_field_dimension - 1: return int_number
    return int_number - int_field_dimension * (int_number // int_field_dimension)
def finding_the_inverse_of_a_number(int_number: int) -> int or str:
    '''Нахождение обратного к числу'''
    global int_field_dimension
    int_number = number_to_field_converter(int_number)
    if int_number == 1:
        wrong_input_data_error('division_by_one')
        return 'error'
    list_straight_stroke = [[None, int_field_dimension, None, int_number]]
    while True:
        current_operation_list = [list_straight_stroke[-1][1], list_straight_stroke[-1][3]]
        current_operation_list.append(current_operation_list[0] // current_operation_list[1])
        current_operation_list.append(current_operation_list[0] - current_operation_list[1] * current_operation_list[-1])
        list_straight_stroke.append(current_operation_list)
        if list_straight_stroke[-1][-1] == 1: break
    list_straight_stroke.pop(0)
    list_reverse_stroke = [[list_straight_stroke[-1][0], 1], [list_straight_stroke[-1][1], -list_straight_stroke[-1][2]]]
    for oper in range(len(list_straight_stroke) - 2, -1, -1):
        list_indexes_of_current_remaining = []
        int_current_remaining = list_straight_stroke[oper][3]
        for int_index_list_number in range(len(list_reverse_stroke)):
            if int_current_remaining in list_reverse_stroke[int_index_list_number]:
                if not list_indexes_of_current_remaining: list_indexes_of_current_remaining.append(int_index_list_number)
                else: list_indexes_of_current_remaining.append(int_index_list_number + 1)
        list_current_replacement = [[list_straight_stroke[oper][0], 1],
                                    [list_straight_stroke[oper][1], -list_straight_stroke[oper][2]]]
        for int_index_current_remainig in list_indexes_of_current_remaining:
            list_current_replacement_copy = []
            list_current_replacement_copy.append([list_current_replacement[0][0], list_reverse_stroke[int_index_current_remainig][1]])
            list_current_replacement_copy.append([list_current_replacement[1][0], list_current_replacement[1][1] *
                                                  list_reverse_stroke[int_index_current_remainig][1]])
            list_reverse_stroke[int_index_current_remainig] = list_current_replacement_copy[0]
            list_reverse_stroke.insert(int_index_current_remainig + 1, list_current_replacement_copy[1])
    int_field_dimension_coefficient, int_reverse_number = 0, 0
    for list_number in list_reverse_stroke:
        if list_number[0] == int_field_dimension:
            int_field_dimension_coefficient += list_number[1]
        else:
            int_reverse_number += list_number[1]
    return number_to_field_converter(int_reverse_number)
def performing_operations(string_operation_type, int_first_number: int, int_second_number: int) -> int or str:
    '''Выполнение операци с числами в зависимости от типа'''
    if string_operation_type == '**' and int_second_number == -1: return finding_the_inverse_of_a_number(
        int_first_number)
    elif not string_operation_type in ['/']:
        return number_to_field_converter(int(eval(str(number_to_field_converter(int_first_number))
                                                  + string_operation_type + str(number_to_field_converter(int_second_number)))))
    elif int_second_number == 0 or number_to_field_converter(int_second_number) == 0:
        wrong_input_data_error('division_by_zero')
        return 'error'
    try: return number_to_field_converter(int_first_number * finding_the_inverse_of_a_number(int_second_number))
    except: return 'error'
def programm_launch() -> None:
    '''Начало работы программы'''
    global int_field_dimension
    ui.TextEditOutputResults.clear()
    list_input_expression = ui.TextEditInputMessage.toPlainText().split()
    if len(list_input_expression) % 2 == 0 or len(list_input_expression) == 1:
        wrong_input_data_error('wrong_message')
        return 0
    for int_index_number in range(1, len(list_input_expression), 2):
        if list_input_expression[int_index_number] not in ['**', '*', '/', '+', '-']:
            wrong_input_data_error('wrong_message')
            return 0
    try:
        for int_index_number in range(0, len(list_input_expression), 2):
            if list_input_expression[int_index_number][0] == '0':
                wrong_input_data_error('wrong_message')
                return 0
            elif isinstance(int(list_input_expression[int_index_number]), int): pass
    except:
        wrong_input_data_error('wrong_message')
        return 0
    int_field_dimension = int(ui.SpinBoxFieldDimension.value())
    if not checking_a_number_for_primality(int_field_dimension):
        wrong_input_data_error('wrong_field_dimension')
        return 0
    list_operation_indices = []
    list_input_expression_reverse = list_input_expression.copy()
    list_input_expression_reverse.reverse()
    for int_index, element in enumerate(list_input_expression_reverse):
        if element in ['**']: list_operation_indices.append(len(list_input_expression_reverse) - int_index - 1)
    for int_index, element in enumerate(list_input_expression):
        if element in ['*', '/', ]: list_operation_indices.append(int_index)
    for int_index, element in enumerate(list_input_expression):
        if element in ['+', '-']: list_operation_indices.append(int_index)
    for int_operation_index in range(len(list_operation_indices)):
        for int_current_operation_index in range(int_operation_index + 1, len(list_operation_indices)):
            if list_operation_indices[int_current_operation_index] > list_operation_indices[int_operation_index]:
                list_operation_indices[int_current_operation_index] -= 2
    for int_index_of_operation_index in list_operation_indices:
        int_current_result = performing_operations(
            list_input_expression[int_index_of_operation_index],
            int(list_input_expression.pop(int_index_of_operation_index - 1)),
            int(list_input_expression.pop(int_index_of_operation_index)))
        if int_current_result == 'error': return 0
        list_input_expression[int_index_of_operation_index - 1] = str(int_current_result)
        if len(list_input_expression) > 1:
            ui.TextEditOutputResults.append('Текущий результат выполнения операции: '+ ' '.join(list_input_expression))
    ui.TextEditOutputResults.append('Окончательный результат: ' + str(list_input_expression[0]))
def get_tutorial_information() -> None:
    '''Вывод правил использования программы'''
    with open('Tutorial.txt', 'r', encoding='utf-8') as file_tutorial:
        string_tutorial_content = file_tutorial.read()
        message_tutorial = QMessageBox()
        message_tutorial.setIcon(QMessageBox.Information)
        message_tutorial.setText('Правила ввода данных и использования калькулятора.')
        message_tutorial.setInformativeText(string_tutorial_content)
        message_tutorial.setWindowTitle("Правила ввода данных.")
        message_tutorial.exec_()
        return 0

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
ui.PushButtonStart.clicked.connect(programm_launch)
ui.PushButtonGetTutorial.clicked.connect(get_tutorial_information)
sys.exit(app.exec_())