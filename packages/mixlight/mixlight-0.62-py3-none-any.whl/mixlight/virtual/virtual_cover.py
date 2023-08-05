

import logging
import sys, time
from mixlight.mixlight_entity import mixlight_Entity

PLATFORM = 'cover'

PAYLOAD_CONFIG = '{"name": "%s", "unique_id": "%s.%s", "state_topic": "%s", "command_topic": "%s", "state_open":"OPEN", "state_closed":"CLOSE", "device": %s  }'
PAYLOAD_STATE = '%s'

PAYLOAD_OPEN = 'OPEN'
PAYLOAD_CLOSE = 'CLOSE'
PAYLOAD_STOP = 'STOP'

class virtual_Cover(mixlight_Entity):

  def __init__(self, id, addr, name, type, universe, params):
    mixlight_Entity.__init__(self, id, addr, name, type, universe, 'virtual')
    self.topic_config = self.linker.buildTopic(PLATFORM, id, "config")
    self.topic_state = self.linker.buildTopic(PLATFORM, id, "state")
    self.topic_set = self.linker.buildTopic(PLATFORM, id, "set")

    self.state  = PAYLOAD_OPEN   # open
    self.future_state = self.state

    self.auto_stop_time = sys.maxsize
    self.sensor = params.get('sensor')
    self.open = params.get('open')
    self.close = params.get('close')
    self.open_input = params.get('open_input')
    self.close_input = params.get('close_input')
    self.delay = params.get('delay')

  def create(self):
    if self.linker.client is None:
      return
    self.link(self.open_input)
    self.link(self.close_input)
    payload = PAYLOAD_CONFIG % (self.name, PLATFORM, self.id, self.topic_state, self.topic_set, self.device_info)
    rc = self.linker.client.publish(self.topic_config, payload, 1, True)
    rc.wait_for_publish()
    self.linker.client.will_set(self.topic_config, None, 1, True)
    rc = self.linker.client.subscribe(self.topic_set)
    print (self.id, ' CREATE: ', payload)
    self.write()
    
  def delete(self):
    if self.linker.client is None:
      return
    self.linker.client.unsubscribe(self.topic_set)
    rc = self.linker.client.publish(self.topic_config, None, 1, True)
    rc.wait_for_publish()
    #rc = self.linker.client.publish(self.topic_state, None, 1, True)
    #rc.wait_for_publish()
    print (self.id, ' DELETE: ')
    
  def get(self):
    return self.state
    
  def set(self, *data):
    if data[0] == self.future_state:
      return
    if data[0] != self.get():
      self.stop()
      if data[0] != PAYLOAD_STOP:
        self.move(data[0])
      else:
        self.future_state = self.state
        self.write()

  def read(self, topic, values):
    if self.linker.client is None:
      return
    if topic == self.topic_set:  
      self.set(values)

  def write(self):
    if self.linker.client is None:
      return
    self.linker.client.publish(self.topic_state, self.get(), 1, True)
    print('WRITE:', self.topic_state, self.get())
        
  def toggle(self, id):
    if id == self.open_input:
      self.set(PAYLOAD_OPEN)
    elif id == self.close_input:
      self.set(PAYLOAD_CLOSE)
    else: 
      pass

  def check(self):
    if time.time() > self.auto_stop_time:
      self.state = self.future_state
      self.auto_stop_time = sys.maxsize
      self.stop()
      self.write()

  def stop(self):
    self.command(self.open, 0)
    self.command(self.close, 0)
    self.auto_stop_time = sys.maxsize

  def move(self, state):
    self.future_state = state
    self.auto_stop_time = time.time() + self.delay
    if (self.future_state == PAYLOAD_OPEN):
      self.command(self.open, 255)
    else:
      self.command(self.close, 255)

  def command(self, id, value):
    entity = self.linker.entities[id]
    if entity is not None:
      entity.set(value)

  def link(self, id):
    if id in self.linker.entities:
      entity = self.linker.entities[id]
      if entity is not None:
        entity.name = self.id
