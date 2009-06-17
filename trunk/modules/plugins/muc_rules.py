# -*- coding: utf-8 -*-

### LANGPACK ###

muc_rules_done_msg = u'Правила записаны'
muc_rules_no_rules_msg = u'Правила не установлены'

################

def handler_rules(t, s, p):
 muc = s[1]
 nick = s[2]

 if p:
  if get_affiliation(muc, nick) >= AFFILIATIONS['admin']:
   p = p.lstrip()

   if p.startswith('='):			# если в начале присутствует '='
    rules = p[1:].lstrip()
    save_option(( (muc, 'rules', rules), ))

    answer = muc_rules_done_msg
    reply(t, s, answer)
    return

   else:
    answer = core_syntax_error_msg

  else:
   answer = core_access_denied_msg

 else:						# в будущем здесь можно выводить текущую тему по запросу
  answer = load_option(muc, 'rules')

  if not answer:
   answer = muc_rules_no_rules_msg
   reply(t, s, answer)
   return

 reply('chat', s, answer)

 if t == 'groupchat':
  reply(t, s, common_commands_sent_msg)



register_command_handler(handler_rules, u'.правила', [u'все', u'конфа'], u'Выводит правила конференции. Чтобы установить правила введите ".правила = текст"', u'.правила [= текст]')
