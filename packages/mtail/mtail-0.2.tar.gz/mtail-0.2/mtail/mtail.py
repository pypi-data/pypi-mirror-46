import time
import sys
import os
import multiprocessing


def tail(fn, sleep=0.1):
  keep_processing = True
  try:
    f = open(fn)
    curino = os.fstat(f.fileno()).st_ino
    f.seek(0, os.SEEK_END)
    while keep_processing:
      line = f.readline()

      if line:
        sys.stdout.write("{}: {}".format(fn, line))
      else:
        time.sleep(sleep)
      
      try:
        if os.stat(fn).st_ino != curino:
          f2 = open(fn)
          f.close()
          f = f2
          curino = os.fstat(f.fileno()).st_ino
      except IOError:
        pass
    f.close()
  except KeyboardInterrupt:
    print("\nClosing {} tail".format(fn))
    keep_processing = False

def mtail():
  try: 
    files = os.listdir('.')
    tails = []
    for fn in files:
      print("<== {} ==>".format(fn))
      if os.path.isdir('./' + fn):
        continue
      p = multiprocessing.Process(target=tail, args=(fn,))
      tails.append(p)
      p.start()
  except KeyboardInterrupt:
    for p in tails:
      p.terminate()