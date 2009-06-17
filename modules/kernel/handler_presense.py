# -*- coding: utf-8 -*-

### HANDLERS ###################################################################

def presence_handler(con, prs):
# global DATA
 ptype = prs.getType()
 full_jid = prs.getJid()
 muc = prs.getFrom().getStripped()
 nick = prs.getFrom().getResource()
 afl = prs.getAffiliation()
 role = prs.getRole()

 if not is_muc(muc):			# не обрабатывать презенсы в ростере
  return

 if not nick:
  print 'PRESENSE: no nick'

 if full_jid:
  jid = full_jid.split('/')[0].lower()		# изменение регистра требуется чтобы обрабатывать Admin и admin как одно и то же

 else:
  jid = nick

 print '\n-===-'
 try:
  if muc and nick: print muc, nick
  if afl and role: print afl, role
  if jid: print jid
 except:
  pass
 print ptype
 print '-end-\n'



 if ptype == None or ptype == 'available':
  if muc in MUCLIST:
   if not get_attribute(muc, nick, 'online'):		# подключился новый участник
    call_join_handlers(jid, muc, nick, afl, role)

   else:
#    call_status_handlers()
    print 'NO NEW USER (presence)'

   set_attribute(( (muc, nick, 'jid', jid), (muc, nick, 'afl', afl), (muc, nick, 'role', role), (muc, nick, 'online', True) ))		# depreciated

   nicks = load_attribute(muc, jid, 'nicks') or []		# запоминание списка ников пользовтеля

   if nick in nicks:						# убираем дубликаты
    nicks.remove(nick)

   nicks.insert(0, nick)
   save_attribute(( (muc, jid, 'nicks', nicks), ))



 elif ptype == 'unavailable':				# отключился
  if nick == get_own_nick(muc):					# если бота выгнали/сам отвалился
   lst = []

   for node in list_data_nodes(muc):				# генерируем событие выхода для всех пользователей
    lst.extend([(muc, node, 'afl', None), (muc, node, 'role', None), (muc, node, 'jid', None), (muc, node, 'online', False)])
    call_leave_handlers(get_attribute(muc, node, 'jid'), muc, node, afl, role)

   set_attribute(tuple(lst))

  else:
   set_attribute(( (muc, nick, 'afl', None), (muc, nick, 'role', None), (muc, nick, 'jid', None), (muc, nick, 'online', False) ))
   call_leave_handlers(jid, muc, nick, afl, role)



 elif ptype == 'error':
  ecode = prs.getErrorCode()
  if ecode:

   if ecode == '409':			# если ник занят
    log(u'error: conflict in ' + muc)
#    join(muc, nick + '+')		# пароли прикрутить

   elif ecode == '404':			# если конфа не найдена
    log(u'error: 404 in ' + muc)

   elif ecode in ['401','403','405',]:	# а хз
    log(u'error: 40x in ' + muc)

   elif ecode == '503':			# снова хз (возможно временно недоступна)
    log(u'error: 503 in ' + muc)
    time.sleep(60)
    join(muc, nick)

# print DATA[muc]['nodes']
# call_presence_handlers(jid, muc, nick, afl, role)
 call_presence_handlers(prs)
