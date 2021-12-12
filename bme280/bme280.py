from sensorconfig import SensorConfig, OperationMode, OversamplingMode
import smbus

_CHIP_ID_REG = 0xD0


class BME280:
    __slots__ = (
        "_i2c_address",
        "_smbus",
        "_sensor_config",
        "_chip_id"
    )

    _i2c_address: int
    _smbus: smbus.SMBus
    _sensor_config: SensorConfig
    _chip_id: int

    def __init__(self,
                 i2c_address: int,
                 i2c_port: int,
                 sensor_config: SensorConfig = SensorConfig()
                 ) -> None:

        if i2c_address is not int or i2c_address < 0:
            raise ValueError("i2c_address should be a positive integer!")
        if i2c_port is not int or i2c_port < 0:
            raise ValueError("i2c_port should be a positive integer!")
        if sensor_config is not SensorConfig:
            raise ValueError("sensor_config should be a SensorConfig object!")

        self._i2c_address = i2c_address
        self._smbus = smbus.SMBus(i2c_port)
        self._sensor_config = sensor_config

        self._chip_id = self._smbus.read_byte_data(self._i2c_address, _CHIP_ID_REG)
        self._init_sensor()

    def _init_sensor(self) -> None:
        pass

    def _reset_sensor(self) -> None:
        pass

    def chip_id(self) -> int:
        return self._chip_id
