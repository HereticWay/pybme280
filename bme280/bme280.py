from bme280.sensorconfig import SensorConfig, OperationMode, OversamplingMode
import typing as t
import smbus2
import time

_CHIP_ID_REG = 0xD0
_RESET_REG = 0xE0
_CONFIG_REG = 0xF5
_CTRL_MEAS_REG = 0xF4
_CTRL_HUM_REG = 0xF2
_MEASUREMENT_DATA_REG = 0xF7
_MEASUREMENT_DATA_LENGTH = 0xFE - 0xF7
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

        self._chip_id = self._read_register(_CHIP_ID_REG)
        self._init_sensor()

    def _init_sensor(self) -> None:
        self._reset_sensor()
        self._reconfigure_sensor()

    def _reconfigure_sensor(self) -> None:
        # Apply iirc filter and standby mode config
        config = self._sensor_config.build_reg_config()
        self._write_register(_CONFIG_REG, config)

        # Apply humidity oversampling mode config
        ctrl_hum = self._sensor_config.build_reg_ctrl_hum()
        self._write_register(_CTRL_HUM_REG, ctrl_hum)

        # Apply working mode and temperature and pressure oversampling modes config
        ctrl_meas = self._sensor_config.build_reg_ctrl_meas()
        self._write_register(_CTRL_MEAS_REG, ctrl_meas)

    def _read_measurement_data(self) -> t.Tuple[int, ...]:
        # Burst read from 0xF7 to 0xFE
        # data = self._read_registers_block(_MEASUREMENT_DATA_REG, _MEASUREMENT_DATA_LENGTH)

        # TODO: implement data reading and compensating
        raise NotImplementedError("Feature not implemented yet!")

    def _reset_sensor(self) -> None:
        self._write_register(_RESET_REG, _RESET_KEYWORD)
        time.sleep(0.002)  # Wait for the IC to start up (2ms)

    def _write_register(self, register: int, data: int) -> None:
        if type(register) is not int or register < 0:
            raise ValueError("register should be a positive integer!")
        if type(data) is not int or data < 0:
            raise ValueError("data should be a positive integer!")

        address = self._i2c_address
        self._smbus.write_byte_data(address, register, data)

    def _read_register(self, register: int) -> int:
        if type(register) is not int or register < 0:
            raise ValueError("register should be a positive integer!")

        return self._smbus.read_byte_data(self._i2c_address, register)

    def _read_registers_block(self, from_register: int, length: int) -> t.Tuple[int, ...]:
        if type(from_register) is not int or from_register < 0:
            raise ValueError("from_register should be a positive integer!")
        if type(length) is not int or length < 0:
            raise ValueError("length should be a positive integer!")

        return tuple(self._smbus.read_i2c_block_data(self._i2c_address, from_register, length))

    def chip_id(self) -> int:
        return self._chip_id
