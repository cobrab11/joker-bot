# -*- coding: utf-8 -*-

################################################################################

MQ = {}
MQT = {}

Q = {}

### FUNCTIONS ##################################################################

def get_jid(muc, target):
 log('get_jid: ' + muc + ' ' + target)

 nick_pattern = re.compile(r'".+"')
 jid_pattern = re.compile(r"'.+'")

 if jid_pattern.match(target):					# обработка ников с пробелами
  jid = target[1:-1].lower()				# lower() ???

 else:
  if nick_pattern.match(target):				# обработка джидов
   target = target[1:-1]

  jid = None

  for item in list_db_nodes(muc):				# поддержка списка ников
   if target in (load_attribute(muc, item, 'nicks') or []):
    jid = item
    break

#  jid = get_attribute(muc, target, 'jid')

 return jid



def get_access_level(jid, node, resource):
 return get_global_access(jid) or get_affiliation(node, resource)



def get_global_access(jid):
 log('get_global_access for: ' + jid)
 return ACCESSLIST.get(jid, 0)



def get_affiliation(muc, nick):
  log('get_affiliation for: ' + muc + ' ' + nick)
  return AFFILIATIONS[get_attribute(muc, nick, 'afl')]



def get_own_nick(muc):
 return MUCLIST[muc]['nick']



def join_all():
 for muc in MUCLIST:
  join(muc, MUCLIST[muc]['nick'], MUCLIST[muc]['pwd'])



def join(muc, nick=None, pwd=None):
 if not nick:
  nick = DEFAULT_NICK
 log(u'joining ' + muc + u' as ' + nick)

 nick = nick

 DATA[muc] = {}						# надо бы вынести это в set_attribute()
 DATA[muc]['nodes'] = {}
 DATA[muc]['options'] = {}

 Q[muc] = 0						# счетчик изменений DB[muc]
 load_db(muc)

 MQ[muc] = []								# очередь сообщений (MessageQueue)
 MQT[muc] = threading.Condition(threading.Lock())			# событие обработки потока сообщений (MQThreads)

 threading.Thread(None, msg_process, muc, (muc,)).start()		# создание потока конференции

# call_enter_handlers(muc)

 presence = xmpp.protocol.Presence(muc + '/' + nick)
 presence.setStatus(STATUS)
 prs = presence.setTag('x', namespace = xmpp.NS_MUC)
 prs.addChild('history', {'maxchars': '0', 'maxstanzas': '0'})

 if pwd:
  prs.setTagData('password', pwd)

 jcon.send(presence)



def leave_all(prs):
 for muc in MUCLIST:
  threading.Thread(None, leave, muc, (muc, prs)).start()



def leave(muc, prs=None):
 log(u'leaving ' + muc)
# call_exit_handlers(muc)

 presence = xmpp.Presence(muc, 'unavailable')
 if prs:
  presence.setStatus(prs)

 jcon.send(presence)

 time.sleep(3)				# задержка для сохранения аттрибутов
 save_db(muc)



def muclist_update():
 file_write(MUC, str(MUCLIST).encode('utf-8'))



def is_online(muc, node):
 return node in DATA[muc]['nodes']



def is_muc(node):
 return node in DATA



def list_mucs():
 return DATA.keys()



def list_data_nodes(muc):
 return DATA[muc]['nodes'].keys()



def list_db_nodes(muc):
 return DB[muc]['nodes'].keys()



def msg_process(muc):
 while process:				# пока есть конфа
  MQT[muc].acquire()

  while not MQ[muc]:
   MQT[muc].wait()

  while MQ[muc]:
   (t, s, b) = MQ[muc].pop(0)
   msg_send(t, s, b)
   time.sleep(MSGDELAY)

  MQT[muc].release()



def reply(t, s, b):
 muc = s[1]
 nick = s[2]

 if is_muc(muc):
  if t == 'groupchat':
#   if len(b) > 1000:			# ограничение длины
#    b = b[:1000] + ' >>>>'

   if nick:
    body = nick + ': ' + b

   else:
    body = b

   MQ[muc].append((t, muc, body.lstrip()))

  elif t == 'chat':
   MQ[muc].append((t, muc + '/' + nick, b))

  MQT[muc].acquire()
  MQT[muc].notifyAll()
  MQT[muc].release()

 else:
  msg_send(t, muc + '/' + nick, b)	# .lstrip()		# зачем???



def msg_send(t, s, b):
 msg = xmpp.Message(s, b)
 msg.setType(t)

 jcon.send(msg)
