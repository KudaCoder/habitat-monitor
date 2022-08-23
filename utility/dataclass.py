from dataclasses import dataclass, asdict
from datetime import datetime, time
from typing import Optional
import json


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

    def to_json(self):
        data = asdict(self)
        for k, v in data.items():
            if isinstance(v, time):
                data[k] = v.isoformat()
        return json.dumps(data)
    
    @staticmethod
    def from_json(json_data):
        env = Environment()
        data = json.loads(json_data)
        for k, v in data.items():
            if hasattr(env, k):
                try:
                    v = datetime.strptime(v, "%H:%M:%S").time()
                except Exception:
                    v = float(v)
                finally:
                    setattr(env, k, v)

        return env


@dataclass
class Reading:
    temperature: Optional[float] = None
    humidity: Optional[float] = None

    def to_json(self):
        return json.dumps(asdict(self))
    
    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        return Reading(**data)


@dataclass
class Light:
    turned_on: Optional[bool] = None

    def to_json(self):
        return json.dumps(asdict(self))
