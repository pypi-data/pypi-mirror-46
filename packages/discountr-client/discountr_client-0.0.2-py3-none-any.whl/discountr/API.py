from __future__ import annotations

import json
import logging
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('APIClient')


class BaseObject:
    def to_json(self):
        return json.dumps(self.__dict__)


class Brand(BaseObject):
    def name(self, name):
        self.name = name
        return self

    def slug(self, slug):
        self.slug = slug
        return self


class Category(BaseObject):
    def name(self, name):
        self.name = name
        return self

    def slug(self, slug):
        self.slug = slug
        return self


class Product(BaseObject):
    def name(self, name: str):
        self.name = name
        return self

    def code(self, code):
        self.code = code
        return self

    def slug(self, slug: str):
        self.slug = slug
        return self

    def brand_id(self, brand_id: int):
        self.brand_id = brand_id
        return self

    def category_id(self, category_id: int):
        self.category_id = category_id
        return self


class Price(BaseObject):
    def __init__(self):
        self.created_at = datetime.now().isoformat()

    def value(self, price: float):
        self.price = price
        return self

    def created_at(self, created_at: datetime):
        self.created_at = created_at.isoformat()
        return self

    def product_id(self, product_id: int):
        self.product_id = product_id
        return self


class API:
    _url = os.getenv('API_URL', 'https://api.discountr.info/')
    _token = "Token " + os.getenv('API_TOKEN', '')

    def __init__(self, app_name: str = None):
        super().__init__()

        self._app_name = app_name
        self.__client = requests.session()

        self.__client.headers['Authorization'] = self._token
        self.__client.headers['Content-Type'] = 'application/json'

    def create_brand(self, brand: Brand):
        self.__create(brand)

    def create_category(self, category: Category):
        self.__create('categories', category)

    def create_product(self, product: Product):
        self.__create('products', product)

    def create_price(self, price: Price):
        self.__create('prices', price)

    def __create(self, endpoint, data):
        response = self.__client.post('%s%s/%s/' % (self._url, self._app_name, endpoint),
                                      data=data.to_json())

        if response.status_code >= 500:
            logger.critical(
                '%s Server Error: %s for url: %s' % (response.status_code, response.reason, response.url))
        elif response.status_code >= 400:
            logger.debug('%s Client Error: %s for url: %s' % (response.status_code, response.reason, response.url))
