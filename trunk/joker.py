# -*- coding: utf-8 -*-

#
# Copyright © Jack Krieger 2009
#
# jack.krieger@gmail.com
#
# This software provided under GPL2
#



from __future__ import with_statement

import sys
import os
import codecs
import errno
import random
import time
import threading
import types

sys.path.insert(0, 'lib')

import xmpp
#from api import *

################################################################################

work = os.path.dirname(sys.argv[0])
if not work: work = '.'
os.chdir(work)

################################################################################

__bot_name__ = 'JoKeR'
__bot_ver__ = '0.3.1.2'

### CONSTANTS ##################################################################

CONFIG = 'joker.cfg'
LOGFILE = 'joker.log'

ACS = './data/accesslist.cfg'
MUC = './data/muclist.cfg'

path_kernel = './modules/kernel/'			# вынести в функцию загрузки модулей
path_plugins = './modules/plugins/'

### GLOBAL VARIABLES ###########################################################



instance_control = threading.BoundedSemaphore(value = 100)

#ACCESSLIST = {}
#MUCLIST = {}

AFFILIATIONS = {'none': 1, 'member': 10, 'admin': 30, 'owner': 40}
ROLES = {'none': 0, 'visitor': 0, 'participant': 5, 'moderator': 15}

STAT = {}

### MAIN #######################################################################

def main():
 pass


### START ######################################################################

if __name__ == '__main__':

 try:
  process = True			# флаг НЕзавершения работы

  for p in os.listdir(path_kernel):
   if p.endswith('.py'):
    f = file(path_kernel + p, 'r')
    exec f.read() in globals()
    f.close()

  log_purge()
  log('-=START=-\n')

#  if LOG:
#   threading.Thread(None, thread_log, 'LogThread', ()).start()			# создание поток лога

  exec unicode((file_read(CONFIG) or ''), 'utf-8') in globals()
  log('CONFIG loaded...')

  exec unicode((file_read('./language/' + LANG + '.txt') or ''), 'utf-8') in globals()

  MUCLIST = eval(file_read(MUC) or '{}')

  ACCESSLIST = eval(file_read(ACS) or '{}')

  for jid in ADMINS:
   ACCESSLIST[jid.lower()] = 100

  log('\nLoading plugins:\n')
  for p in os.listdir(path_plugins):
   if p.endswith('.py'):
    log(p + ':')

    if DEBUG_PLUGINS:
     exec file_read(path_plugins + p) in globals()

    else:
     try:
      exec file_read(path_plugins + p) in globals()

     except:
      print '\t<plugin broken>'
 
  log('\nPlugins loaded...\n')

  connect()

 except KeyboardInterrupt:
  log('INTERRUPT')
  process = False
  # обработка завершения работы
  sys.exit(0)
