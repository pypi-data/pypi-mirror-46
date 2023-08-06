import logging
import sys

import requests
from sequence_field.fields import SequenceField
from sequence_field.error import OrderNumberError

logger = logging.getLogger(__name__)


class OrderNumber(object):

    def __init__(self, app=None):
        self.app = app
        self.url = None
        if app:
            self.init_app(app)

    def init_app(self, app=None):
        url = app.config.get('ORDERURL')
        if not url:
            logger.error("未配置ORDERURL")
            sys.exit(1)
        # 判断该url是否有效
        res = requests.get(url=url)
        # print(res.json())
        if res.json() != 'hello':
            logger.error("ORDERURL无效")
            sys.exit(3)
        self.url = url

    def exist(self, key=''):
        exist_url = self.url + '/exist'
        res = requests.get(exist_url, params=dict(key=key))
        if res.status_code == 200:
            return True
        else:
            return False

    def create(self, key):
        create_url = self.url + '/create'
        res = requests.post(create_url, json=dict(key=key))
        if res.status_code == 200:
            return True
        else:
            raise OrderNumberError(message="该key已经被占用了")

    def add(self, key):
        key_url = self.url + '/add'
        res = requests.get(key_url, params=dict(key=key))
        if res.status_code == 200:
            return res.json()
        else:
            raise OrderNumberError(message="该key没有创建")


