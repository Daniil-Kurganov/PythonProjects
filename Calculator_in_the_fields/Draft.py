def number_to_field_converter(int_number: int) -> int:
    '''Перевод числа в заданное поле'''
    global int_field_dimension
    if int_number < 0: return int_field_dimension + int_number
    elif int_number < int_field_dimension - 1: return int_number
    return int_number - int_field_dimension * (int_number // int_field_dimension)
def finding_the_inverse_of_a_number(int_number: int) -> int:
    '''Нахождение обратного к числу'''
    global int_field_dimension
    int_number = number_to_field_converter(int_number)
    list_straight_stroke = [[None, int_field_dimension, None, int_number]]
    while True:
        current_operation_list = [list_straight_stroke[-1][1], list_straight_stroke[-1][3]]
        current_operation_list.append(current_operation_list[0] // current_operation_list[1])
        current_operation_list.append(current_operation_list[0] - current_operation_list[1] * current_operation_list[-1])
        list_straight_stroke.append(current_operation_list)
        print(list_straight_stroke)
        if list_straight_stroke[-1][-1] == 1: break
    list_straight_stroke.pop(0)
    print(list_straight_stroke)
    list_reverse_stroke = [[list_straight_stroke[-1][0], 1], [list_straight_stroke[-1][1], -list_straight_stroke[-1][2]]]
    for oper in range(len(list_straight_stroke) - 2, -1, -1):
        print('Список до начала текущих изменений:', list_reverse_stroke)
        list_indexes_of_current_remaining = []
        int_current_remaining = list_straight_stroke[oper][3]
        print('Заменяемый остаток:', int_current_remaining)
        for int_index_list_number in range(len(list_reverse_stroke)):
            if int_current_remaining in list_reverse_stroke[int_index_list_number]:
                if not list_indexes_of_current_remaining: list_indexes_of_current_remaining.append(int_index_list_number)
                else: list_indexes_of_current_remaining.append(int_index_list_number + 1)
            # if len(list_indexes_of_current_remaining) > 1: list_indexes_of_current_remaining[-1] += 1
        print('Индексы итерации:', list_indexes_of_current_remaining)
        list_current_replacement = [[list_straight_stroke[oper][0], 1],
                                    [list_straight_stroke[oper][1], -list_straight_stroke[oper][2]]]
        print('Подсписок изменений:', list_current_replacement)
        for int_index_current_remainig in list_indexes_of_current_remaining:
            list_current_replacement_copy = []
            list_current_replacement_copy.append([list_current_replacement[0][0], list_reverse_stroke[int_index_current_remainig][1]])
            list_current_replacement_copy.append([list_current_replacement[1][0], list_current_replacement[1][1] *
                                                  list_reverse_stroke[int_index_current_remainig][1]])
            list_reverse_stroke[int_index_current_remainig] = list_current_replacement_copy[0]
            list_reverse_stroke.insert(int_index_current_remainig + 1, list_current_replacement_copy[1])
            print('Список оборатного хода, после текущего изменения:', list_reverse_stroke)
        print('{:*^120}'.format('*'))
    int_field_dimension_coefficient, int_reverse_number = 0, 0
    for list_number in list_reverse_stroke:
        if list_number[0] == int_field_dimension:
            int_field_dimension_coefficient += list_number[1]
        else:
            int_reverse_number += list_number[1]
    if int_field_dimension * int_field_dimension_coefficient - int_number * int_reverse_number:
        print('Нахождение обратного элемента прошло успешно.')
    return number_to_field_converter(int_reverse_number)
def performing_operations(string_operation_type, int_first_number: int, int_second_number: int) -> int:
    '''Выполнение операци с числами в зависимости от типа'''
    if string_operation_type == '**' and int_second_number == -1: return finding_the_inverse_of_a_number(
        int_first_number)
    elif not string_operation_type in ['/', ':']:
        return number_to_field_converter(int(eval(str(number_to_field_converter(int_first_number))
                                                  + string_operation_type + str(number_to_field_converter(int_second_number)))))
    elif int_second_number == 0 or number_to_field_converter(int_second_number) == 0:
        # message_error = QMessageBox()
        # message_error.setIcon(QMessageBox.Critical)
        # message_error.setText("Ошибка переполнения памяти.")
        # message_error.setInformativeText('Сбавьте обороты...')
        # message_error.setWindowTitle("Ошибка!")
        # message_error.exec_()
        print('Деление на 0 запрещено!')
        return 0
    return number_to_field_converter(int_first_number * finding_the_inverse_of_a_number(int_second_number))
def checking_a_number_for_primality(int_number: int) -> bool:
    '''Проверка числа на простоту'''
    if int_number % 2 == 0:
        return int_number == 2
    int_divider = 3
    while int_divider * int_divider <= int_number and int_number % int_divider != 0:
        int_divider += 2
    return int_divider * int_divider > int_number
def wrong_message_exit() -> None:
    '''Завершает работу программы в связи с неверным вводом выражения'''
    print('Введно неверное сообщение.')
    exit()

list_input_expression = input('Введите выражение, вписывая операции через пробел (возведение в степень - "**" / "^"): ').split()
if len(list_input_expression) % 2 == 0: wrong_message_exit()
for int_index_number in range(0, len(list_input_expression), 2):
    if list_input_expression[int_index_number] not in ['**', '*', '/', '+', '-']: wrong_message_exit()
try:
    for int_index_number in range(1, len(list_input_expression), 2):
        if isinstance(int(list_input_expression[int_index_number]), int): pass
except: wrong_message_exit()
int_field_dimension = int(input('Введите размерность поля: ')) # > 2
if int_field_dimension < 1 or not checking_a_number_for_primality(int_field_dimension):
    print('Введена неверная размерность поля.')
    exit()
re_string_null_element, re_string_int = '^0.+', '^[1-9]\d*$'
# regul_stepen = r'(^[1-9]\d*(\**|\^)([1-9]\d*)+$)'
list_operation_indices = []
list_input_expression_reverse = list_input_expression.copy()
list_input_expression_reverse.reverse()
for int_index, element in enumerate(list_input_expression_reverse):
    if element in ['**']: list_operation_indices.append(len(list_input_expression_reverse) - int_index - 1)
for int_index, element in enumerate(list_input_expression):
    if element in ['*', '/',]: list_operation_indices.append(int_index)
for int_index, element in enumerate(list_input_expression):
    if element in ['+', '-']: list_operation_indices.append(int_index)
print('Индексы выполнения операций до обработки: {}'.format(list_operation_indices))
for int_operation_index in range(len(list_operation_indices)):
    for int_current_operation_index in range(int_operation_index + 1, len(list_operation_indices)):
        if list_operation_indices[int_current_operation_index] > list_operation_indices[int_operation_index]:
            list_operation_indices[int_current_operation_index] -= 2
print('Индексы выполнения операций после обработки: {}'.format(list_operation_indices))
for int_index_of_operation_index in list_operation_indices:
    list_input_expression[int_index_of_operation_index - 1] = performing_operations(list_input_expression[int_index_of_operation_index],
                                                                                    int(list_input_expression.pop(int_index_of_operation_index - 1)),
                                                                                    int(list_input_expression.pop(int_index_of_operation_index)))
    print(list_input_expression)
#
#
#
# # 20 + 1 ** 3 + 2 ** 1 ** 6 * 10 / 8 - 28
#
# # l[int_operation_index-1] = calc(l[int_operation_index], l.pop(int_operation_index-1), l.pop(int_operation_index))
#
# # Документация: пишем через пробелы; доступные операторы (+, -, /, **).
#
# # Прямой и обратный ход
# # list_straight_stroke = [[None, 149, None, 9]]
# # while True:
# #     current_operation_list = [list_straight_stroke[-1][1], list_straight_stroke[-1][3]]
# #     current_operation_list.append(current_operation_list[0] // current_operation_list[1])
# #     current_operation_list.append(current_operation_list[0] - current_operation_list[1] * current_operation_list[-1])
# #     list_straight_stroke.append(current_operation_list)
# #     print(list_straight_stroke)
# #     if list_straight_stroke[-1][-1] == 1: break
# # list_straight_stroke.pop(0)
# # l = [[149, 9, 16, 5], [9, 5, 1, 4], [5, 4, 1, 1]]
# # l_rev = [[l[-1][0], 1], [l[-1][1], -l[-1][2]]]
# # for oper in range(len(l) - 2, -1, -1):
# #     print('Список до начала текущих изменений:', l_rev)
# #     list_ind_cur_rem = []
# #     int_cur_rem = l[oper][3]
# #     print('Заменяемый остаток:', int_cur_rem)
# #     for int_ind_list_numer in range(len(l_rev)):
# #         if int_cur_rem in l_rev[int_ind_list_numer]: list_ind_cur_rem.append(int_ind_list_numer)
# #         if len(list_ind_cur_rem) > 1: list_ind_cur_rem[-1] += 1
# #     print('Индексы итерации:', list_ind_cur_rem)
# #     list_cur_rep = [[l[oper][0], 1],
# #                     [l[oper][1], -l[oper][2]]]
# #     print('Подсписок изменений:', list_cur_rep)
# #     for int_ind_cur_rem in list_ind_cur_rem:
# #         list_cur_rep[0][1] = l_rev[int_ind_cur_rem][1]
# #         list_cur_rep[1][1] *= l_rev[int_ind_cur_rem][1]
# #         l_rev[int_ind_cur_rem] = list_cur_rep[0]
# #         l_rev.insert(int_ind_cur_rem + 1, list_cur_rep[1])
# #         print('Список оборатного хода, после текущего изменения:', l_rev)
# #     print('{:*^120}'.format('*'))
#