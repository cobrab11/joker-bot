# -*- coding: utf-8 -*-

### LANGPACK ###

info_ping_pong_msg = u'пинг от %s %s секунд'
info_ping_not_found_msg = u'Цель не найдена'
info_ping_no_answer_msg = u'Нет ответа'
info_ping_self_msg = u'тебя'

################

#if not ping_pending:
ping_pending = []



def handler_ping(t, s, p):
 muc = s[1]
 nick = s[2]

 p = p.strip()

 if p:						# если указан параметр
  p = string_strip(p)

  if is_online(muc, p):				# если это ник и он в конфе
   target = muc + '/' + p

  else:							# может это сервер
   target = p

 else:
  target = muc + '/' + nick

 id = 'p' + str(random.randrange(1, 10000))

 iq = xmpp.Iq('get')
 iq.setID(id)
 iq.setTo(target)
 iq.setTag('ping', {}, 'urn:xmpp:ping')

 t0 = time.time()
# jcon.SendAndCallForResponse(iq, handler_ping_answer, {'t': t, 's': s, 'p': p, 't0': t0})
 jcon.SendAndCallForResponse(iq, ping_process, {'t': t, 's': s, 'p': p, 't0': t0})
 ping_pending.append(id)



# защита от падений

def ping_process(iq, response, t, s, p, t0):
 threading.Thread(None, ping_answer, 'ping_' + response.getID(), (iq, response, t, s, p, t0,)).start()



def ping_answer(iq, res, t, s, p, t0):
 t1 = time.time()

 nick = s[2]
 id = res.getID()

 if id in ping_pending:
  ping_pending.remove(id)

 else:
  print u'ping queue error'
  return

 if res:
  if not res.getErrorCode() == '404':
   if not p or p == nick:
    target = info_ping_self_msg

   else:
    target = p

   answer = info_ping_pong_msg % (target, str(round(t1 - t0, 3)))

  else:
   answer = info_ping_not_found_msg

 else:
  answer = info_ping_no_answer_msg

 reply(t, s, answer)
	


register_command_handler(handler_ping, u'.пинг', [u'инфо',u'все'], u'Показывает время отклика от пользователя или сервера. Если нет параметров, то показывает время отклика от вызвавшего команду.', u'.пинг <ник>', 1, True)
register_command_handler(handler_ping, u'.п', [], pub=True)
