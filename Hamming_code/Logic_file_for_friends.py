import math
import random

def calculation_of_correction_bits(int_n: int, list_positions_of_correction_bits: list, list_code_underword: list, bool_check: bool) -> str:
    # Данная функция используется для вычисления и проверки корректирующих битов в каждом кодовом подслове
    '''Вычисление корректирующих битов в кодовых подсловах'''
    # Проверка вида запуска (вычисление/проверка), если проверка - создаём переменную в которой будем ссумировать индексы ошибочных битов
    if bool_check: int_position_of_error_bit = 0
    # Ходим по элементам списка с индексами корректирующих бит вида [0, 1, 3, 7, 15, ...]
    for int_position_of_correction_bit in list_positions_of_correction_bits:
        # Переменная для вычисления суммы по модулю 2
        int_current_correction_bit = 0
        # При осуществлении это странного перебора (1 через 1, 2 через 2, ...) идём по концам этих промежутков: для 2 бита (1-2)(5-6) где мы идём
        # 2, 6, 8, ...; для 4 бита (3-6)(11-14) идём по 6, 14, ...; идём до конца подслова с прыжком = № бита * 2 (вывел аналитически)
        for int_position_of_tail_bit in range(int_position_of_correction_bit * 2, int_n, (int_position_of_correction_bit + 1) * 2):
            # Перебираем элементы в тех самых промежутках: 2 - (1-2)(5-6); 4 - (3-6)(11-14); левая граница = конец () - № бита - 1
            # правая граница = конец () + 1
            for int_bit_subblock_position in range (int_position_of_tail_bit - int_position_of_correction_bit, int_position_of_tail_bit + 1):
                # Если текущий элемент - бит, а не буквы то считаем
                if list_code_underword[int_bit_subblock_position][0] != 'b':
                    # Это просто сумма по модуля 2, писал не я
                    int_current_correction_bit = int(ord(str(int_current_correction_bit)) ^ ord(str(list_code_underword[int_bit_subblock_position])))
        # Если режим вычисления - исправляем корректирующий бит с 'b?' на 1/0
        if not bool_check: list_code_underword[int_position_of_correction_bit] = str(int_current_correction_bit)
        # Если проверка и мы нашли ошибку (ошибка - это если в конце сумм по модулю 2 оказалась 1, а не 0), то складываем № корректирующего бита + 1
        elif int_current_correction_bit: int_position_of_error_bit += int_position_of_correction_bit + 1
    # print(list_code_underword)
    # Если был режим проверки - готовим позицию ошибки в кодовом подслове (- 1 просто потому что играться с индексами надо)
    if bool_check:string_output = str(int_position_of_error_bit - 1)
    # Если режим вычисления - сливаем список битов в строку (текущее кодовое подслово)
    else: string_output = ''.join(list_code_underword)
    # Возвращаем 1 из ответов
    return string_output
def changing_the_bit(string_bit: str) -> str:
    '''Заменяет бит на противоположный'''
    if int(string_bit): return '0'
    else: return '1'
def cutting_code_subword_to_information_word(string_code_underword: str) -> str:
    '''Выбивание корректирующих битов из кодовых подслов и преобразование их в информационные'''
    # Заготовка под будущее информационное подслово
    list_current_information_underword = []
    # print(string_code_underword)
    # Ходим по всем индексам кодового подслова, начиная с 1 (0 нет смысла проверять)
    for int_position_of_bit in range(1, int_n + 1):
        # Нас не интересуют индексы = степени 2
        if (int_position_of_bit & (int_position_of_bit - 1) == 0): pass
        # Остальные записываем в список
        else: list_current_information_underword.append(string_code_underword[int_position_of_bit - 1])
    # А после, возвращаем информационное подслово
    return ''.join(list_current_information_underword)

