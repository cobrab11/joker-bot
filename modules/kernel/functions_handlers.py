# -*- coding: utf-8 -*-

################################################################################

COMMANDS = {}

COMMAND_HANDLERS = {}
MESSAGE_HANDLERS = []
PRESENCE_HANDLERS = []
IQ_HANDLERS = []
JOIN_HANDLERS = []
LEAVE_HANDLERS = []

### HANDLERS REGISTERING #######################################################

def register_message_handler(instance):
 MESSAGE_HANDLERS.append(instance)



def register_presence_handler(instance):
 PRESENCE_HANDLERS.append(instance)



def register_iq_handler(instance):
 IQ_HANDLERS.append(instance)



def register_join_handler(instance):
 JOIN_HANDLERS.append(instance)



def register_leave_handler(instance):
 LEAVE_HANDLERS.append(instance)



def register_command_handler(instance, cmd, ctg=[], dsc='', syn='', acs=1, pub=None):
# (handler, команда, категории, описание, синтаксис, доступ, флаг "используется в ростере")
 log(u'\t' + cmd)
 COMMAND_HANDLERS[cmd] = instance
 COMMANDS[cmd] = {'ctg': ctg, 'dsc': dsc, 'syn': syn, 'acs': acs, 'pub': pub}

### HANDLERS CALLING ###########################################################

def call_message_handlers(t, s, b):
 for handler in MESSAGE_HANDLERS:
  with instance_control:
   threading.Thread(None, handler, 'msg_' + str(random.randrange(0,999)), (t, s, b,)).start()



def call_presence_handlers(prs):
 for handler in PRESENCE_HANDLERS:
  with instance_control:
   threading.Thread(None, handler, 'prs_' + str(random.randrange(0,999)), (prs,)).start()



def call_iq_handlers(iq):
 print 'call_iq'
 for handler in IQ_HANDLERS:
  with instance_control:
   threading.Thread(None, handler, 'iq_' + str(random.randrange(0,999)), (iq,)).start()



def call_join_handlers(jid, muc, nick, afl, role):
 print 'call_join'
 for handler in JOIN_HANDLERS:
  with instance_control:
   threading.Thread(None, handler, 'join_' + str(random.randrange(0,999)), (jid, muc, nick, afl, role,)).start()



def call_leave_handlers(jid, muc, nick, afl, role):
 log('call_leave')
 for handler in LEAVE_HANDLERS:
  with instance_control:
   threading.Thread(None, handler, 'leave_' + str(random.randrange(0,999)), (jid, muc, nick, afl, role,)).start()



def call_command_handlers(cmd, t, s, p):
 muc = s[1]

 if is_muc(muc):
  if cmd in (load_option(muc, 'disabled') or []):		# если команда находится в отключенных
   with instance_control:
    threading.Thread(None, reply, 'cmd_' + str(random.randrange(0,999)), (t, s, core_cmd_disabled_msg % cmd,)).start()
    return

 else:
  if not COMMANDS[cmd]['pub']:			# если команда только для конференций
   with instance_control:
    threading.Thread(None, reply, 'cmd_' + str(random.randrange(0,999)), (t, s, core_muc_only_msg,)).start()
    return

 with instance_control:
  threading.Thread(None, COMMAND_HANDLERS[cmd], 'cmd_' + str(random.randrange(0,999)), (t, s, p,)).start()
