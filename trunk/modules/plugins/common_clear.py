# -*- coding: utf-8 -*-

### LANGPACK ###

common_clear_list_msg = u'Доступны следующие банки памяти:\n'
common_clear_not_found_msg = u'Банк %s осуствует'
common_clear_done_msg = u'Выполнено!'

################

try: CLEANERS
except NameError: CLEANERS = {}

#CLEANERS[u'всё']



def handler_clear(t, s, p):
 muc = s[1]
 nick = s[2]

 p = p.strip()

 if p:
  if p in CLEANERS:
   for jid in list_db_nodes(muc):
    for i in range(0, len(CLEANERS[p])):
     save_attribute(( (muc, jid, CLEANERS[p][i], None), ))

   answer = common_clear_done_msg

  else:
   answer = common_clear_not_found_msg % p

 else:
  banks = CLEANERS.keys()
  answer = common_clear_list_msg + ', '.join(banks)

 reply(t, s, answer)



register_command_handler(handler_clear, u'.очистить', [u'админ',u'все'], u'Очищает банки памяти (криво звучит, но лучше пока не придумал)', u'.очистить [база]', 15)