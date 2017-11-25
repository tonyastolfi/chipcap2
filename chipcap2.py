#!/usr/bin/python
import smbus
import logging

address = 0x28
data_fetch = 0x80 | address

class Sensor:
    def __init__(self, i2c_bus):
        self._bus = smbus.SMBus(i2c_bus)
    
    def read(self):
        self._data = self._bus.read_i2c_block_data(address, data_fetch)
        self.rh = float(((self._data[0] & 0x3f) << 8) | (self._data[1] & 0xff)) * 100.0 / 16384.0
        self.tempC = float((self._data[2] << 6) | ((self._data[3] & 0xfc) >> 2)) * 165.0 / 16384.0 - 40.0
        self.tempF = self.tempC * 9./5. + 32.
        return self.rh, self.tempF

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._bus.close()
        logging.info('closed the bus')


if __name__ == "__main__":
    s = Sensor(1)
    rh, tempF = s.read()
    print 'rh {}'.format(rh)
    print 'tempF {}'.format(tempF)
    print 'tempC {}'.format(s.tempC)
    print 'raw_chipcap2_data {}'.format(s._data)
