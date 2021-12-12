from enum import Enum, unique


@unique
class StandbyInterval(Enum):
    INT_0_5_MS = 0x00
    INT_62_5_MS = 0x01
    INT_125_MS = 0x02
    INT_250_MS = 0x03
    INT_500_MS = 0x04
    INT_1000_MS = 0x05
    INT_10_MS = 0x06
    INT_20_MS = 0x07


@unique
class IIRFilterCoefficient(Enum):
    OFF = 0x00
    X2 = 0x01
    X4 = 0x02
    X8 = 0x03
    X16 = 0x04


@unique
class OversamplingMode(Enum):
    SKIPPED = 0x00
    X1 = 0x01
    X2 = 0x02
    X4 = 0x03
    X8 = 0x04
    X16 = 0x05


@unique
class OperationMode(Enum):
    SLEEP = 0x00
    FORCED = 0x01
    NORMAL = 0x03


class SensorConfig:
    __slots__ = (
        "_operation_mode",
        "_temp_oversampling_mode",
        "_pressure_oversampling_mode",
        "_humidity_oversampling_mode",
        "_iir_filter_coefficient",
        "_standby_interval"
    )

    _operation_mode: OperationMode
    _temp_oversampling_mode: OversamplingMode
    _pressure_oversampling_mode: OversamplingMode
    _humidity_oversampling_mode: OversamplingMode
    _iir_filter_coefficient: IIRFilterCoefficient
    _standby_interval: StandbyInterval

    def __init__(self,
                 operation_mode: OperationMode = OperationMode.NORMAL,
                 temperature_oversampling_mode: OversamplingMode = OversamplingMode.X2,
                 pressure_oversampling_mode: OversamplingMode = OversamplingMode.X16,
                 humidity_oversampling_mode: OversamplingMode = OversamplingMode.X1,
                 iir_filter_coefficient: IIRFilterCoefficient = IIRFilterCoefficient.X16,
                 standby_interval: StandbyInterval = StandbyInterval.INT_125_MS
                 ) -> None:
        self.set_operation_mode(operation_mode)
        self.set_temperature_oversampling_mode(temperature_oversampling_mode)
        self.set_pressure_oversampling_mode(pressure_oversampling_mode)
        self.set_humidity_oversampling_mode(humidity_oversampling_mode)
        self.set_iir_filter_coefficient(iir_filter_coefficient)
        self.set_standby_interval(standby_interval)

    def set_operation_mode(self, mode: OperationMode) -> None:
        if type(mode) is not OperationMode:
            raise TypeError("Parameter should be an OperationMode!")
        self._operation_mode = mode

    def set_temperature_oversampling_mode(self, mode: OversamplingMode) -> None:
        if type(mode) is not OversamplingMode:
            raise TypeError("Parameter should be an OversamplingMode!")
        self._temp_oversampling_mode = mode

    def set_pressure_oversampling_mode(self, mode: OversamplingMode) -> None:
        if type(mode) is not OversamplingMode:
            raise TypeError("Parameter should be an OversamplingMode!")
        self._pressure_oversampling_mode = mode

    def set_humidity_oversampling_mode(self, mode: OversamplingMode) -> None:
        if type(mode) is not OversamplingMode:
            raise TypeError("Parameter should be an OversamplingMode!")
        self._humidity_oversampling_mode = mode

    def set_iir_filter_coefficient(self, coefficient: IIRFilterCoefficient) -> None:
        if type(coefficient) is not IIRFilterCoefficient:
            raise TypeError("Parameter should be an IIRFilterCoefficient!")
        self._iir_filter_coefficient = coefficient

    def set_standby_interval(self, interval: StandbyInterval) -> None:
        if type(interval) is not StandbyInterval:
            raise TypeError("Parameter should be a StandbyInterval!")
        self._standby_interval = interval

    def operation_mode(self) -> OperationMode:
        return self._operation_mode

    def temperature_oversampling_mode(self) -> OversamplingMode:
        return self._temp_oversampling_mode

    def pressure_oversampling_mode(self) -> OversamplingMode:
        return self._temp_oversampling_mode

    def humidity_oversampling_mode(self) -> OversamplingMode:
        return self._humidity_oversampling_mode

    def iirc_filter_coefficient(self) -> IIRFilterCoefficient:
        return self._iir_filter_coefficient

    def standby_interval(self) -> StandbyInterval:
        return self._standby_interval

    def build_reg_ctrl_meas(self) -> int:
        mode = self.operation_mode().value
        osrs_p = self.pressure_oversampling_mode().value << 2
        osrs_t = self.temperature_oversampling_mode().value << 5
        return mode | osrs_p | osrs_t

    def build_reg_ctrl_hum(self) -> int:
        return self.humidity_oversampling_mode().value

    def build_reg_config(self) -> int:
        spi3w_en = 0  # Disable 3-wire SPI
        filter_ = self.iirc_filter_coefficient().value << 1
        t_sb = self.standby_interval().value << 4
        return spi3w_en | filter_ | t_sb

