# -*- coding: utf-8 -*-

import urllib2, re, urllib, string
from xml.dom import minidom

### LANGPACK ###

net_weather_weather_msg = u'Погода для города %s:'
net_weather_not_found_msg = u'Город не найден'
net_weather_temperature_msg = u'Температура: '
net_weather_pressure_msg = u'Давление: '

net_weather_pr_units_msg = u' мм рт.ст.'

#net_weather_phenomena_msg = u'Осадки: '
net_weather_phenomena_msg = u''

net_weather_ph_0_msg = u'Ясно'
net_weather_ph_1_msg = u'Малооблачно'
net_weather_ph_2_msg = u'Облачно'
net_weather_ph_3_msg = u'Пасмурно'

net_weather_ph_4_msg = u'дождь'
net_weather_ph_5_msg = u'ливень'
net_weather_ph_6_msg = u'снег'
net_weather_ph_7_msg = u'снег'
net_weather_ph_8_msg = u'гроза'
net_weather_ph_9_msg = u'нет данных'
net_weather_ph_10_msg = u'без осадков'

net_weather_relwet_msg = u'Влажность: '
net_weather_wind_msg = u'Ветер '

net_weather_wind_units_msg = u' м/с'

net_weather_north_msg = u'северный'
net_weather_northeast_msg = u'северо-восточный'
net_weather_east_msg = u'восточный'
net_weather_southeast_msg = u'юго-восточный'
net_weather_south_msg = u'южный'
net_weather_southwest_msg = u'юго-западный'
net_weather_west_msg = u'западный'
net_weather_northwest_msg = u'северо-западный'

################

townlist_file = './data/static/gmbartlistfull.txt'
weather_url = 'http://informer.gismeteo.ru/xml/%s_1.xml'

"""
Описание формата:
TOWN			информация о пункте прогнозирования:
 index				уникальный пятизначный код города
 sname			закодированное название города
 latitude			широта в целых градусах
 longitude			долгота в целых градусах
FORECAST		информация о сроке прогнозирования:
 day, month, year		дата, на которую составлен прогноз в данном блоке
 hour				местное время, на которое составлен прогноз
 tod				время суток, для которого составлен прогноз: 0 - ночь 1 - утро, 2 - день, 3 - вечер
 weekday			день недели, 1 - воскресенье, 2 - понедельник, и т.д.
 predict			заблаговременность прогноза в часах
PHENOMENA	 	атмосферные явления:
 cloudiness			облачность по градациям:  0 - ясно, 1- малооблачно, 2 - облачно, 3 - пасмурно
 precipitation			тип осадков: 4 - дождь, 5 - ливень, 6,7 – снег, 8 - гроза, 9 - нет данных, 10 - без осадков
 rpower				интенсивность осадков, если они есть. 0 - возможен дождь/снег, 1 - дождь/снег
 spower				вероятность грозы, если прогнозируется: 0 - возможна гроза, 1 - гроза
PRESSURE		атмосферное давление, в мм.рт.ст.
TEMPERATURE		температура воздуха, в градусах Цельсия
WIND			приземный ветер
 min, max			минимальное и максимальное значения средней скорости ветра, без порывов
 direction 			направление ветра в румбах, 0 - северный, 1 - северо-восточный,  и т.д.
RELWET			относительная влажность воздуха, в %
HEAT			комфорт - температура воздуха по ощущению одетого по сезону человека, выходящего на улицу
"""



def handler_weather_get(t, s, p):

 answer = 'error'
 p = p.strip()

 if p:
  p = p.lower()

  townlist = open(townlist_file)

  while True:
   line = unicode(townlist.readline(),'windows-1251')

   if not line:
    code = 0
    break

   line = line.split(';')

   if len(line) > 1:
    if line[1].lower() == p:
     code = line[0]
     city = line[1]
     break

  townlist.close()

  if code:
   forecast = urllib2.Request(weather_url % code)
   f = urllib2.urlopen(forecast)
   body = f.read()
   dom = minidom.parseString(body)

   answer = net_weather_weather_msg % city

   temperature = get_dom_item(dom, "TEMPERATURE")
   answer += '\n' + net_weather_temperature_msg + temperature[2][5:-1] + '..' + temperature[1][5:-1]


   phenomena = get_dom_item(dom, "PHENOMENA")
   cloudness = phenomena[1][12:-1]

   if cloudness == '0':
    clouds = net_weather_ph_0_msg

   elif cloudness == '1':
    clouds = net_weather_ph_1_msg

   elif cloudness == '2':
    clouds = net_weather_ph_2_msg

   elif cloudness == '3':
    clouds = net_weather_ph_3_msg


   precipitation = phenomena[2][15:-1]

   if precipitation == '4':
    prec = net_weather_ph_4_msg

   elif precipitation == '5':
    prec = net_weather_ph_5_msg

   elif precipitation == '6':
    prec = net_weather_ph_6_msg

   elif precipitation == '7':
    prec = net_weather_ph_7_msg

   elif precipitation == '8':
    prec = net_weather_ph_8_msg

   elif precipitation == '9':
    prec = net_weather_ph_9_msg

   elif precipitation == '10':
    prec = net_weather_ph_10_msg

   answer += '\n' + net_weather_phenomena_msg + clouds + ', ' + prec


   wind = get_dom_item(dom, "WIND")
   direction = wind[1][11:-1]

   if direction == '0':
    dir = net_weather_north_msg

   elif direction == '1':
    dir = net_weather_northeast_msg

   elif direction == '2':
    dir = net_weather_east_msg

   elif direction == '3':
    dir = net_weather_southeast_msg

   elif direction == '4':
    dir = net_weather_south_msg

   elif direction == '5':
    dir = net_weather_southwest_msg

   elif direction == '6':
    dir = net_weather_west_msg

   elif direction == '7':
    dir = net_weather_northwest_msg

   answer += '\n' + net_weather_wind_msg + dir + ', ' + wind[3][5:-1] + '..' + wind[2][5:-1] + net_weather_wind_units_msg


   relwet = get_dom_item(dom, "RELWET")
   answer += '\n' + net_weather_relwet_msg + relwet[2][5:-1] + '..' + relwet[1][5:-1] + '%'


   pressure = get_dom_item(dom, "PRESSURE")
   answer += '\n' + net_weather_pressure_msg + pressure[2][5:-1] + '..' + pressure[1][5:-1] + net_weather_pr_units_msg

  else:
   answer = net_weather_not_found_msg

 else:
  answer = syntax_error_msg

 reply(t, s, answer)



def get_dom_item(dom, name):
 item = str(dom.getElementsByTagName(name)[0].toxml())
 item = item.replace('<', '').replace('/>', '')

 return item.split()



register_command_handler(handler_weather_get, u'.погода', [u'сервис', u'все'], u'Показывает погоду с сайта gismeteo.ru.', u'.погода <город>', 1, True)
