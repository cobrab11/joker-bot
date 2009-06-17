import os
import errno
import threading



class fs:

 """simple file api class"""

 def __init__(self, filename):
  self.f = filename
  self.mutex = threading.Lock()



 def write(self, data):
  self.mutex.acquire()

  if not os.path.exists(self.f):
   self.init()

  f = open(self.f, 'w')
  f.write(data)
  f.close()
  self.mutex.release()



 def read(self):
  if not os.path.exists(self.f):
   return None

  f = open(self.f, 'r')
  data = f.read()
  f.close()

  return data



 def append(self, data):
  self.mutex.acquire()
  f = open(self.f, 'a')
  f.write(data)
  f.close()
  self.mutex.release()



# def execute(self):
#  cfg = unicode((self.read() or ''), 'utf-8')
#  exec cfg in globals()



 def init(self):
  dir = os.path.dirname(self.f)

  if dir:
   try:
    os.makedirs(dir, mode = 0777)

   except OSError, err:
    if err.errno != errno.EEXIST or not os.path.isdir(dir):
     raise
