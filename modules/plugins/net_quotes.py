# -*- coding: utf-8 -*-

### LANGPACK ###

net_quotes_empty_msg = u'База афоризмов пуста'

################

quotes_file = './data/static/quotes.txt'

################

def handler_quote(t, s, p):

 answer = 'error'

 if not p:
  if os.path.exists(quotes_file):
   quotes = open(quotes_file)

   lines = quotes.readlines()
   quotes.close()

   count = len(lines) - 1

   if count >= 0:
    i = random.randrange(0, count)

    answer = unicode(lines[i],'utf-8')

   else:
    answer = net_quotes_empty_msg

  else:
   answer = net_quotes_empty_msg

 else:
  answer = syntax_error_msg

 reply(t, s, answer)



#register_command_handler(handler_quote, u'.афоризм', [u'сервис', u'все'], u'Показывает случайный афоризм.', u'.афоризм', 1, True)
register_command_handler(handler_quote, u'.аф', [u'сервис', u'все'], u'Показывает случайный афоризм.', u'.аф', 1, True)
