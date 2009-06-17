# -*- coding: utf-8 -*-

### CONNECTION #################################################################

def connect():
 global jcon

 if DEBUG:
  jcon = xmpp.Client(server=SERVER, port=PORT)

 else:
  jcon = xmpp.Client(server=SERVER, port=PORT, debug=[])

 log('\nConnection...')

 if not jcon.connect():
  log("COULDN'T CONNECT")
  time.sleep(30)
  sys.exit(1)

 else:
  log('Connection established...')
  log('Using ' + jcon.isConnected().upper())

 log('\nAuthentication...')
 auth = jcon.auth(USERNAME, PASSWORD, RESOURCE, sasl=1)

 if not auth:
  log('Authentication error!\nError: ')
  log(jcon.lastErr)
  log(jcon.lastErrCode)
  time.sleep(15)
  sys.exit(1)

 else:
  log('Authentication passed...')

 if auth != 'sasl':
  log('Warning: unable to perform SASL auth. Old authentication method used!')


 jcon.RegisterHandler('message', message_handler)
 jcon.RegisterHandler('presence', presence_handler)
 jcon.RegisterHandler('iq', iq_handler)
 jcon.RegisterDisconnectHandler(disconnect_handler)
 jcon.UnregisterDisconnectHandler(jcon.DisconnectHandler)
 log('Handlers registered...')

 log('Sending presence...\n')
 jcon.sendInitPresence(requestRoster=0)

 STAT['start'] = time.time()

 join_all()

 log('\nReady...\n')

 while True:
  jcon.Process(10)



def disconnect(prs=None):
 print 'call_disconnect'
# call_stop_handler()
 leave_all(prs)
 time.sleep(1)
 presence = xmpp.Presence(typ = 'unavailable')
 if prs:
  presence.setStatus(prs)

 jcon.send(presence)



def restart(prs=None):
 disconnect(prs)
				# сюда неплохо бы втиснуть очистку памяти
 time.sleep(3)
 cmd = RESTART_CMD
 log('Restarting: %s' % (cmd, ))
# os.execv(cmd.split()[0], tuple(cmd.split()))
 os.execv(cmd, sys.argv)



def stop(prs=None):		# нужно ли None ???
 disconnect(prs)
 time.sleep(3)
 os._exit(0)
