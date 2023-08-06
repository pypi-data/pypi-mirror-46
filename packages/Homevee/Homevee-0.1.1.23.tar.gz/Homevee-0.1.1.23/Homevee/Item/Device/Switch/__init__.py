from Homevee.Exception import AbstractFunctionCallException
from Homevee.Item.Device import Device


class Switch(Device):
    def __init__(self, name, icon, location, id=None, mode=False):
        super(Switch, self).__init__(name, icon, location, id=id)

        if mode == 1:
            self.mode = True
        else:
            self.mode = False

    def set_mode(self, mode, db=None):
        #TODO sicherstellen, dass mode immer boolean ist (Ticket #26)
        if mode == "1" or mode == 1 or mode == True:
            mode = True
        else:
            mode = False

        if(self.update_mode(mode, db)):
            self.mode = mode
            self.save_to_db(db)

    def update_mode(self, mode, db=None):
        raise AbstractFunctionCallException("Switch.update_mode() is abstract")

    #@staticmethod
    #def get_all(location=None, db=None):
    #    # get all devices of all types
    #    devices = []
    #    devices.extend(Switch.get_all(location, db))
    #    return devices