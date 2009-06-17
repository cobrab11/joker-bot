# -*- coding: utf-8 -*-

################################################################################

process = True

LOG = False
LogCondition = threading.Condition(threading.Lock())
LOG_QUEUE = []

### LOGGING ####################################################################



def thread_log():						# поток лога
# print threading.currentThread().getName()

 while process:
  LogCondition.acquire()
  while not LOG_QUEUE:
   LogCondition.wait()

  while LOG_QUEUE:
   data = LOG_QUEUE.pop(0)

   if data:
    file_append(LOGFILE, data.encode('utf-8') + '\n')

   print data

  LogCondition.release()



def log(data, mode=None):
 if LOG:
  LOG_QUEUE.append(data)

  LogCondition.acquire()
  LogCondition.notify()
  LogCondition.release()

 else:
  try:
   print data

  except:
   pass



def log_purge():
 try:
  os.remove(log_file)

 except:
  pass
