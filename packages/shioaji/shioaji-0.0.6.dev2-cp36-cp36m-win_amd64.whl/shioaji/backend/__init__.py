from shioaji.backend.http import HttpApi
from shioaji.backend.socket import Wrapper


def get_backends():
    apis = {
        'http': HttpApi,
        'socket': Wrapper,
    }
    return apis
