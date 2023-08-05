

import logging
from mixlight.mixlight_entity import mixlight_Entity


PLATFORM = 'light'

PAYLOAD_CONFIG = '{"name": "%s", "unique_id": "%s.%s", "state_topic":"%s", "command_topic": "%s", "device": %s  }'
PAYLOAD_STATE = '%s'


class entity_Light(mixlight_Entity):

  def __init__(self, id, addr, name, type, universe):
    mixlight_Entity.__init__(self, id, addr, name, type, universe, 'dmx512')
    self.topic_config = self.linker.buildTopic(PLATFORM, id, "config")
    self.topic_state = self.linker.buildTopic(PLATFORM, id, "state")
    self.topic_set = self.linker.buildTopic(PLATFORM, id, "set")
    
  def create(self):
    if self.linker.client is None:
      return
    payload = PAYLOAD_CONFIG % (self.name, PLATFORM, self.id, self.topic_state, self.topic_set, self.device_info)
    rc = self.linker.client.publish(self.topic_config, payload, 1, True)
    rc.wait_for_publish()
    self.linker.client.will_set(self.topic_config, None, 1, True)
    rc = self.linker.client.subscribe(self.topic_set)
    #print(rc)
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
    return self.linker.output.get(self.addr)  
    
  def set(self, *data):
    self.linker.output.set(self.addr, data[0])
    self.write()
    
  def read(self, topic, values):
    if topic == self.topic_set:    
      if values == "ON":
        self.set(255)
      else:
        self.set(0)
    
  def write(self):
    if self.linker.client is None:
      return
    payload = "OFF"
    if self.get() > 0:
      payload = "ON"
    self.linker.client.publish(self.topic_state, payload, 1, True)

  def toggle(self, id):
    if self.get() > 0:
      self.set(0)
    else:
      self.set(255)      
        