# -*- coding: utf-8 -*-

### LANGPACK ###

muc_subject_done_msg = u'Тема установлена'

################

def handler_subject(t, s, p):
 muc = s[1]
 nick = s[2]

 if p:
  p = p.lstrip()

  if p.startswith('='):				# если в начале присутствует '='
   subject = p[1:].lstrip()

   msg = xmpp.Message(muc, None)
   msg.setType('groupchat')
   msg.setSubject(subject)

   jcon.send(msg)

   answer = muc_subject_done_msg

  else:
   answer = core_syntax_error_msg

 else:						# в будущем здесь можно выводить текущую тему по запросу
  answer = not_implemented_msg

 reply(t, s, answer)



register_command_handler(handler_subject, u'.тема', [u'все', u'админ'], u'Устанавливает тему конференции', u'.тема = текст', 15)
