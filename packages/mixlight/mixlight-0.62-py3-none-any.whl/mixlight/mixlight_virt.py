

import logging
import  sys, time, threading, _thread, traceback


class mixlight_Virtual(threading.Thread):

  def __init__(self, link, debug):
    threading.Thread.__init__(self)
    self.linker = link
    self.debug = debug

    # prepare to run
    self.running = False

  def run(self):
    self.running = True
    logging.info('Starting MIXLIGHT Universe Virtual')
    st = time.time()
    i = 0
    while self.running:
      try:
        if not self.isAlive() or not self.running: break
        virtCache = self.linker.entities
        for addr in virtCache:
          entity = virtCache[addr]
          if entity.isVirtual(): 
            entity.check()
        time.sleep(0.5)
      except Exception as e:
        print("Error in thread mixlight_VIRT: ", e)        
        traceback.print_exc()
      i += 1
    logging.info('MIXLiGHT achieved framerate %s: %s' % (self.name, i / (time.time() - st)))
    logging.info('Stopped MIXLIGHT Universe Virtual')

  def stop(self):
    self.running = False
    self.join()

