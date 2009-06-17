# -*- coding: utf-8 -*-

### LANGPACK ###

muc_actions_deny_kick_msg = u'Невозможно выгнать %s'
muc_actions_deny_role_msg = u'Невозможно изменить роль %s'
muc_actions_deny_afl_msg = u'Невозможно изменить роль %s'
muc_actions_unsufficient_afl_msg = u'нехватает полномочий'
#muc_actions__msg = u''
#muc_actions__msg = u''
#muc_actions__msg = u''

################

# NS_MUC_ADMIN = 'http://jabber.org/protocol/muc#admin'

################



def set_role(muc, nick, role, reason=''):			# role = ['none', 'visitor', 'participant', 'moderator']
 iq = xmpp.Iq('set')
 iq.setTo(muc)
 iq.setID('role_' + str(random.randrange(1000, 9999)))

 query = xmpp.Node('query')
 query.setNamespace(xmpp.NS_MUC_ADMIN)

 q = query.addChild('item', {'nick': nick, 'role': role})

 if role == 'none':						# причина подставляется только в случае удаления пользователя
  q.setTagData('reason', reason)

 iq.addChild(node = query)
 jcon.send(iq)



def set_affiliation(muc, jid, afl, reason=''):			# afl = ['none', 'member', 'admin', 'owner']
 iq = xmpp.Iq('set')
 iq.setTo(muc)
 iq.setID('afl_' + str(random.randrange(1000, 9999)))

 query = xmpp.Node('query')
 query.setNamespace(xmpp.NS_MUC_ADMIN)

 q = query.addChild('item', {'jid': jid, 'affiliation': afl})

 if afl == 'outcast':						# причина подставляется только в случае блокирования пользователя
  q.setTagData('reason', reason)

 iq.addChild(node = query)
 jcon.send(iq)



def handler_change_role(t, s, p, role):
 muc = s[1]
 nick = get_own_nick(muc)

 if get_attribute(muc, nick, 'role') == u'moderator':
  p = p.strip()

  if p:
   p = p.split('\n', 1)

   target = p[0].strip()
   reason = ''

   if len(p) > 1:
    reason = p[1]

   if target in list_data_nodes(muc):
    if get_affiliation(muc, nick) > get_affiliation(muc, target):
     print muc, target, role, reason
     set_role(muc, target, role, reason)
     log('setting role "' + role + '" for ' + target + '[' + muc + ']')
     return

    else:
     answer = muc_actions_deny_role_msg % target + ': ' + muc_actions_unsufficient_afl_msg

   else:
    answer = core_not_in_muc_msg % target

  else:
   answer = core_syntax_error_msg

 else:
  answer = core_not_moder_msg

 reply(t, s, answer)



def handler_change_afl(t, s, p, afl):
 muc = s[1]
 nick = get_own_nick(muc)

 if get_affiliation(muc, nick) >= AFFILIATIONS['admin']:
  p = p.strip()

  if p:
   p = p.split('\n', 1)

   target = p[0].strip()
   reason = ''

   if len(p) > 1:
    reason = p[1]

   if target in list_data_nodes(muc):
    if get_affiliation(muc, nick) > get_affiliation(muc, target):
     jid = get_attribute(muc, target, 'jid')
     print muc, jid, afl, reason
     set_affiliation(muc, jid, afl, reason)
     log('setting afl "' + afl + '" for ' + target + '[' + muc + ']')
     return

    else:
     answer = muc_actions_deny_role_msg % target + ': ' + muc_actions_unsufficient_afl_msg

   else:
    answer = core_not_in_muc_msg % target

  else:
   answer = core_syntax_error_msg

 else:
  answer = core_not_moder_msg

 reply(t, s, answer)



def handler_role_none(t, s, p):				# кик
 handler_change_role(t, s, p, 'none')

def handler_role_visitor(t, s, p):
 handler_change_role(t, s, p, 'visitor')

def handler_role_participant(t, s, p):
 handler_change_role(t, s, p, 'participant')

def handler_role_moderator(t, s, p):
 handler_change_role(t, s, p, 'moderator')



def handler_afl_outcast(t, s, p):			# бан
 handler_change_afl(t, s, p, 'outcast')

def handler_afl_none(t, s, p):
 handler_change_afl(t, s, p, 'none')

def handler_afl_member(t, s, p):
 handler_change_afl(t, s, p, 'member')

def handler_afl_admin(t, s, p):
 handler_change_afl(t, s, p, 'admin')

def handler_afl_owner(t, s, p):
 handler_change_afl(t, s, p, 'owner')



register_command_handler(handler_role_none, u'.кик', [u'все', u'админ'], u'Выгнать пользователя из конференции. На второй строке можно указать причину', u'.кик <ник>\nпричина', 15)
register_command_handler(handler_role_visitor, u'.гость', [u'все', u'админ'], u'отобрать право голоса у пользователя', u'.гость <ник>', 15)
register_command_handler(handler_role_participant, u'.участник', [u'все', u'админ'], u'Предоставить право голоса пользователю', u'.участник <ник>', 15)
#register_command_handler(handler_role_moderator, u'.модератор', [u'все', u'админ'], u'Предоставить права модератора пользователю', u'.модератор <ник>', 30)

#register_command_handler(handler_afl_none, u'.наблюдатель', [u'все', u'админ'], u'Кик', u'', 15)
##register_command_handler(handler_afl_member, u'.мембер', [u'все', u'админ'], u'Мембер', u'', 15)
##register_command_handler(handler_afl_admin, u'.админ', [u'все', u'админ'], u'Админ', u'', 15)
register_command_handler(handler_afl_outcast, u'.бан', [u'все', u'админ'], u'Заблокировать пользователя.На второй строке можно указать причину', u'.бан <ник>\nпричина', 30)