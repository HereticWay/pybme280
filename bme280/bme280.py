from sensorconfig import SensorConfig, OperationMode, OversamplingMode
import smbus

_CHIP_ID_REG = 0xD0


class BME280:
    def __init__(self,
                 i2c_address: int,
                 i2c_port: int,
                 sensor_config: SensorConfig = SensorConfig()) -> None:
        self._i2c_address = i2c_address
        self._smbus = smbus.SMBus(i2c_port)
        self._chip_id = self._smbus.read_byte_data(self._i2c_address, _CHIP_ID_REG)
        self._sensor_config = sensor_config

        self._init_sensor()

    def _init_sensor(self) -> None:
        pass

    def _reset_sensor(self) -> None:
        pass

    def get_chip_id(self) -> int:
        return self._chip_id
