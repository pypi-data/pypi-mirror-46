
import logging
from mixlight.mixlight_entity import mixlight_Entity

PLATFORM = 'climate'

PAYLOAD_CONFIG = '{"name": "%s", "unique_id": "%s.%s", "state_topic": "%s", "command_topic": "%s", "device": %s  }'
PAYLOAD_STATE = '%s'


class virtual_Climate(mixlight_Entity):

  def __init__(self, id, addr, name, type, universe, params):
    mixlight_Entity.__init__(self, id, addr, name, type, universe, 'virtual')

  def check(self):
    #print(self.id, ' check')
    pass