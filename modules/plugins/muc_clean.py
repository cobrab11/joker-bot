# -*- coding: utf-8 -*-

### LANGPACK ###

muc_clean_list_msg = ('а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т')
muc_clean_done_msg = u'Выполнено!'

################



def handler_clean(t, s, p):
 muc = s[1]
 nick = s[2]

 abc = muc_clean_list_msg

 for x in range(0, 20):
  reply('groupchat', [None, muc, None], unicode(abc[x], 'utf-8'))

 reply(t, s, muc_clean_done_msg)



register_command_handler(handler_clean, u'.очистка', [u'конфа',u'все'], u'Очищает конференцию (считает до 20).', u'.очистка', 15)