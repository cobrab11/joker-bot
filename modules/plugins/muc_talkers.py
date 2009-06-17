# -*- coding: utf-8 -*-

### LANGPACK ###

muc_talkers_list_msg = u'\nБОЛТУНЫ:'
muc_talkers_empty_msg = u'База болтунов пуста'
muc_talkers_cleared_msg = u'База болтунов очищена'
muc_talkers_item_msg = u'\n%d. %s: %d слов, %d фраз'

################

MUC_TALKERS_LIMIT = 10
talkers_clear_key = u'болтуны'

try: CLEANERS
except NameError: CLEANERS = {}

CLEANERS[talkers_clear_key] = ['words', 'phrases']

################



def handler_talkers(t, s, p):
 muc = s[1]
 nick = s[2]

 TALKERS = []

 if p:						# если есть параметр
  answer = not_implemented_msg

 else:
  for jid in list_db_nodes(muc):
   words = load_attribute(muc, jid, 'words')
   phrases = load_attribute(muc, jid, 'phrases')

   if words:
    TALKERS.append((words, load_attribute(muc, jid, 'nicks')[0], phrases))

  answer = muc_talkers_list_msg

  if TALKERS:
   TALKERS.sort(reverse=True)	#.reverse()

   for i in range(len(TALKERS)):
    if i > MUC_TALKERS_LIMIT - 1:
     break

    answer += muc_talkers_item_msg % ((i+1), TALKERS[i][1], TALKERS[i][0], TALKERS[i][2])

  else:
   answer = muc_talkers_empty_msg

 reply(t, s, answer)



def handler_message_talkers(t, s, b):
 jid = s[0]
 muc = s[1]
 nick = s[2]

 if not is_muc(muc):
  return

 if t == 'chat':			# не считать слова в приват
  return

 if b.split()[0] in COMMANDS:		# команды не считаем
  return

 if not jid:				# не считаем темы
  return

 words = load_attribute(muc, jid, 'words') or 0
 phrases = load_attribute(muc, jid, 'phrases') or 0

 words += len(b.split())
 phrases += 1

# if b.strip() == '+1':				# репутация (плюсадины)
#  rpt += 1

 save_attribute(( (muc, jid, 'words', words), (muc, jid, 'phrases', phrases) ))



register_command_handler(handler_talkers, u'.болтуны', [u'конфа', u'все'], u'Выводит список %d самых активных пользователей. Для очистки используйте команду ".очистить %s"' % (MUC_TALKERS_LIMIT, talkers_clear_key), u'.болтуны')
register_message_handler(handler_message_talkers)
