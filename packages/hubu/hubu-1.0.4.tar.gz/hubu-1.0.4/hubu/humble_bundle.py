import json
import re
import requests
from hubu.base import Base


class HumbleBundle(Base):
    def __init__(self, auth_session_id):
        super(__class__, self).__init__()
        self.__cookies = dict(_simpleauth_sess=auth_session_id)

    def purchases(self):
        response = requests.get('https://www.humblebundle.com/home/purchases', cookies=self.__cookies)
        keys = json.loads(re.search(r'"gamekeys"\s*:\s*(.*)', response.text).groups()[0][:-1])
        return [Purchase(key, self.__cookies) for key in keys]

class Purchase(Base):
    def __init__(self, key, cookies):
        super(__class__, self).__init__()
        self.key = key
        self.cookies = cookies
        self.info = None
        self.sanitized_name = None

    def _download_info(self):
        url = f'https://www.humblebundle.com/api/v1/order/{self.key}?all_tpkds=true'
        response = requests.get(url, cookies=self.cookies)
        self.info = json.loads(response.text)
        self.sanitized_name = self.slugify(self.info['product']['human_name'])

    def products(self):
        if self.info is None:
            self._download_info()
        for product in self.info['subproducts']:
            product['slugify_name'] = self.slugify(product['human_name'])
            yield product
