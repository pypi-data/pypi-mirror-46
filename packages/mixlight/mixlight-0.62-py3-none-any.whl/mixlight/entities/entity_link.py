

import logging
from mixlight.mixlight_entity import mixlight_Entity

class entity_Link(mixlight_Entity):

  def __init__(self, id, addr, nr, name, type, universe):
    mixlight_Entity.__init__(self, id, addr, name, type, universe, 'hidden')
    
  def create(self):
    pass

  def delete(self):
    pass

  def get(self):
    pass
    
  def set(self, *data):
    pass

  def read(self, topic, values):
    pass

  def write(self):
    print(self.id, ' toggled ', self.name)
    if self.name in self.linker.entities:
      self.linker.entities[self.name].toggle(self.id)
        