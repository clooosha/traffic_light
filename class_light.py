#-*- coding: utf-8 -*-
import itertools
class Light:
	def __init__(self,):
		self.color = 'green'
		self.break_section = [set(),set()]	#список сломанных секциц для каждого циферблата
		self.change_count_1 = 0
		self.prev_section = [[], []]
		self.numbs = [set(), set()]			# список множест предополагаемых цифр
		self.counter = 0					# кол-во поступивших запросов
		self.set_number = ({0,1,2,4,5,6}, {2,5}, {0,2,3,4,6}, {0,2,3,5,6}, {1,2,3,5}, {0,1,3,5,6}, {0,1,3,4,5,6}, {0,2,5}, {0,1,2,3,4,5,6}, {0,1,2,3,5,6})

	def str_in_set(self, str_num):
		"""Преобразование строки горящих секций в множество"""
		return {x for x in range(7) if int(str_num[x])}

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

	def search_break_section(self, cur_section, cur_numbs):
		"""Определение сломанных секций."""
		section = {0,1,2,3,4,5,6}
		for x in cur_numbs:
			section &= self.set_number[x]									#Из списка предполагаемых цифр, определяем множество общих секций
		return section - cur_section										#Вычитаем текущие секции

	def analyze(self, color, str_nums = ['0000000', '0000000']):
		"""Анализируем полученные секции и цвет цветофора"""
		if self.color == 'red':
			return ('error', "The red observation should be the last")
		if color == 'red':
			self.color = 'red'
			if self.counter == 0:
				return ('error', "There isn't enough data") 				#Ошибка, нет данных
			else:
				self.numbs[0] &= {self.counter // 10}
				self.numbs[1] &= {self.counter % 10}
				if len(self.numbs[0]) == 0 or len(self.numbs[0]) == 0:
					return ('error', "No solutions found")
				else:
					for x in range(len(self.prev_section[0])):
						self.break_section[0] |= self.search_break_section(self.prev_section[0][x], {y - x for y in self.numbs[0]})
					for x in range(len(self.prev_section[1])):
						self.break_section[1] |= self.search_break_section(self.prev_section[1][x], {y - x for y in self.numbs[1]})
				return ('ok', [self.counter], self.set_in_str(self.break_section[0]), self.set_in_str(self.break_section[1]))
		else:
			#Анализ 1-го циферблата
			cur_section = self.str_in_set(str_nums[0])
			cur_numbs = self.search_number(cur_section)

			if self.counter == 0:											#Первые данные
				self.numbs[0] |= set(cur_numbs)
				self.prev_section[0].append(cur_section)

			if cur_section != self.prev_section[0][-1]:						#Сменилась цифра на 1-м циферблате, значит на 2-ом текущая 9
				self.numbs[1] &= {(9 + self.counter) % 10}					#Значит на 2-м цифра текущая 9, вычесляем стартовую, учитывая ранее найденные
				if len(self.prev_section[0]) < 10:
					self.prev_section[0].append(cur_section)
					self.numbs[0] &= {(x + len(self.prev_section[0]) - 1) % 10 for x in cur_numbs}	#Пересечение предыдущих предполагаемых цифр и полученных сейчас

			if len(self.numbs[0]) == 0:
				return ('error', "No solutions found")						#Ошибка. Некорректные данные
			elif len(self.numbs[0]) == 1:
				for x in range(len(self.prev_section[0])):
					self.break_section[0] |= self.search_break_section(self.prev_section[0][x], {y - x for y in self.numbs[0]})
			else:
				self.break_section[0] |= self.search_break_section(cur_section, cur_numbs)

			#Анализ 2-го циферблата
			cur_section = self.str_in_set(str_nums[1])
			if len(self.prev_section[1]) < 10:
				self.prev_section[1].append(cur_section)

			cur_numbs = self.search_number(cur_section)

			if self.counter == 0:											#Первые данные
				self.numbs[1] |= set(cur_numbs)
			else:
				self.numbs[1] &= {(x + self.counter) % 10 for x in cur_numbs}#Пересечение предыдущих предполагаемых цифр и полученных сейчас

			if len(self.numbs[1]) == 0:
				return ('error', "No solutions found")						#Ошибка. Некорректные данные
			elif len(self.numbs[1]) == 1:
				for x in range(len(self.prev_section[1])):
					self.break_section[1] |= self.search_break_section(self.prev_section[1][x], {y - x for y in self.numbs[1]})
			else:
				self.break_section[1] |= self.search_break_section(cur_section, cur_numbs)

			self.counter += 1
		return ('ok', list(x[0]*10 + x[1] for x in itertools.product(self.numbs[0], self.numbs[1])), self.set_in_str(self.break_section[0]), self.set_in_str(self.break_section[1]))

if __name__ == '__main__':
	a = Light()
	print (a.analyze('green', ['1110111', '0011101']))
	print (a.analyze('green', ['1110111', '0010000']))
	print (a.analyze('red'))
	print (a.analyze('green', ['1110111', '0010000']))
	b = Light()
	print (b.analyze('green', ['0010010', '1110110']))
	print (b.analyze('green', ['1110111', '1110010']))
	c = Light()
	print (c.analyze('red'))