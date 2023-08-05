import sys

from batchcompute import (
    Client, CN_QINGDAO
)
from batchcompute.resources import (ClusterDescription, GroupDescription)
from batchcompute.utils.log import set_log_level, get_logger
import batchcompute

logger = get_logger('batchcompute.test', level='DEBUG', file_name='batchcompute_python_sdk.LOG')


clnt = Client(CN_HANGZHOU, "", "")
print clnt.get_app("haha")
