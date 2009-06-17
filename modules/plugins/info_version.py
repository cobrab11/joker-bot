# -*- coding: utf-8 -*-

### LANGPACK ###

info_version_answer_msg = u'\nВерсия'
info_version_client_msg = u'\nКлиент: '
info_version_version_msg = u'\nВерсия: '
info_version_os_msg = u'\nОС: '
info_version_error_msg = u'Объект недоступен'
info_version_denied_msg = u'Информация недоступна'

################

#if not version_pending:
version_pending = []

def handler_version(t, s, p):
 muc = s[1]
 nick = s[2]

 p = p.strip()

 if p:

  p = string_strip(p)

  # непонятно зачем
  if p == MUCLIST[muc]['nick']:
   answer = u'\nКлиент: ' + __bot_name__ + u'\nВерсия: ' + __bot_ver__

   if SHARE_OS:
    osname = os.popen('ver')
    osver = osname.read().strip()
    osname.close()

    pyver = sys.version
    osver = osver + u'; Python: ' + pyver

    answer += u'\nОС: ' + osver

   reply(t, s, answer)
   return



  if is_online(muc, p):
   target = muc + '/' + p

  else:
   target = p

 else:
  target = muc + '/' + nick

 id = 'q' + str(random.randrange(1, 10000))

 iq = xmpp.Iq('get')
 iq.setID(id)
 iq.setTo(target)
 iq.setQueryNS(xmpp.NS_VERSION)

 version_pending.append(id)
 jcon.SendAndCallForResponse(iq, handler_version_answer, {'t': t, 's': s})



def handler_version_answer(iq, res, t, s):
 nick = s[2]
 id = res.getID()

 if id in version_pending:		# если пингует себя, то запросом get убивается id
  version_pending.remove(id)

 if res:				# это не нужно (заведомо есть)
  print res.getType()
  if res.getType() == 'result':
   name = None
   version = None
   os = None
   answer = ''
   props = res.getQueryChildren()

   for p in props:
    if p.getName() == 'name':
     name = p.getData()	#.encode('utf-8')

    elif p.getName() == 'version':
     version = p.getData() #.encode('utf-8')

    elif p.getName() == 'os':
     os = p.getData() #.encode('utf-8')

   if name:
    answer += info_version_client_msg + name

   if version:
    answer += info_version_version_msg + version

   if os:
    answer += info_version_os_msg + os

  else:
   answer = info_version_error_msg

 else:
  answer = info_version_denied_msg

 reply(t, s, answer)


	
register_command_handler(handler_version, u'.версия', [u'инфо',u'все'], u'Показывает информацию о клиенте пользователя или версию сервера.', u'.версия <ник\сервер>', 1, True)
register_command_handler(handler_version, u'.в', [], pub=True)