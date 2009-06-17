# -*- coding: utf-8 -*-

### LANGPACK ###

muc_disable_enable_msg = u'Команда %s включена'
muc_disable_disable_msg = u'Команда %s отключена'
muc_disable_not_found_msg = u'Нет такой команды в отключенных'
muc_disable_found_msg = u'Команда %s уже отключена'
muc_disable_empty_msg = u'Нет отключенных команд'
muc_disable_disabled_msg = u'\nСписок отключенных команд:\n'
muc_disable_all_enabled_msg = u'Все команды включены'

################

muc_disable_all_key = u'все'

################



def handler_disable_cmd(t, s, p):
 muc = s[1]
 nick = s[2]

 if p:
  if p in COMMANDS:
   disabled = load_option(muc, 'disabled') or []

   if not p in disabled:
    disabled.append(p)
    save_option(( (muc, 'disabled', disabled), ))
    answer = muc_disable_disable_msg % (p,)

   else:
    answer = muc_disable_found_msg % (p,)

  else:
   answer = muc_disable_not_found_msg

 else:
  answer = syntax_error_msg

 reply(t, s, answer)



def handler_enable_cmd(t, s, p):
 muc = s[1]
 nick = s[2]

 if p:
  disabled = load_option(muc, 'disabled')

  if disabled:
   if p == muc_disable_all_key:
    save_option(( (muc, 'disabled', None), ))
    answer = muc_disable_all_enabled_msg

   else:
    if p in disabled:					# если команда находится в отключенных
     disabled = disabled.remove(p)
     save_option(( (muc, 'disabled', disabled), ))
     answer = muc_disable_enable_msg % (p,)

    else:
     answer = muc_disable_not_found_msg

  else:
   answer = muc_disable_empty_msg

 else:
  disabled = load_option(muc, 'disabled')

  if disabled:
   answer = muc_disable_disabled_msg + ', '.join(disabled)

  else:
   answer = muc_disable_empty_msg

 reply(t, s, answer)



register_command_handler(handler_disable_cmd, u'.отключить', [u'админ', u'все'], u'Отключает команду бота в конференции', u'.отключить <команда>', 30)
register_command_handler(handler_enable_cmd, u'.включить', [u'админ', u'все'], u'Включает команду бота в конференции. Для включения всех команд используйте команду ".включить %s". Если вызвать без параметров, выводит список отключенных команд' % muc_disable_all_key, u'.включить [команда/%s]' % muc_disable_all_key, 30)