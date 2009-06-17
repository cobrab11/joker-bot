# -*- coding: utf-8 -*-

### LANGPACK ###

muc_send_message_msg = u'Сообщение от %s:\n%s'
muc_send_sent_msg = u'Сообщение для %s сохранено'
muc_send_sent_online_msg = u'Сообщение для %s отправлено'
muc_send_not_sent_msg = u'Получатель неизвестен'
muc_send_empty_msg = u'Нет текста сообщения'
muc_send_not_send_self_msg = u'Нельзя отправлять сообщения самому себе'
muc_send_not_send_bot_msg = u'Нельзя отправлять сообщения боту'

################



def handler_send(t, s, p):
 muc = s[1]
 nick = s[2]

 if p:
  p = p.split('=', 1)

  if len(p) == 2:				# если присутствует '='

   if p[0]:
    recipient = p[0]
    message = p[1].strip()

    if recipient[-1] == ' ':				# удаляем, если есть, пробел перед '='
     recipient = recipient[:-1]

    print '[' + recipient + ']'

    if message:

     if recipient == nick:				# если сам себе
      reply(t, s, muc_send_not_send_self_msg)
      return

     if recipient == get_own_nick(muc):			# если боту
      reply(t, s, muc_send_not_send_bot_msg)
      return

     if get_attribute(muc, recipient, 'online'):		# если получатель онлайн
      print 'MESSAGE', muc_send_message_msg % (nick, message)
      reply('chat', [None, muc, recipient], muc_send_message_msg % (nick, message))
      answer = muc_send_sent_online_msg % recipient

     else:
      done = False

      for jid in list_db_nodes(muc):
       print jid, load_attribute(muc, jid, 'nicks')
       if recipient in load_attribute(muc, jid, 'nicks'):
        print 'FOUND'
        msgs = load_attribute(muc, jid, 'msg') or []
        print 'msgs', msgs
        msgs.append(muc_send_message_msg % (nick, message))

        save_attribute(( (muc, jid, 'msg', msgs), ))
        done = True

      print done
      if done:
       answer = muc_send_sent_msg % recipient

      else:
       answer = muc_send_not_sent_msg

    else:
     answer = muc_send_empty_msg

   else:
    answer = syntax_error_msg

  else:
   answer = syntax_error_msg

 else:
  answer = syntax_error_msg

 reply(t, s, answer)



def handler_join_send(jid, muc, nick, aff, role):
 time.sleep(1)

 msgs = load_attribute(muc, jid, 'msg')

 if msgs:
  for i in range(0, len(msgs)):
   reply('chat', [None, muc, nick], msgs.pop(i))

  save_attribute(( (muc, jid, 'msg', msgs), ))




register_command_handler(handler_send, u'.сообщение', [u'все', u'конфа'], u'Передаёт сообщение другому участнику. Если участник не в конференции, он получит сообщение при входе.', u'.сообщение <ник> = <текст>')
register_join_handler(handler_join_send)
