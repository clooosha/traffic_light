#-*- coding: utf-8 -*-
import itertools
class Light:
    def __init__(self, _id):
	self._id = _id				#идентификатор светофора
	self.break_section= [set(), set()]		#список сломанных секция для каждого циферблата
	self.numbs = [set(), set()]			#список множест предополагаемых цифр дл
	self.counter = 0			#кол-во поступивших запросов
	self.set_number = ({0,1,2,4,5,6}, {2,4}, {0,2,3,4,6}, {0,2,3,5,6}, {1,2,3,5}, {0,1,3,5,6}, {0,1,3,4,5,6}, {0,2,5}, {0,1,2,3,4,5,6}, {0,1,2,3,5,6})

    def str_in_set(self, str_num):
	"""Преобразование строки горящих секций в множество"""
	return {x for x in xrange(7) if int(str_num[x])}

    def set_in_str(self, set_):
	"""Преобразование множества секций в строку для вывода пользователю"""
	rez = ''
	for x in range(7):
	    if x in set_:
		rez +='1'
	    else:
		rez +='0'
	return rez

    def search_number(self, num):
	"""Поиск среди цифр возможных по множеству горящих секций"""
	return {x for x in range(len(self.set_number)) if len(num - self.set_number[x]) == 0}

    def search_break_section(self, cur_num, cur_numbs):
	"""Определение сломанных секций."""
	section = {0,1,2,3,4,5,6}
	for x in cur_numbs:
		section &= self.set_number[x]		#Из списка предполагаемых цифр, определяем множество общих секций
	return section - cur_num			#Вычитаем текущие секции

    def analyze(self, color, str_num1 = '0000000', str_num2 = '0000000'):
	"""Анализируем полученные секции и цвет цветофора"""
	if color == 'red':
	    if self.counter == 0:
		return -2				#Ошибка, нет данных
	    else:
		return (self.counter, self.set_in_str(self.break_section[0]), self.set_in_str(self.break_section[1]))
	else:
	    #Анализ 1-го циферблата
	    cur_num = self.str_in_set(str_num1)
	    cur_numbs = self.search_number(cur_num)

	    if self.counter == 0:				#Первая данные
		self.numbs[0] |= set(cur_numbs)
	    if self.numbs[0] != cur_numbs:			#Сменилась цифра на 1-м циферблате, значит на 2-ом текущая 9
		self.numbs[1] = (9 + self.counter) % 10		#Значит на 2-м текущая 9
		self.numbs[0] &= {(x + 1) % 10 for x in cur_numbs}#Пересечение предыдущих предполагаемых цифр и полученных сейчас

	    cur_break_section = set()
	    if len(self.numbs[0]) == 0:
		return -1				#Ошибка. Некорректные данные
	    elif len(self.numbs[0]) == 1:
		cur_break_section = self.search_break_section(cur_num, (self.numbs[0] - counter) % 10)
	    else:
		cur_break_section = self.search_break_section(cur_num, cur_numbs)
	    self.break_section[0] |= cur_break_section

	    #Анализ 2-го циферблата
	    cur_num = self.str_in_set(str_num2)
	    cur_numbs = self.search_number(cur_num)

	    if self.counter == 0:				#Первая данные
		self.numbs[1] |= set(cur_numbs)
	    else:
		self.numbs[1] &= {(x + self.counter) % 10 for x in cur_numbs}#Пересечение предыдущих предполагаемых цифр и полученных сейчас
	    
	    cur_break_section = set()
	    if len(self.numbs[1]) == 0:
		return -1				#Ошибка. Некорректные данные
	    elif len(self.numbs[1]) == 1:
		cur_break_section = self.search_break_section(cur_num, (self.numbs[1] - counter) % 10)
	    else:
		cur_break_section = self.search_break_section(cur_num, cur_numbs)
	    self.break_section[1] |= cur_break_section
	    
	    self.counter += 1
	    return (list(itertools.product(self.numbs[0], self.numbs[1])), self.set_in_str(self.break_section[0]), self.set_in_str(self.break_section[1]))
	