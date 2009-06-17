# -*- coding: utf-8 -*-

### LANGPACK ###

muc_jid_sent_msg = u'Отправлено в приват'
muc_jid_not_found_msg = u'JID для %s не определен'

################



def handler_realjid(t, s, p):
 muc = s[1]
 nick = s[2]

 target = string_strip(p.strip())

 if not target:
  target = nick

 jid = get_jid(muc, target)

 if not jid:
  answer = muc_jid_not_found_msg % target

 else:
  if t == 'groupchat':
   reply('chat', s, jid)
   answer = muc_jid_sent_msg

  else:
   answer = jid

 reply(t, s, answer)



register_command_handler(handler_realjid, u'.джид', [u'все'], u'Показывает джид пользователя', u'.джид', 30)