# -*- coding: utf-8 -*-

### LANGPACK ###

muc_greetings_list_msg = u'\nСписок приветствий:'
muc_greetings_list_item_msg = u'\n%s = %s'
muc_greetings_not_set_msg = u'Приветствие не установлено'
muc_greetings_deleted_msg = u'Приветствие удалено'
muc_greetings_added_msg = u'Приветствие установлено'
muc_greetings_no_greets_msg = u'Приветствия не установлены'
muc_greetings_not_implemented_msg = u'Функция приветствия с правами пользователя временно недоступна'
muc_greetings_sent_msg = u'Отправлено в приват'
muc_greetings_common_msg = u'Общее приветствие:\n%s'
muc_greetings_common_set_msg = u'Общее приветствие сохранено'
muc_greetings_common_not_set_msg = u'Общее приветствие не установлено'

################

greetings_clear_key = u'приветствия'

try: CLEANERS
except NameError: CLEANERS = {}

CLEANERS[greetings_clear_key] = ['greet']

################

def handler_join_greet(jid, muc, nick, aff, role):
 if time.time() - STAT['start'] > 5:			# не приветствовать первые 5 секунд
  time.sleep(1)

  greet = load_attribute(muc, jid, 'greet')

  if greet:
   reply('groupchat', [None, muc, None], nick + '> ' + greet)

  else:
   if nick == get_own_nick(muc):
    return

   if not load_attribute(muc, jid, 'greeted'):			# если человек впервые заходит в конфу
    greet = load_option(muc, 'greet')
    save_attribute(( (muc, jid, 'greeted', True), ))			# пишем, что этого уж приветствовали

    reply('chat', [None, muc, nick], greet)



def handler_greet(t, s, p):
 muc = s[1]
 nick = s[2]
 answer = u'Ы'

 if p:
  p = string_split(p, '=')

  print p

  if len(p) == 2:				# если присутствует '='
   target = p[0].strip()
   greet = p[1].strip()

   print target, greet

   if target:
    jid = get_jid(muc, target)

#    print target, jid

    if jid:
     if greet.strip() == '':					# если нет текста приветствия - удаляем
      if load_attribute(muc, jid, 'greet'):
       save_attribute(( (muc, jid, 'greet', None), ))
       
       answer = muc_greetings_deleted_msg

      else:
       answer = muc_greetings_not_set_msg

     else:						# если есть текст приветствия - добавляем
      if greet[:1] == ' ':			# если пробел впереди приветствия, удаляем
       greet = greet[1:]

      save_attribute(( (muc, jid, 'greet', greet), ))

      answer = muc_greetings_added_msg

    else:
     answer = core_not_in_muc_msg % target

   else:
    answer = syntax_error_msg

  else:
   answer = syntax_error_msg

 else:
  answer = syntax_error_msg

 reply(t, s, answer)



def handler_greets(t, s, p):
 muc = s[1]
 nick = s[2]
 answer = muc_greetings_list_msg

 if not p:
  for jid in list_db_nodes(muc):
   greet = load_attribute(muc, jid, 'greet')

   if greet:
    answer += muc_greetings_list_item_msg % (jid, greet)

  if answer == muc_greetings_list_msg:
   answer = muc_greetings_no_greets_msg

 else:
  answer = syntax_error_msg

 reply('chat', s, answer)

 if t == 'groupchat':
#  reply('groupchat', [None, muc, None], muc_greetings_sent_msg)
  reply('groupchat', s, muc_greetings_sent_msg)



def handler_greet_all(t, s, p):
 muc = s[1]

 p = p.strip()

 if p:
  if p.startswith('='):				# если первый символ - "="
   print p
   greet = p[1:].strip()
   save_option(( (muc, 'greet', greet), ))
   answer = muc_greetings_common_set_msg

  else:
   answer = core_syntax_error_msg

 else:
  greet = load_option(muc, 'greet')

  if greet:
   answer = muc_greetings_common_msg % (greet, )

  else:
   answer = muc_greetings_common_not_set_msg

 reply(t, s, answer)




register_command_handler(handler_greet, u'.приветствие', [u'конфа', u'все'], u'Добавляет приветствие для определённого ника или джида.', u'.приветствие [ник/джид] = текст приветствия', 30)
register_command_handler(handler_greets, u'.приветствия', [u'конфа', u'все'], u'Выводит список всех приветствий.', u'.приветствия', 30)
register_command_handler(handler_greet_all, u'.привет', [u'конфа', u'все'], u'Добавляет приветствие для новых пользователей.', u'.привет = текст приветствия', 30)
register_join_handler(handler_join_greet)
