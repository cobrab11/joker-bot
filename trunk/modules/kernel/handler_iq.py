# -*- coding: utf-8 -*-

### HANDLERS ###################################################################

def iq_handler(con, iq):		#from Talisman
# global jcon
 s = iq.getFrom()

 print 'iq'

 call_iq_handlers(iq)

 if iq.getTags('ping', {}, 'urn:xmpp:ping') or iq.getTags('query', {}, 'urn:xmpp:ping'):	# второе видимо не по XEPу
  print 'ping_request'
  jcon.send(iq.buildReply('result'))
  raise xmpp.NodeProcessed

 elif iq.getTags('query', {}, xmpp.NS_VERSION):
  print 'os_request'

  result = iq.buildReply('result')
  query = result.getTag('query')
  query.setTagData('name', __bot_name__)
  query.setTagData('version', __bot_ver__)

  if SHARE_OS:
   osname = os.popen('ver')
   osver = osname.read().strip().decode('cp866')
   osname.close()
   pyver = sys.version
   osver = osver + '; Python: ' + pyver
   query.setTagData('os', osver)

  jcon.send(result)
  raise xmpp.NodeProcessed

 elif iq.getTags('time', {}, 'urn:xmpp:time'):
  print 'time'
  tzo=(lambda tup: tup[0]+'%02d:'%tup[1]+'%02d'%tup[2])((lambda t: tuple(['+' if t<0 else '-', abs(t)/3600, abs(t)/60%60]))(time.altzone if time.daylight else time.timezone))
  utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
  result = iq.buildReply('result')
  reply=result.addChild('time', {}, [], 'urn:xmpp:time')
  reply.setTagData('tzo', tzo)
  reply.setTagData('utc', utc)
  jcon.send(result)
  raise xmpp.NodeProcessed

 elif iq.getTags('query', {}, xmpp.NS_DISCO_INFO):
  print 'disco'
  items=[]
  ids=[]
  ids.append({'category':'client','type':'bot','name':'zBot'})
#  features=[xmpp.NS_DISCO_INFO,xmpp.NS_DISCO_ITEMS,xmpp.NS_MUC,'urn:xmpp:time','urn:xmpp:ping',xmpp.NS_VERSION,xmpp.NS_PRIVACY,xmpp.NS_ROSTER,xmpp.NS_VCARD,xmpp.NS_DATA,xmpp.NS_LAST,xmpp.NS_COMMANDS,'msglog','fullunicode',xmpp.NS_TIME]
  features=[xmpp.NS_MUC, 'urn:xmpp:time', 'urn:xmpp:ping', xmpp.NS_VERSION, xmpp.NS_VCARD, xmpp.NS_TIME]
  info={'ids':ids,'features':features}
  b=xmpp.browser.Browser()
  b.PlugIn(jcon)
  b.setDiscoHandler({'items':items,'info':info})

 elif iq.getTags('query', {}, xmpp.NS_TIME):
  print 'time_2'
  timedisp=time.strftime('%a, %d %b %Y %H:%M:%S UTC', time.localtime())
  timetz=time.strftime('%Z', time.localtime())
  timeutc=time.strftime('%Y%m%dT%H:%M:%S', time.gmtime())
  result = xmpp.Iq('result')
  result.setTo(s)
  result.setID(iq.getID())
  query = result.addChild('query', {}, [], 'jabber:iq:time')
  query.setTagData('utc', timeutc)
  query.setTagData('tz', timetz)
  query.setTagData('display', timedisp)
  jcon.send(result)
  raise xmpp.NodeProcessed

 else:
  print 'other_iq'
#  result = iq.buildReply('error')
#  query.setTagData('type', 'cancel')
