from bme280.sensorconfig import SensorConfig, OperationMode, OversamplingMode
import smbus2
import time

_CHIP_ID_REG = 0xD0
_RESET_REG = 0xE0
_RESET_KEYWORD = 0xB6


class BME280:
    __slots__ = (
        "_i2c_address",
        "_smbus",
        "_sensor_config",
        "_chip_id"
    )

    _i2c_address: int
    _smbus: smbus2.SMBus
    _sensor_config: SensorConfig
    _chip_id: int

    def __init__(self,
                 i2c_address: int,
                 i2c_port: int,
                 sensor_config: SensorConfig = SensorConfig()
                 ) -> None:

        if type(i2c_address) is not int or i2c_address < 0:
            raise ValueError("i2c_address should be a positive integer!")
        if type(i2c_port) is not int or i2c_port < 0:
            raise ValueError("i2c_port should be a positive integer!")
        if type(sensor_config) is not SensorConfig:
            raise ValueError("sensor_config should be a SensorConfig object!")

        self._i2c_address = i2c_address
        self._smbus = smbus2.SMBus(i2c_port)
        self._sensor_config = sensor_config

        self._chip_id = self._smbus.read_byte_data(self._i2c_address, _CHIP_ID_REG)
        self._init_sensor()

    def _init_sensor(self) -> None:
        self._reset_sensor()

    def _reset_sensor(self) -> None:
        self._write_register(_RESET_REG, _RESET_KEYWORD)
        time.sleep(0.002)  # Wait for the IC to start up (2ms)

    def _write_register(self, register: int, data: int):
        address = self._i2c_address
        self._smbus.write_byte_data(address, register, data)

    def chip_id(self) -> int:
        return self._chip_id
