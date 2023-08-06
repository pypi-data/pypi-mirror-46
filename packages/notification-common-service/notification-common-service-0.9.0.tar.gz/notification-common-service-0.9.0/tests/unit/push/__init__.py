# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from unittest import TestCase
from operator import methodcaller

from faker import Faker

from notification_service.push.base import Environment

faker = Faker()


def create_Message(cls, **kwargs):
    need_faker_fields = [('title', 'name'), ('content', 'text')]
    for field_name, method_name in need_faker_fields:
        if not field_name in kwargs:
            kwargs[field_name] = methodcaller(method_name)(faker)
    if 'ios' in kwargs['client_type'] and not 'environment' in kwargs:
        kwargs.update(environment=Environment.production)
    return cls(**kwargs)


class TestMessage(TestCase):

    def setUp(self):
        self.title = faker.name()
        self.content = faker.text()
        self.new_title = faker.name()
        self.new_content = faker.text()
