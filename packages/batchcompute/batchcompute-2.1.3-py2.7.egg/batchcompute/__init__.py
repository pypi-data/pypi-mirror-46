'''A simple implementation for BatchCompute service SDK.
'''
__version__ = '2.1.3'
__all__ = [
    "Client", "ClientError", "FieldError", "ValidationError", "JsonError",
    "ConfigError", "CN_QINGDAO", "CN_HANGZHOU", "CN_SHENZHEN", "CN_BEIJING",
    "CN_ZHANGJIAKOU", "CN_HUHEHAOTE", "CN_SHANGHAI",
    "CN_HONGKONG", "AP_SOUTHEAST_1", "EU_CENTRAL_1", "US_WEST_1", "US_EAST_1",
]
__author__ = 'crisish'

from .client import Client
from .core import ClientError, FieldError, ValidationError, JsonError
from .utils import (
    CN_QINGDAO, CN_SHENZHEN, CN_HANGZHOU, CN_BEIJING, CN_ZHANGJIAKOU,
    CN_HUHEHAOTE, CN_SHANGHAI,CN_HONGKONG,AP_SOUTHEAST_1,EU_CENTRAL_1,
    US_WEST_1, US_EAST_1, ConfigError,
)
