# -*- coding: utf-8 -*-

import threading

### LANGPACK BEGIN ###

info_vcard_vcard_msg = u'\nВизитка %s:'
info_vcard_empty_msg = u'<пусто>'
info_vcard_not_supported_msg = u'Информация недоступна'

### LANGPACK END ###



VCARD_FIELDS = {
'NICKNAME'	: u'Ник',
'FN'		: u'Полное имя',
'GENDER'	: u'Пол',
'URL'		: u'Сайт',
'BDAY'		: u'День рождения',
'DESC'		: u'О себе',
'TITLE'		: u'Роль',
'PHOTO'		: {'TYPE': u'Фото'},
'ADR'		: {'CTRY': u'Государство', 'REGION': u'Регион', 'LOCALITY': u'Город'},
'ORG'		: {'ORGNAME': u'Организация'},
'EMAIL'		: {'USERID': u'Мыло'},
'TEL'		: {'NUMBER': u'Телефон'}
}

###

vcard_pending = []



def handler_vcard(t, s, p):
 muc = s[1]
 nick = s[2]

 p = p.strip()

 if p:
  p = string_strip(p)

  if is_online(muc, p):
   target = muc + '/' + p

  else:
   target = p

 else:
  target = muc + '/' + nick

 print target

 id = 'p' + str(random.randrange(1, 1000))

 iq = xmpp.Iq('get')
 iq.setID(id)
 iq.setTo(target)
 iq.addChild('vCard', {}, [], 'vcard-temp')

 vcard_pending.append(id)
 jcon.SendAndCallForResponse(iq, vcard_process, {'t': t, 's': s, 'p': p})



def vcard_process(iq, response, t, s, p):

 """защита от падений"""

 threading.Thread(None, vcard_answer, 'vcard_' + response.getID(), (iq, response, t, s, p,)).start()
 print 'started'



def vcard_answer(iq, res, t, s, p):
 nick = s[2]
 id = res.getID()

 print id

 if id in vcard_pending:
  vcard_pending.remove(id)

 else:
  print 'vcard queue error'
  return

 restype = res.getType()

 if restype == 'result':
  if res.getChildren():

   if not p:
    p = nick

   answer = info_vcard_vcard_msg % p
   vcard = res.getChildren()[0].getChildren()

   for x in vcard:
    item = x.getName()

    if item in VCARD_FIELDS:
     if x.getChildren():

      for i in x.getChildren():
       subitem = i.getName()

       if subitem in VCARD_FIELDS[item]:
        data = i.getData()
        if data:
         answer += '\n' + VCARD_FIELDS[item][subitem] + u': ' + data

     else:
      data = x.getData()
      if data:
       answer += '\n' + VCARD_FIELDS[item] + u': ' + data

   if not answer:
    answer = info_vcard_empty_msg

  else:
   answer = info_vcard_empty_msg

 elif restype == 'error':
  answer = info_vcard_not_supported_msg

 reply(t, s, answer)


	
register_command_handler(handler_vcard, u'.визитка', [u'инфо',u'все'], u'Показывает информацию о пользователе.', u'.визитка <ник>')
register_command_handler(handler_vcard, u'.вкард', [])
