from datetime import datetime
import pickle
import redis

from api.blueprints import utils as api_tools

# Rename dataclasses to protect against any future 
# scenario where models are used here as well
from utility.dataclass import Environment as data_env
from utility.dataclass import Reading as data_read
from utility.dataclass import Light as data_light


DC_LIBRARY = {
    "environment": data_env,
    "reading": data_read,
    "light": data_light
}

class RedisWrapper:
    def connect(self):
        connection_pool = redis.ConnectionPool(host="cache", port=6379, db=0)
        return redis.StrictRedis(connection_pool=connection_pool)


def get_redis(key, reset=False):
    redis = RedisWrapper().connect()
    r = redis.get(key)

    # If first time redis key is being set - only really appropriate to config
    if r is None:
        data = None
        # TODO: Delete redis and see if this is working or not?
        if key == "environment":
            try:
                if not reset:
                    data = api_tools.get_config()
                if reset or not data:
                    data = api_tools.new_config()
            except Exception:
                pass

        if data is not None:
            update_redis(key, data)
            get_redis(key)
    
    if r is None:
        return r

    return pickle.loads(r)


def set_redis(key, obj):
    redis = RedisWrapper().connect()
    redis.set(key, pickle.dumps(obj))


def update_redis(key, data):
    dc = DC_LIBRARY.get(key)
    if dc is None:
        # TODO: Throw exception here?!
        return

    dc = dc()
    for k, v in data.items():
        if hasattr(dc, k):
            try:
                v = datetime.strptime(v, "%H:%M:%S").time()
            except Exception:
                pass
            setattr(dc, k, v)
    set_redis(key, dc)
