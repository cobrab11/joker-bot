# -*- coding: utf-8 -*-

### HANDLERS ###################################################################

def message_handler(con, msg):
 t = msg.getType()
 s = msg.getFrom()
 b = msg.getBody()

 node = s.getStripped()						# конференция либо джид в ростере
 resource = s.getResource()					# ник либо ресурс в ростере

 if not b or not b.strip():					# защита от пустых сообщений
  return

# if len(b) > 5000:
#  b = b[:5000] + ' >>>>'

 if is_muc(node):						# если это конфа (если есть такая онлайн)
  log(resource + ': ' + b)
  if get_own_nick(node) == resource:				# не обрабатывать свои сообщения
   return

  elif not resource:						# тема конференции
   # call_subject_handlers(node, b)
   return

  jid = get_attribute(node, resource, 'jid')			# получить джид

 else:
  log(node + ': ' + b)
  jid = node							# джид, если в ростере

  if not jid in ADMINS:						# не отвечать на сообщения в ростер не от админов
   print 'not admin in roster: ', jid
   return

 if t == 'error':
  print 'error: ', msg.getErrorCode()
  return

 b = b.lstrip()
 cmd = b.split()[0].lower()

 if cmd in COMMANDS:
  access_level = get_access_level(jid, node, resource)
  if access_level >= COMMANDS[cmd]['acs']:
   call_command_handlers(cmd, t, [jid, node, resource], b[len(cmd)+1:])

  elif access_level <= 0:					# игнор-лист, игнор визиторов
   return

  else:
   reply(t, [jid, node, resource], access_denied_msg)

 else:
  call_message_handlers(t, [jid, node, resource], b)
