# -*- coding: utf-8 -*-

### LANGPACK ###

common_commands_cmd_msg = u'Команда "%s":\n'
common_commands_usage_msg = u'\nИспользование: '
common_commands_level_msg = u'Необходимый уровень доступа: %s'
common_commands_not_found_msg = u'Такой команды нет'
common_commands_help_msg = u'Для получения помощи по команде наберите ".команда <команда>" (без кавычек)'
common_commands_ctg_not_found_msg = u'Нет такой категории'
common_commands_ctg_msg = u'\n\nКатегории: '
common_commands_ctg_cmds0_msg = u'\nСписок команд в категоии ['
common_commands_ctg_cmds1_msg = u']:\n'
common_commands_ctg_list_msg = u'\nСписок категорий:\n%s\n\nДля просмотра списка команд содержащихся в категории наберите ".команды <категория>" (без кавычек), например: .команды все'
common_commands_disabled_msg = u'\nЭта команда отключена в данной конференции!'
#common_commands__msg = 
common_commands_help_msg = u'Краткая справка:\nПараметры команд:\n<> - обязательный параметр\n[] - необязательный параметр'
common_commands_sent_msg = u'Отправлено в приват'

################

def handler_help_command(t, s, p):
 jid = s[0]
 muc = s[1]
 nick = s[2]

 level = get_access_level(jid, muc, nick)
 ctglist = []

 p = p.strip()

 if p:
  if p in COMMANDS:
   if level >= COMMANDS[p]['acs']:
    answer = common_commands_cmd_msg % p + COMMANDS[p]['dsc'] + common_commands_ctg_msg

    for ctg in COMMANDS[p]['ctg']:
     ctglist.append(ctg)

    answer += ', '.join(ctglist) + common_commands_usage_msg + COMMANDS[p]['syn'] + '\n'
    answer += common_commands_level_msg % str(COMMANDS[p]['acs'])

    disabled = load_option(muc, 'disabled')

    if disabled and p in disabled:
     answer += common_commands_disabled_msg

   else:
    answer = common_commands_level_msg % str(COMMANDS[p]['acs'])

  else:
   answer = common_commands_not_found_msg

 else:
  answer = common_commands_help_msg

 reply('chat', s, answer)

 if t == 'groupchat':
  reply(t, s, common_commands_sent_msg)



def handler_help_commands(t, s, p):
 jid = s[0]
 muc = s[1]
 nick = s[2]

 level = get_access_level(jid, muc, nick)

 p = p.strip()

 if p:
#  answer = common_commands_ctg_cmds_msg % p
  cmdlist = []

  for cmd in COMMANDS:
   if not cmd in (load_option(muc, 'disabled') or []):
    if level >= COMMANDS[cmd]['acs']:
     for ctg in COMMANDS[cmd]['ctg']:
      if ctg == p:
       cmdlist.append(cmd)

## Вариант команда - описание:
#      i = 0
#      if i > 0:
#       answer += ', '
#      answer += cmd + '\t- ' + COMMANDS[cmd]['dsc']
#      i += 1

#  answer = u'Список команд в категоии ' + p + ':\n' +  ', '.join(cmdlist.keys())

  print cmdlist

  cmdlist.sort()
  if not cmdlist == []:
   answer = common_commands_ctg_cmds0_msg + p + common_commands_ctg_cmds1_msg + ', '.join(cmdlist)

  else:
   answer = common_commands_ctg_not_found_msg

 else:
  ctglist = []

  for cmd in COMMANDS:
#   if not cmd in (load_option(muc, 'disabled') or []):				# спорный пункт
   if level >= COMMANDS[cmd]['acs']:
    for ctg in COMMANDS[cmd]['ctg']:
     if not ctg in ctglist:
      ctglist.append(ctg)

  ctglist.sort()
  print ctglist
  answer = common_commands_ctg_list_msg % ', '.join(ctglist)

 reply('chat', s, answer)

 if t == 'groupchat':
  reply(t, s, common_commands_sent_msg)


register_command_handler(handler_help_command, u'.команда', [], u'Показывает основную справку или информацию об определённой команде.', u'.команда <команда>', 0, True)
register_command_handler(handler_help_commands, u'.команды', [], u'Показывает список всех категорий команд. При запросе категории показывает список команд находящихся в ней.', u'.команды [категория]', 0, True)
