# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser

class HTML_parser(HTMLParser):

 def handle_starttag(self, tag, attrs):
  global pos
  if tag == 'div' and attrs == '':
   print "beginning of a %s tag" % tag
#   print attrs
#   print self.getpos()

 def handle_endtag(self, tag):
  if tag == 'div':
   t = self.get_starttag_text()
   print "end of a %s tag" % tag
#   print self.getpos()
   print t

 def handle_startendtag(self, tag, attrs):
  print 'STARTEND'