# -*- coding: utf-8 -*-

# автор - ferym@jabbim.org.ru
# по вопросам обращаться в support@conference.veganet.org.ru
# web site: http://veganet.org

def handler_afor(type, source, parameters):
    try:
        if parameters.strip() != '':
            reply(type, source, eval(parameters.strip()))
        else:
            r = urllib2.urlopen(req)
    except:
        req = urllib2.Request('http://veselchak.net/cgi-bin/inf.cgi?t=1')
        req.add_header = ('User-agent', 'Mozilla/5.0')
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<p>',target)
        message = target[od.end():]
        message = message[:re.search('<a',message).start()]
        message = message.strip()
        message = decode(message)
        reply(type, source, unicode(message,'windows-1251'))
                  
def decode(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n'))

register_command_handler(handler_afor, u'.афоризм', [u'сервис', u'все'], u'показывает случайный афоризм с veselchak.net\nby ferym', u'.афоризм', 1, True)