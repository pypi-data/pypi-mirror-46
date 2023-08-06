from bubot.devices.ModbusSlave.ModbusSlave import ModbusSlave
from bubot.devices.ThermostatSML1000.__init__ import __version__ as device_version
from bubot.devices.ThermostatSML1000.lib.ThermostatSML1000 import ThermostatSML1000 as ModbusDevice
# import logging

# _logger = logging.getLogger(__name__)


class ThermostatSML1000(ModbusSlave):
    ModbusDevice = ModbusDevice
    version = device_version
    file = __file__

    async def on_retrieve_power(self, message):
        res = await self.modbus.read_param('power')
        self.set_param('/power', 'value', res)
        return self.get_param('/power')

    async def on_update_power(self, message):
        value = message.cn.get('value')
        if value is not None:
            value = message.cn['value']
            await self.modbus.write_param('power', value)
        self.update_param('/power', None, message.cn)
        return self.get_param('/power')

    async def on_idle(self):
        try:
            res = await self.modbus.read_param('power')
            self.set_param('/power', 'value', res)
        except Exception as err:
            self.log.error(err)