# Ввод числа кодирующих битов, но тут не обработал ввод 0 и 1
int_r = int(input('Введите количество кодирующих битов в кажом кодовом подслове: ')) # обработать > 1
# Вычисление длинн кодовых и инфорационных подстрок
int_n, int_k= 2 ** int_r - 1, 2 ** int_r - 1 - int_r
# Визуализация этих же длинн
print('r = {r}, n = {n}, k = {k}'.format(r = str(int_r), n = str(int_n), k = str(int_k)))
# Ввод нашего текста
string_input_text_real = input('Введите текст для кодирования: ')
# Преобразование текста в бинарный код (кодер), писал не сам; надо обрезать - потому что в начале добавлет '0b'
string_input_text_binary = bin(int.from_bytes(string_input_text_real.encode(), 'big'))[2:]
# Просто вывод бинарного кода и его длины
print('Бинарное представление входного текста: ' + string_input_text_binary + '\nдлиной {} cимволов'.format(len(string_input_text_binary)) + '\n')
# Заготовки под списки информационных и кодовых подслов
list_informaion_underwords, list_code_underwords = [], []
# Количество незначащих 0 добавленных в последнее информационное подслово
int_count_of_zeros = 0
# Если длина бинарного кода > длины информационных подслов
if len(string_input_text_binary) > int_k:
    # Выполняем ровное количество итераций от 1 до целого числа вхождений длин информационных подстрок в нашу строку бинарного кода
    for iteration in range(1, math.ceil(len(string_input_text_binary) / int_k)):
        # Добавляем срез бинарного кода (информационное подслово) в пределах от прошлого среза, до будущего
        list_informaion_underwords.append(string_input_text_binary[iteration * int_k - int_k:iteration * int_k])
    # Если это условие выполняется - надо дополнять последнее подслово 0
    if len(string_input_text_binary) % int_k != 0:
        # Необходимое количество 0 = длина информационного подслова - (длина бинарного кода - количество целых вхождений длин информационных слов
        # * на эту самую длину
        int_count_of_zeros = int_k - (len(string_input_text_binary) - (int_k * (len(string_input_text_binary) // int_k)))
        # Добавление последнего информационного подслова, дополненного незначащими 0 с начала
        list_informaion_underwords.append(('0' * int_count_of_zeros) + string_input_text_binary[-(int_k - int_count_of_zeros):])
    # Если, бинарный код ровно делится на длину информационных подслов - просто дописываем последнее подслово
    else: list_informaion_underwords.append(string_input_text_binary[-int_k:])
# Если, изначально, длина бинарного кода < чем длина информационных посдлов
else:
    # Считаем количество 0, которые необходимо дописать
    int_count_of_zeros = int_k - len(string_input_text_binary)
    # И дописываем к началу бинарного кода
    list_informaion_underwords.append(('0' * int_count_of_zeros) + string_input_text_binary)
# Показываем иноформационные подслова
print('Информационные подслова:')
print(list_informaion_underwords)
# Идём по информационным подсловам
for string_information_underword in list_informaion_underwords:
    # Заготовки списков под текущее кодовое подслово и список с позициями корректирующих битов
    list_code_underword, list_positions_of_correction_bits = [], []
    # Вспомогательный индекс (играемся сразу с 2 длинами: информационное подслово короче кодового, поэтому нужны разные индексы)
    int_posotion_of_bits = 0
    # Проходимся по всем индексам будущего кодового подслова
    for int_position_of_bit in range(1, int_n + 1):
        # Если индекс == степени 2
        if (int_position_of_bit & (int_position_of_bit - 1) == 0):
            # Записываем в списко текущего кодового подслова конструкцию 'b?', где ? - № бита по порядку
            list_code_underword.append('b' + str(int_position_of_bit))
            # Записываем индекс текущего корректирующего бита
            list_positions_of_correction_bits.append(len(list_code_underword) - 1)
        # Если индекс != степени 2
        else:
            # Добавляем бит из информационного подслова
            list_code_underword.append(string_information_underword[int_posotion_of_bits])
            # Увеличиваем вспомогательный счётчик (сдвинулись в информационном подслове вправо)
            int_posotion_of_bits += 1
    # Запускаем функцию рассчёта всех корректирующих битов и записываем в список всех кодовых подслов: длина кодовых подслов, список индексов
    # корректирующих битов, список с самим кодовым подсловом, флаг режима вычисления
    list_code_underwords.append(calculation_of_correction_bits(int_n, list_positions_of_correction_bits, list_code_underword, False))
# Показываем всё кодовое слово
print('Кодовое слово: ' + ''.join(list_code_underwords))
# Показываем весь список кодовых подслов
print('Кодовые подслова: ')
print(list_code_underwords)
# Отчищаем список информационных подслов - эмуляция получения закодированного сообщения в бинарном виде
list_informaion_underwords.clear()
# Перебираем все кодовые подслова
for string_code_underword in list_code_underwords:
    # Генерируем случайное место появления ошибки в кодовом подслове
    int_position_of_error = random.randint(0, len(string_code_underword) - 1)
    # Выводим позицию реальной ошибки
    print('Ошибка реальная: ' + str(int_position_of_error))
    # Вносим ошибку в кодовое подслово; почему так длинно? ну потому что приходится это делать срезами строк))
    string_code_underword = (string_code_underword[:int_position_of_error] + changing_the_bit(string_code_underword[int_position_of_error]) +
                                                        string_code_underword[int_position_of_error + 1:])
    # Вычисляем с помощью функции позицию ошибки, запуская её в режиме проверки: длина кодовых подслов, список индексов
    # корректирующих битов, список с самим кодовым подсловом, флаг режима проверки
    int_position_of_error = int(calculation_of_correction_bits(int_n, list_positions_of_correction_bits, list(string_code_underword), True))
    # Показывваем теоритически вычисленную позицию ошибки
    print('Ошибка вычисленная: ' + str(int_position_of_error))
    # Исправляем ошибку (снова срезы), меняя бит на обратный с помощью самописной функции
    string_code_underword = (string_code_underword[:int_position_of_error] + changing_the_bit(string_code_underword[int_position_of_error]) +
                                         string_code_underword[int_position_of_error + 1:])
    # Получаем текущее информационное подслово, функцией выбивая из кодового подслова ненужные биты
    string_current_information_underword = cutting_code_subword_to_information_word(string_code_underword)
    # Добавляем информационное подслово в список всех информационных подслов
    list_informaion_underwords.append(string_current_information_underword)
# Если производилось добавление незначащих 0 - срезом их убираем
if int_count_of_zeros > 0: list_informaion_underwords[-1] = list_informaion_underwords[-1][int_count_of_zeros:]
# Показываем список информационных подслов
print('Информационные подслова после декодирования:')
print(list_informaion_underwords)
# Сливаем списко информационных подслов в строку бинарного кода
string_output_text_binary = ''.join(list_informaion_underwords)
# Проверка, верно ли отработал кодек Хэмминга
if string_input_text_binary != string_output_text_binary: print('Допущена ошибка при работе кодека!')
# Надеюсь будет работать только else))
else: print('Строки идентичны.')
# Показываем бинарный код декодированного сообщения
print('Декодированное информационное слово: ' + string_output_text_binary)
# Применяя преобразования бинарного кода в текст (декодер) получаем исходное сообщение; писал не сам.
print('Декодированное сообщение: ' + int(string_output_text_binary, 2).to_bytes((int(string_output_text_binary, 2).bit_length() + 7) // 8, 'big').decode())
