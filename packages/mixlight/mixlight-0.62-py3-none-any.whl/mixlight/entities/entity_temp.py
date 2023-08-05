

import logging
from mixlight.mixlight_entity import mixlight_Entity

PLATFORM = 'sensor'

PAYLOAD_CONFIG = '{"name": "%s", "unique_id": "%s.%s", "state_topic":"%s", "device_class": "temperature", "unit_of_measurement": "°C", "device": %s  }'
PAYLOAD_STATE = '%s'


class entity_Temp(mixlight_Entity):

  def __init__(self, id, addr, name, type, universe):
    mixlight_Entity.__init__(self, id, addr, name, type, universe, '8bths-v2')
    self.topic_config = self.linker.buildTopic(PLATFORM, id, "config")
    self.topic_state = self.linker.buildTopic(PLATFORM, id, "state")

  def create(self):
    if self.linker.client is None:
      return
    payload = PAYLOAD_CONFIG % (self.name, PLATFORM, self.id, self.topic_state, self.device_info)
    rc = self.linker.client.publish(self.topic_config, payload, 1, True)
    rc.wait_for_publish()
    self.linker.client.will_set(self.topic_config, None, 1, True)
    print (self.id, ' CREATE: ', payload)
    self.write()

  def delete(self):
    if self.linker.client is None:
      return
    rc = self.linker.client.publish(self.topic_config, None, 1, True)
    rc.wait_for_publish()
    #rc = self.linker.client.publish(self.topic_state, None, 1, True)
    #rc.wait_for_publish()
    print (self.id, ' DELETE: ')

  def get(self):
    return self.linker.boards[self.addr].temp

  def set(self, *data):
    pass

  def read(self, topic, values):
    pass

  def write(self):
    if self.linker.client is None:
      return
    payload = "0"
    if self.get() > 0:
      payload = str(self.get())
    self.linker.client.publish(self.topic_state, payload, 1, True)
