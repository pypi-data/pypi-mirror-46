'''Constants used across the BatchCompute SDK package in general.
'''
import sys
import logging
from datetime import datetime

# A dictionary to map numeric state to string state.
STATE_MAP = [
    'Init', 'Waiting', 'Running',
    'Finished', 'Failed', 'Stopped'
]

# BatchCompute endpoint information.
ENDPOINT_INFO = {
    'cn-qingdao': 'batchcompute.cn-qingdao.aliyuncs.com',
    'cn-hangzhou': 'batchcompute.cn-hangzhou.aliyuncs.com',
    'cn-shenzhen': 'batchcompute.cn-shenzhen.aliyuncs.com',
    'cn-beijing': 'batchcompute.cn-beijing.aliyuncs.com',
    'cn-zhangjiakou': 'batchcompute.cn-zhangjiakou.aliyuncs.com',
    'cn-huhehaote': 'batchcompute.cn-huhehaote.aliyuncs.com',
    'cn-shanghai': 'batchcompute.cn-shanghai.aliyuncs.com',
    'cn-hongkong': 'batchcompute.cn-hongkong.aliyuncs.com',
    'ap-southeast-1': 'batchcompute.ap-southeast-1.aliyuncs.com',
    'eu-central-1': 'batchcompute.eu-central-1.aliyuncs.com',
    'us-west-1': 'batchcompute.us-west-1.aliyuncs.com',
    'us-east-1': 'batchcompute.us-east-1.aliyuncs.com',
}
SERVICE_PORT = 80 
SERVICE_PORT_MOCKED = 8888
SECURITY_SERVICE_PORT = 443
CN_HANGZHOU = ENDPOINT_INFO['cn-hangzhou']
CN_QINGDAO = ENDPOINT_INFO['cn-qingdao']
CN_SHENZHEN = ENDPOINT_INFO['cn-shenzhen']
CN_BEIJING = ENDPOINT_INFO['cn-beijing']
CN_ZHANGJIAKOU = ENDPOINT_INFO['cn-zhangjiakou']
CN_HUHEHAOTE = ENDPOINT_INFO['cn-huhehaote']
CN_SHANGHAI = ENDPOINT_INFO['cn-shanghai']
CN_HONGKONG = ENDPOINT_INFO['cn-hongkong']
AP_SOUTHEAST_1 = ENDPOINT_INFO['ap-southeast-1']
EU_CENTRAL_1 = ENDPOINT_INFO['eu-central-1']
US_WEST_1 = ENDPOINT_INFO['us-west-1']
US_EAST_1 = ENDPOINT_INFO['us-east-1']
# Api version supported by BatchCompute.
API_VERSION = '2015-11-11'

# Python 2 or Python 3 is in use.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY25 = sys.version_info[0] == 2 and sys.version_info[1] <= 5

# Definition of descriptor types.
if PY2:
    STRING = (str, unicode, type(None), )
    NUMBER = (int, long, float, type(None), )

if PY3:
    STRING = (str, bytes, type(None), )
    NUMBER = (int, float, type(None), )

FLOAT = (float, type(None))
ANY = STRING + NUMBER
TIME = (int, datetime, type(None)) + STRING
COLLECTION = (list, tuple)

# Log configuration
LOG_LEVEL = logging.WARNING
LOG_FILE_NAME = 'batchcompute_python_sdk.LOG'
LOG_FORMATTER = "[%(asctime)s]\t[%(levelname)s]\t[%(thread)d]\t[%(pathname)s:%(lineno)d]\t%(message)s"
LOG_HANDLER = None
ALL_LOGS= {} 

# Default values
DEFAULT_LIST_ITEM = 100

# Time format
if PY25:
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
else:
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ" 
