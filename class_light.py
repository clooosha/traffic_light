#-*- coding: utf-8 -*-
import itertools
class Light:
	def __init__(self,):
		self.color = 'green'
		self.break_section = [set(),set()]	#список сломанных секциц для каждого циферблата
		self.work_section = [set(), set()]	#список рабочих секций
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

	def search_number(self, section):
		"""Поиск среди цифр возможных по множеству горящих секций"""
		return {x for x in range(len(self.set_number)) if len(section - self.set_number[x]) == 0}

	def search_break_section(self, work_section, prev_section, numbs):
		"""Определение сломанных секций."""
		break_section = set()
		for x in range(len(prev_section)):
			#Определяем текущие незаженные, рабочие секции = 
			cur_nolight_and_work = ({0,1,2,3,4,5,6} ^ prev_section[x]) & work_section
			#При нахождении такой секции в цифре, исключаем цифру
			for y in cur_nolight_and_work:
				del_num = set()
				for num in numbs:
					if y in self.set_number[num - x]:
						del_num.add(num)
				numbs -= del_num
		
		#Если таких цифр нет, возвращаем пустые множества
		if len(numbs) == 0:
			return (set(), set())
		else:
			for x in range(len(prev_section)):
				section = {0,1,2,3,4,5,6}
				cur_numbs = {num - x for num in numbs}
				for cur_num in cur_numbs:
					section &= self.set_number[cur_num]
				break_section |= section - prev_section[x]
			return (numbs, break_section)

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
					self.numbs[0], self.break_section[0] = self.search_break_section(self.work_section[0], self.prev_section[0], self.numbs[0])
					if len(self.numbs[0]) == 0:
						return ('error', "No solutions found")						#Ошибка. Некорректные данные
					self.numbs[1], self.break_section[1] = self.search_break_section(self.work_section[1], self.prev_section[1], self.numbs[1])

					if len(self.numbs[1]) == 0:
						return ('error', "No solutions found")						#Ошибка. Некорректные данные
					return ('ok', [self.counter], self.set_in_str(self.break_section[0]), self.set_in_str(self.break_section[1]))
		else:
			#Анализ 1-го циферблата
			cur_section = self.str_in_set(str_nums[0])
			cur_numbs = self.search_number(cur_section)
			self.work_section[0] |= cur_section

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
			else:
				self.numbs[0], self.break_section[0] = self.search_break_section(self.work_section[0], self.prev_section[0], self.numbs[0])

			#Анализ 2-го циферблата
			cur_section = self.str_in_set(str_nums[1])
			self.work_section[1] |= cur_section

			if len(self.prev_section[1]) < 10:
				self.prev_section[1].append(cur_section)

			cur_numbs = self.search_number(cur_section)

			if self.counter == 0:											#Первые данные
				self.numbs[1] |= set(cur_numbs)
			else:
				self.numbs[1] &= {(x + self.counter) % 10 for x in cur_numbs}#Пересечение предыдущих предполагаемых цифр и полученных сейчас

			if len(self.numbs[1]) == 0:
				return ('error', "No solutions found")						#Ошибка. Некорректные данные
			else:
				self.numbs[1], self.break_section[1] = self.search_break_section(self.work_section[1], self.prev_section[1], self.numbs[1])
				if len(self.numbs[1]) == 0:
					return ('error', "No solutions found")					#Ошибка. Некорректные данные

			self.counter += 1
		return ('ok', list(x[0]*10 + x[1] for x in itertools.product(self.numbs[0], self.numbs[1]) if x[0]*10 + x[1] != 0), self.set_in_str(self.break_section[0]), self.set_in_str(self.break_section[1]))

import unittest

class TestLights(unittest.TestCase):

	def test_str_in_set(self):
		self.assertEqual(Light().str_in_set('1010111'), {0,2,4,5,6})

	def test_set_in_str(self):
		self.assertEqual(Light().set_in_str({0,2,4,5,6}), '1010111')

	def test_search_number(self):
		self.assertEqual(Light().search_number({0,1,3,5}), {5, 6, 8, 9})

	def test_class_light(self):
		a = Light()
		self.assertEqual(a.analyze('green', ['1110111', '0011101']), ('ok', [8, 2, 88, 82], '0000000', '1000000'))
		self.assertEqual(a.analyze('green', ['1110111', '0010000']), ('ok', [8, 2, 88, 82], '0000000', '1000010'))
		self.assertEqual(a.analyze('red'), ('ok', [2], '0000000', '1000010'))
		self.assertEqual(a.analyze('green', ['1110111', '0010000']), ('error', 'The red observation should be the last'))
		b = Light()
		self.assertEqual(b.analyze('green', ['0010010', '1110110']), ('ok', [8, 10, 18, 30, 38, 40, 48, 70, 78, 80, 88, 90, 98], '0000000', '0000001'))
		self.assertEqual(b.analyze('green', ['1110111', '1110010']), ('ok', [10], '0000000', '0001001'))
		c = Light()
		self.assertEqual(c.analyze('red'), ('error', "There isn't enough data"), ('ok', [8, 2, 80, 88, 82], '0000000', '0000000'))
		d= Light ()
		self.assertEqual(d.analyze('green', ['1110111', '1010101']), ('ok', [8, 2, 80, 88, 82], '0000000', '0000000'))
		self.assertEqual(d.analyze('green', ['1110111', '0010010']), ('ok', [2, 82], '0000000', '0001000'))
		self.assertEqual(d.analyze('red'), ('ok', [2], '0000000', '0001000'))

if __name__ == '__main__':
	unittest.main()