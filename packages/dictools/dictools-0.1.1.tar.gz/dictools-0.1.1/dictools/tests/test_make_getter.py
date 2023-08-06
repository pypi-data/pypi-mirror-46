# -*- coding: utf-8 -*-

import unittest

import six
from dictools import make_getter


def map2(*args, **kwargs):
    if six.PY3:
        return [x for x in map(*args, **kwargs)]
    return map(*args, **kwargs)


class TestMakeGetter(unittest.TestCase):
    def setUp(self):
        # fmt: off
        dict1 = {
            'k1': {
                'k11': {
                    'k111': 'v111'
                }
            },
            'k2': {
                'k21': {
                    'k211': 'v211',
                    'k212': 'v212'
                }
            },
        }

        self.test_data_list = [
            {
                'dict': dict1,
                'path': 'k2.k21.k212',
                'result': 'v212'
            },
            {
                'dict': dict1,
                'path': 'k2.k21.k215',
                'result': None
            },
            {
                'dict': dict1,
                'path': 'k2.k21.k215',
                'default': 5,
                'result': 5
            },
        ]
        self.test_data_list_with_root = [
            {
                'dict': dict1,
                'root': 'k2',
                'path': 'k21.k212',
                'result': 'v212'
            },
            {
                'dict': dict1,
                'root': 'k2',
                'path': 'k21.k215',
                'result': None
            },
            {
                'dict': dict1,
                'root:': 'k2',
                'path': 'k21.k215',
                'default': 5,
                'result': 5
            },
        ]
        # fmt: on

    def tearDown(self):
        pass

    def test_make_getter_01(self):
        def check_test_data(data):
            d = data['dict']
            get = make_getter(d, default=data.get('default', None))
            path = data.get('path', None)
            result = get(path)
            self.assertEqual(result, data['result'])

        map2(check_test_data, self.test_data_list)

    def test_make_getter_02(self):
        def check_test_data(data):
            d = data['dict']
            get = make_getter(d)
            path = data.get('path', None)
            result = get(path, default=data.get('default', None))
            self.assertEqual(result, data['result'])

        map2(check_test_data, self.test_data_list)

    def test_make_getter_03(self):
        def check_test_data(data):
            d = data['dict']
            get = make_getter(d, root=data.get('root', None))
            path = data.get('path', None)
            result = get(path, default=data.get('default', None))
            self.assertEqual(result, data['result'])

        map2(check_test_data, self.test_data_list_with_root)
