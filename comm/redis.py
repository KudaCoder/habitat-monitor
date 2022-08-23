from datetime import datetime
import redis
import json

from habitat_tools import APITools

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
api_tools = APITools()

class RedisWrapper:
    def connect(self):
        connection_pool = redis.ConnectionPool(host="cache", port=6379, db=0)
        return redis.StrictRedis(connection_pool=connection_pool)


def show_redis():
    redis = RedisWrapper().connect()
    return redis.keys()

    
def get_redis(key, reset=False):
    redis = RedisWrapper().connect()
    dc = DC_LIBRARY.get(key)
    r = redis.get(key)

    if r is None:
        data = None
        if key == "environment":
            if not reset:
                data = api_tools.get_config()
            if reset or data is None:
                data = api_tools.new_config()

            data = dc().from_json(json.dumps(data))
            
        elif key == "reading":
            data = data_read()

        if data is not None:
            set_redis(key, data)
            get_redis(key)

    if r is not None:
        return dc().from_json(r.decode("utf-8"))


def set_redis(key, data):
    redis = RedisWrapper().connect()
    redis.set(key, data.to_json())
