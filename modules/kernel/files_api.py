# -*- coding: utf-8 -*-

################################################################################

mutex = threading.Lock()

### FILE FUNCTIONS #############################################################

def file_write(filename, data):
 mutex.acquire()

 if not os.path.exists(filename):
  path_init(filename)

 f = open(filename, 'w')
 f.write(data)
 f.close()
 mutex.release()



def file_read(filename):
 if not os.path.exists(filename):
  return None

 f = open(filename, 'r')
 data = f.read()
 f.close()

 return data



def file_append(filename, data):
 mutex.acquire()
 f = open(filename, 'a')
 f.write(data)	# .encode('utf-8')
 f.close()
 mutex.release()



def path_init(filename):
 dir = os.path.dirname(filename)

 if dir:
  try:
   os.makedirs(dir, mode = 0777)

  except OSError, err:
   if err.errno != errno.EEXIST or not os.path.isdir(dir):
    raise
