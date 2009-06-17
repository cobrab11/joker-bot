# -*- coding: utf-8 -*-

# from html_parser import HTML_parser
import urllib2, re, urllib
from re import compile # as re_compile

#strip_tags = re_compile(r'<[^<>]+>')



search_string = '[:||||:]'
pattern = re.compile(r'<div>.+</div>')
pattern_i = re.compile(r'<a href="/quote/\d+/bayan"')


def handler_bashorgru_get(t, s, p):
 if not p.strip():
  req = urllib2.Request('http://bash.org.ru/random')

 else:
  req = urllib2.Request('http://bash.org.ru/quote/' + p.strip())
  req.add_header = ('User-agent', 'Mozilla/5.0')

# try:
 r = urllib2.urlopen(req)

 body = r.read()	#[:5000]



# body = file_read('./docs/bash.org.ru.html')



# HTML_parser().feed(body)
# HTML_parser().close()
# log(body, 1)

 n = random.randrange(0, 49)
 print n

# q = re.search(re.compile(r'<div>.+</div>'), body)
# print q.group(0)
# log(str(q.groups()), 1)

# q = re.findall(re.compile(r'<div class="q">.+<hr class="iq">'), body)
# q = re.findall(re.compile(r'<a.*\[:\|\|\|\|\:]</a>'), body)
 q = re.findall(pattern, body)
 qi = re.findall(pattern_i, body)
 print len(q)
 print len(qi)
# log(str(q), 1)

 quote = '\n' + decode(q[n]).strip() #.encode('utf-8')
# log(quote)

# log(q[n], 1)
 reply(t, s, unicode(quote,'windows-1251'))



def decode(text):
# return strip_tags.sub('', text.replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')
 return text.replace('<br>','\n').replace('<br />','\n').replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('<div>','').replace('</div>','')



register_command_handler(handler_bashorgru_get, u'.баш', [u'сервис', u'все'], u'Показывает случайную цитату с сайта bash.org.ru. Также может по заданному номеру вывести.', u'.баш <номер>', 1, True)
#register_command_handler(handler_bashorgru_abyss_get, u'.бездна', [u'сервис', u'все'], u'Показывает случайную цитату из Бездны (bash.org.ru).', u'.бездна', 1, True)
