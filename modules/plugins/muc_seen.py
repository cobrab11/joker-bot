# -*- coding: utf-8 -*-

### LANGPACK ###

muc_seen_seen_msg = u'В последний раз %s был замечен %sназад.'
muc_seen_seen_unknown_msg = u'Нет данных о %s.'
muc_seen_seen_online_msg = u'%s сейчас в конференции;\n'
muc_seen_seen_self_msg = u'Я тут.'
muc_seen_idle_msg = u'%s молчит уже %s.'
muc_seen_idle_online_msg = u'Ты не молчишь.'
muc_seen_idle_self_msg = u'Я мыслю - значит существую! ©'
muc_seen_online_msg = u'%s провел в конференции %s секунд.'
muc_seen_not_found_msg = u'Ник %s не найден.'

################



def handler_seen(t, s, p):
 muc = s[1]
 nick = s[2]

 answer = ''

 p = p.strip()

 if p:
  if p == get_own_nick(muc):
   reply(t, s, muc_seen_seen_self_msg)
   return

  target = get_jid(muc, p)

  if target:
   if is_online(muc, load_attribute(muc, target, 'nicks')[0]):			# если этот джид онлайн
    answer = muc_seen_seen_online_msg % p

   seen = load_attribute(muc, target, 'seen')

   if seen:
    last = get_time() - seen

    td, th, tm, ts = format_time(last)

    seen_str = ''

    if td:
     seen_str += str(td) + u' дней '

    if th:
     seen_str += str(th) + u' часов '

    if tm:
     seen_str += str(tm) + u' минут '

    if not seen_str:
     seen_str += str(ts) + u' секунд '

    answer += muc_seen_seen_msg % (p, seen_str)

   else:
    answer += muc_seen_seen_unknown_msg % p

  else:
   answer = muc_seen_not_found_msg % p

 else:
  answer = core_syntax_error_msg

 reply(t, s, answer)



def handler_idle(t, s, p):
 muc = s[1]
 nick = s[2]

# answer = ''

 p = p.strip()

 if p:
  if p == get_own_nick(muc):
   reply(t, s, muc_seen_idle_self_msg)
   return

  if p == nick:
   reply(t, s, muc_seen_idle_online_msg)
   return

  if p in list_data_nodes(muc):
   idle = get_time() - (get_attribute(muc, nick, 'idle') or 0)

   td, th, tm, ts = format_time(idle)

   idle_str = ''

   if td:
    idle_str += str(td) + u' дней '

   if th:
    idle_str += str(th) + u' часов '

   if tm:
    idle_str += str(tm) + u' минут '

   if not idle_str:
#    idle_str = u'%s все время говорит'
    idle_str += str(ts) + u' секунд '

   answer = muc_seen_idle_msg % (p, idle_str)

  else:
   answer = core_not_in_muc_msg % p

 else:
  answer = core_syntax_error_msg

 reply(t, s, answer)



def handler_online(t, s, p):
 muc = s[1]
 nick = s[2]

# answer = ''

 p = p.strip()

 target = p

 if not p:
  p = nick
  target = u'Ты'

 if p in list_data_nodes(muc):
  answer = muc_seen_online_msg % (target, (load_attribute(muc, get_attribute(muc, p, 'jid'), 'online') or 0) + (get_time() - get_attribute(muc, p, 'join')) )

 else:
  answer = core_not_in_muc_msg % p

 reply(t, s, answer)



def handler_join_seen(jid, muc, nick, aff, role):
 t = get_time()
 set_attribute(( (muc, nick, 'join', t), (muc, nick, 'idle', t) ))



def handler_leave_seen(jid, muc, nick, aff, role):
 t = get_time()
 save_attribute(( (muc, jid, 'seen', t), (muc, jid, 'online', t - (get_attribute(muc, nick, 'join') or 0) + (load_attribute(muc, jid, 'online') or 0)) ))
 set_attribute(( (muc, nick, 'join', None), (muc, nick, 'idle', None) ))



def handler_message_seen(t, s, p):
 muc = s[1]
 nick = s[2]

 if is_muc(muc):
  set_attribute(( (muc, nick, 'idle', get_time()), ))



def get_time():
 return int(time.time())



def format_time(time):

 td = time/86400			# дни (60*60*24)

 th = time%86400/3600			# остаток от дней делим на часы (60*60)

 tm = time%86400%3600/60		# остаток от часов делим на минуты

 ts = time%86400%3600%60		# остаток от минут - секунды

 print td, th, tm, ts

 return td, th, tm, ts



register_command_handler(handler_seen, u'.был', [u'конфа', u'все'], u'Показывает время, когда в последний раз пользователь был в конференции', u'.был <ник>')
register_command_handler(handler_idle, u'.молчит', [u'конфа', u'все'], u'Показывает время, в течение которого пользователь ничего не говорил', u'.молчит <ник>')
#register_command_handler(handler_online, u'.онлайн', [u'конфа', u'все'], u'Показывает время, проведенное пользователем в конференции', u'.онлайн [ник]')
register_join_handler(handler_join_seen)
register_leave_handler(handler_leave_seen)
register_message_handler(handler_message_seen)
