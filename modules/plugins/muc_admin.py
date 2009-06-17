# -*- coding: utf-8 -*-

### LANGPACK ###

muc_admin_join_msg = u'Зашел в <%s>'
muc_admin_leave_msg = u'Вышел из <%s>'
muc_admin_leave_prs_msg = u'Выход по команде '
muc_admin_command_msg = u'администратора'
muc_admin_no_muc_msg = u': необходимо указать конфенренцию'
muc_admin_no_such_muc_msg = u'Отсуствую в конференции [%s]'
muc_admin_wrong_muc_msg = u'Неправильный адрес конференции'
muc_admin_reason_msg = u'\nПричина: '

################


def handler_admin_join(t, s, p):
 pwd = None
 nick = unicode(DEFAULT_NICK, 'utf-8')

 p = p.strip()

 if p:
  p = p.split('\n', 1)

  if len(p) == 2:
   pwd = p[1]

  p = p[0].split(' ', 1)
  muc = p[0].split()[0].lower()

  if muc.count('@') == 1:
   if len(p) == 2:
    nick = p[1]

   MUCLIST[muc] = {}
   MUCLIST[muc]['nick'] = nick
   MUCLIST[muc]['pwd'] = pwd
   muclist_update()

   join(muc, nick, pwd)
   answer = muc_admin_join_msg % muc

  else:
   answer = muc_admin_wrong_muc_msg
   
 else:
  answer = syntax_error_msg + muc_admin_no_muc_msg

 reply(t, s, answer)



def handler_admin_leave(t, s, p):
 muc = s[1]
 nick = s[2]
 jid = s[0]

 if is_muc(muc):
  prs = muc_admin_leave_prs_msg + nick

 else:
  prs = muc_admin_leave_prs_msg + muc_admin_command_msg

 target = None
 answer = None

 p = p.strip()
 prm = p.split(' ', 1)						# выделяем первую часть

 if p and prm[0].count('@') == 1:					# если есть параматр и prm похоже на адрес конфы
  target = prm[0]

  if len(prm) == 2:						# считаем что это адрес конфы :)
   prs += muc_admin_reason_msg + p[len(prm[0])+1:]

 else:								# если нет параметра
  if p:								# если prm не похоже - это все причина
   prs += muc_admin_reason_msg + p

 if is_muc(muc):						# если вызвали из конфы
  if not target:						# и не указали явно адрес
   target = muc							# то конфа и есть конфа

  else:
   if not target == muc:
    if get_access_level(jid, muc, nick) < 50:			# проверяем уровень доступа
     reply(t, s, core_access_denied_msg)
     return

 else:								# если в ростер
  if not target:
   print 'error muc'
   reply(t, s, core_syntax_error_msg + muc_admin_no_muc_msg)	# говорим, что надо указать конфу
   return

  else:
   answer = muc_admin_leave_msg % target

 target = target.lower()

 if target in MUCLIST:
  leave(target, prs)
  time.sleep(3)
  del MUCLIST[target]
  muclist_update()

 else:
  answer = muc_admin_no_such_muc_msg % target  

 if answer:
  reply(t, s, answer)



register_command_handler(handler_admin_join, u'.зайти', [u'админ',u'все'], u'Зайти в конференцию. Ник в конференции указываеся через пробел. Пароль - на второй строке.', u'.зайти <конференция> [ник]\n[пароль]', 15, True)
register_command_handler(handler_admin_leave, u'.выйти', [u'админ',u'все'], u'Выгнать бота из конференции.', u'.выйти [конференция] [причина]', 15, True)
