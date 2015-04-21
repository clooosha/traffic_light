#-*- coding: utf-8 -*-
from class_light import Light
a = Light(0)
print a.analyze('green', '1110111', '0011101')
print a.analyze('green', '1110111', '0010000')
print a.analyze('red')
