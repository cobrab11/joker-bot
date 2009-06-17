# -*- coding: utf-8 -*-

### HANDLERS ###################################################################

def disconnect_handler():		# че то не работает
 log('DISCONNECTED')

 if AUTO_RESTART:
  log('WAITING FOR RESTART...')
  time.sleep(10)
  log('RESTARTING')
  restart()

 else:
  sys.exit(0)
