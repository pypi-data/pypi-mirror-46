

import logging



class mixlight_Entity():

  def __init__(self, id, addr, name, type, universe, device_type):
    self.id = id
    self.addr = addr
    self.name = name
    self.linker = universe.linker
    self.type = type
    self.device_type = device_type
    self.device_info = self.linker.buildDeviceInfo(id, name, device_type, universe.name)

  def isVirtual(self):
    return self.device_type == 'virtual'

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
    pass

  def toggle(self):
    pass
