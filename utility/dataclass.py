from dataclasses import dataclass
from typing import Optional
from datetime import datetime, time


@dataclass
class Environment:
    lights_on_time: Optional[time] = None
    lights_off_time: Optional[time] = None
    day_h_sp: Optional[float] = None
    day_l_sp: Optional[float] = None
    night_h_sp: Optional[float] = None
    night_l_sp: Optional[float] = None
    humidity_h_sp: Optional[float] = None
    humidity_l_sp: Optional[float] = None


@dataclass
class Reading:
    temp: Optional[float] = None
    hum: Optional[float] = None


@dataclass
class Light:
    turned_on: Optional[bool] = None
