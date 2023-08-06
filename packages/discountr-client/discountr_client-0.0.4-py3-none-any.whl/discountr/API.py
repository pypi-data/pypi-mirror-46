from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('APIClient')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class BaseObject:
    def to_json(self):
        temp = {}
        for key, value in self.__dict__.items():
            temp[re.sub(r'^_', '', key)] = value
        return json.dumps(temp)


class Brand(BaseObject):

    def name(self, name) -> Brand:
        self._name = name
        return self

    def slug(self, slug) -> Brand:
        self._slug = slug
        return self


class Category(BaseObject):
    def name(self, name) -> Category:
        self._name = name
        return self

    def slug(self, slug) -> Category:
        self._slug = slug
        return self


class Product(BaseObject):
    def name(self, name: str) -> Product:
        self._name = name
        return self

    def code(self, code) -> Product:
        self._code = code
        return self

    def slug(self, slug: str) -> Product:
        self._slug = slug
        return self

    def brand_id(self, brand_id: int) -> Product:
        self._brand_id = brand_id
        return self

    def category_id(self, category_id: int) -> Product:
        self._category_id = category_id
        return self


class Price(BaseObject):
    def __init__(self):
        self._created_at = datetime.now().isoformat()

    def value(self, price: float) -> Price:
        self._price = price
        return self

    def created_at(self, created_at: datetime) -> Price:
        self._created_at = created_at.isoformat()
        return self

    def product_id(self, product_id: int) -> Price:
        self._product_id = product_id
        return self


class API:
    _url = os.getenv('API_URL', 'https://api.discountr.info/')
    _token = "Token " + os.getenv('API_TOKEN', '')

    def __init__(self, app_name: str = None):
        super().__init__()

        self._app_name = app_name

    def create_brand(self, brand: Brand):
        self.__create('brands', brand)

    def create_category(self, category: Category):
        self.__create('categories', category)

    def create_product(self, product: Product):
        self.__create('products', product)

    def create_price(self, price: Price):
        self.__create('prices', price)

    def __create(self, endpoint, data):
        response = requests.post('%s%s/%s/' % (self._url, self._app_name, endpoint),
                                 data=data.to_json(), headers={
                'Authorization': self._token,
                'Content-Type': 'application/json'
            })

        if response.status_code >= 500:
            logger.critical(
                '%s Server Error: %s for url: %s' % (response.status_code, response.reason, response.url))
        elif response.status_code >= 400:
            logger.debug('%s Client Error: %s for url: %s' % (response.status_code, response.reason, response.url))
