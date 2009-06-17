# -*- coding: utf-8 -*-

### LANGPACK ###

muc_define_not_found_msg = u'Определение %s отсуствует'
muc_define_def_msg = u'Список определений:\n'
muc_define_no_def_msg = u'Нет определений'
muc_define_done_msg = u'Записано'
muc_define_deleted_msg = u'Определение %s удалено'

################

define_clear_key = u'определения'

try: CLEANERS
except NameError: CLEANERS = {}

CLEANERS[define_clear_key] = ['def']

################



def handler_define(t, s, p):
 jid = s[0]
 muc = s[1]
 nick = s[2]

 if p:
  p = string_split(p, '=')

  key = p[0]
  definitions = load_option(muc, 'def') or {}

  if len(p) == 2:				# если присутствует '='
   if get_access_level(jid, muc, nick) >= AFFILIATIONS['admin']:
    definition = string_strip(p[1])

    if key:
     if definition:					# присвоение
      definitions[key] = definition
      answer = muc_define_done_msg

     else:						# удаление
      if key in definitions:
       del definitions[key]
       answer = muc_define_deleted_msg % (key,)

      else:
       answer = muc_define_not_found_msg % (key,)

     save_option(( (muc, 'def', definitions), ))

    else:
     answer = core_syntax_error_msg

   else:
    answer = core_access_denied_msg

  else:						# если нет присвоения (нет символа '=')
   if not definitions:
    answer = muc_define_no_def_msg

   if key in definitions:
    answer = definitions[key]

   else:
    answer = muc_define_not_found_msg % (key,)

 else:
  definitions = load_option(muc, 'def')

  if not definitions:
   answer = muc_define_no_def_msg

  else:
   answer = muc_define_def_msg + ', '.join(definitions.keys())

 reply(t, s, answer)



#register_command_handler(handler_define, u'.определение', [u'сервис', u'все'], u'Записывает определение ключевого слова. Без параметра выводит список записанных определений. Для удаления определения присвойте ему пустое значение.', u'.определение [слово = определение]')
register_command_handler(handler_define, u'.о', [])
