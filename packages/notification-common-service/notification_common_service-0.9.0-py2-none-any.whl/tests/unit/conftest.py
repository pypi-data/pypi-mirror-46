# -*- coding: utf-8 -*-
import pytest
from faker import Faker


@pytest.fixture(scope='session')
def faker():
    return Faker('zh-CN')


@pytest.fixture(scope='session')
def xinge_info():
    return {
        'android': {
            'access_id': '2100311092',
            'secret_key': '8d9bc98ffcdb833b369ae8ea72f8082c',
            'target':
            '1c58480365191f2638bf49c8de4f8477b0958452',
        },
        'ios': {
            'access_id': '2200321268',
            'secret_key': '2a020ed64ef2e31e352f076d7460543a',
            'target':
            'bc648aa880d4757127a4433ddda073b19f8454a60bd53b6da952890ca11848cf',
        }
    }
