# -*- coding: utf-8 -*-

##############################################################################

DATA = {}		# основная оперативная память
DB = {}			# основная постоянная память (копия содержимого файлов, необходимо до SQL)

### DATA FUNCTIONS ###########################################################



def set_attribute(list):			# ((muc, nick, attribute, value), )
 for item in range(0, len(list)):
  muc = list[item][0]
  nick = list[item][1]
  attribute = list[item][2]
  value = list[item][3]

  if not value:
   if nick in DATA[muc]['nodes']:
    if attribute in DATA[muc]['nodes'][nick]:
     del DATA[muc]['nodes'][nick][attribute]

    if DATA[muc]['nodes'][nick] == {}:
     del DATA[muc]['nodes'][nick]

  else:
   if not nick in DATA[muc]['nodes']:
    DATA[muc]['nodes'][nick] = {}

   DATA[muc]['nodes'][nick].update({attribute: value})



def set_option(list):				# (muc, option, value)
 for item in range(0, len(list)):
  muc = list[item][0]
  option = list[item][1]
  value = list[item][2]

  if not value:
   if option in DATA[muc]['options']:
    del DATA[muc]['options'][option]

  else:
   DATA[muc]['options'].update({option: value})



def save_attribute(list):			# ((muc, jid, attribute, value), )
 for item in range(0, len(list)):
  muc = list[item][0]
  jid = list[item][1]
  attribute = list[item][2]
  value = list[item][3]

  if not value:
   if jid in DB[muc]['nodes']:
    if attribute in DB[muc]['nodes'][jid]:
     del DB[muc]['nodes'][jid][attribute]

    if DB[muc]['nodes'][jid] == {}:
     del DB[muc]['nodes'][jid]

  else:
   if not muc in DB:
    DB[muc] = {}
    DB[muc]['nodes'] = {}
    DB[muc]['options'] = {}

   if not jid in DB[muc]['nodes']:
    DB[muc]['nodes'][jid] = {}

   DB[muc]['nodes'][jid].update({attribute: value})

 if Q[muc] > 15:					# сохранять DB[muc] после 15 изменений
  save_db(muc)					# чтоб слишком часто не открывать/закрывать файл
  Q[muc] = 0

 else:
  Q[muc] += 1



def save_option(list):				# (muc, option, value)
 for item in range(0, len(list)):
  muc = list[item][0]
  option = list[item][1]
  value = list[item][2]

  if not value:
   if option in DB[muc]['options']:
    del DB[muc]['options'][option]

  else:
   if not muc in DB:
    DB[muc] = {}
    DB[muc]['nodes'] = {}
    DB[muc]['options'] = {}

   DB[muc]['options'].update({option: value})

 if Q[muc] > 15:				# сохранять DB[muc] после 15 изменений
  save_db(muc)					# чтоб слишком часто не открывать/закрывать файл
  Q[muc] = 0

 else:
  Q[muc] += 1



def get_attribute(muc, nick, attribute):
 if nick in DATA[muc]['nodes']:
  return DATA[muc]['nodes'][nick].get(attribute, None)



def get_option(muc, option):
  return DATA[muc]['options'].get(option, None)



def load_attribute(muc, jid, attribute):
 if jid in DB[muc]['nodes']:
  return DB[muc]['nodes'][jid].get(attribute, None)



def load_option(muc, option):
 return DB[muc]['options'].get(option, None)



def save_db(muc):
 file_write('./data/' + muc + '/db', str(DB[muc]).encode('utf-8'))



def load_db(muc):
 DB[muc] = eval(file_read('./data/' + muc + '/db') or "{'nodes': {}, 'options': {}}")
