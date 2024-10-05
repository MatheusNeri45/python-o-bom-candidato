from decouple import config


class Config(object):
    MONGO_URI = config('MONGO_URI', default='mongodb://localhost:27017/')


def configure():
    return Config
