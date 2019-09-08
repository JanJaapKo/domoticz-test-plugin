"""Dyson Pure Cool Link constants."""

from enum import Enum

DYSON_PURE_COOL_LINK_TOUR = "475"
DYSON_PURE_COOL_LINK_DESK = "469"
DYSON_PURE_HOT_COOL_LINK_TOUR = "455"
DYSON_360_EYE = "N223"


class FanMode(Enum):
    """Fan mode."""

    OFF = 'OFF'
    FAN = 'FAN'
    AUTO = 'AUTO'


class Oscillation(Enum):
    """Oscillation."""

    OSCILLATION_ON = 'ON'
    OSCILLATION_OFF = 'OFF'


class NightMode(Enum):
    """Night mode."""

    NIGHT_MODE_ON = 'ON'
    NIGHT_MODE_OFF = 'OFF'


class FanSpeed(Enum):
    """Fan Speed."""

    FAN_SPEED_1 = '0001'
    FAN_SPEED_2 = '0002'
    FAN_SPEED_3 = '0003'
    FAN_SPEED_4 = '0004'
    FAN_SPEED_5 = '0005'
    FAN_SPEED_6 = '0006'
    FAN_SPEED_7 = '0007'
    FAN_SPEED_8 = '0008'
    FAN_SPEED_9 = '0009'
    FAN_SPEED_10 = '0010'
    FAN_SPEED_AUTO = 'AUTO'


class FanState(Enum):
    """Fan State."""

    FAN_OFF = "OFF"
    FAN_ON = "FAN"


class QualityTarget(Enum):
    """Quality Target for air."""

    QUALITY_NORMAL = "0004"
    QUALITY_HIGH = "0003"
    QUALITY_BETTER = "0001"


class StandbyMonitoring(Enum):
    """Monitor air quality when on standby."""

    STANDBY_MONITORING_ON = "ON"
    STANDBY_MONITORING_OFF = "OFF"


class FocusMode(Enum):
    """Fan operates in a focused stream or wide spread."""

    FOCUS_OFF = "OFF"
    FOCUS_ON = "ON"


class TiltState(Enum):
    """Indicates if device is tilted."""

    TILT_TRUE = "TILT"
    TILT_FALSE = "OK"


class HeatMode(Enum):
    """Heat mode for the fan."""

    HEAT_OFF = "OFF"
    HEAT_ON = "HEAT"


class HeatState(Enum):
    """Heating State."""

    HEAT_STATE_OFF = "OFF"
    HEAT_STATE_ON = "HEAT"


class ResetFilter(Enum):
    """Reset the filter status / new filter."""

    RESET_FILTER = "RSTF"
    DO_NOTHING = "STET"


class PowerMode(Enum):
    """360 Eye power mode."""

    QUIET = "halfPower"
    MAX = "fullPower"


class Dyson360EyeMode(Enum):
    """360 Eye state."""

    INACTIVE_CHARGED = "INACTIVE_CHARGED"
    FULL_CLEAN_INITIATED = "FULL_CLEAN_INITIATED"
    FULL_CLEAN_RUNNING = "FULL_CLEAN_RUNNING"
    FULL_CLEAN_PAUSED = "FULL_CLEAN_PAUSED"
    FULL_CLEAN_ABORTED = "FULL_CLEAN_ABORTED"
    FULL_CLEAN_FINISHED = "FULL_CLEAN_FINISHED"
    INACTIVE_CHARGING = "INACTIVE_CHARGING"
    FAULT_USER_RECOVERABLE = "FAULT_USER_RECOVERABLE"
    FULL_CLEAN_NEEDS_CHARGE = "FULL_CLEAN_NEEDS_CHARGE"
    FAULT_REPLACE_ON_DOCK = "FAULT_REPLACE_ON_DOCK"


class Dyson360EyeCommand(Enum):
    """360 Eye commands."""

    STATE_SET = "STATE-SET"
    START = "START"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    ABORT = "ABORT"
