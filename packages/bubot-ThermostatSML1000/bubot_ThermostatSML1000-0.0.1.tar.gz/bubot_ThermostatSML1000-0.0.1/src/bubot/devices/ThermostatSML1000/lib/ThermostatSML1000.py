from aio_modbus_client.ModbusDevice import ModbusDevice
from aio_modbus_client.DataFormatter import DataFormatterInteger


class ThermostatSML1000(ModbusDevice):
    file = __file__

    def __init__(self, address, protocol, **kwargs):
        self.formatter['decimal05'] = FormatterDecimal05
        self.formatter['boolean5a'] = FormatterBoolean5a
        super().__init__(address, protocol, **kwargs)

    pass


class FormatterDecimal05(DataFormatterInteger):

    @classmethod
    def encode(cls, device, param, value):
        return value * 2
        # return value.to_bytes(cls.get_register_count(device, param), byteorder=param.get('reg_byteorder', 'big'))

    @classmethod
    def decode(cls, device, param, value):
        return int.from_bytes(value, byteorder=param.get('reg_byteorder', 'big')) / 2


class FormatterBoolean5a(DataFormatterInteger):

    @classmethod
    def encode(cls, device, param, value):
        return 0xA5 if value else 0x5A
        # return value.to_bytes(cls.get_register_count(device, param), byteorder=param.get('reg_byteorder', 'big'))

    @classmethod
    def decode(cls, device, param, value):
        value = int.from_bytes(value, byteorder=param.get('reg_byteorder', 'big'))
        if value == 0xA5:
            return True
        elif value == 0x5A:
            return False
        else:
            return Exception('Illegal value {}'.format(value))
