# -*- coding: utf-8 -*-


def string_rus(num, ends):				# (number, (0end, 1end, 2-4end))

 """поправка на правила русского языка ;-) (замена окончаний)"""

 number = str(num)

 if number.endswith('11') or number.endswith('12') or number.endswith('13') or number.endswith('14'):
  ending = ends[0]

 elif number.endswith('1'):
  ending = ends[1]

 elif number.endswith('2') or number.endswith('3') or number.endswith('4'):
  ending = ends[2]

 else:
  ending = ends[0]

 return ending



def string_split(string, delimiter):

 """разделение строки sring по delimiter"""

 str = re.split('[^\\\\]' + delimiter, string, 1)
 str[0] = re.sub('\\\\' + delimiter, delimiter, string[:len(str[0])+1]).strip()

 if len(str) == 2:
  str[1] = str[1].strip()

 return tuple(str)



def string_strip(string):

 """обрезание кавычек"""

 string = string.split()

 if re.match('".+"', string):
  string = string[1:-1]

 return string
