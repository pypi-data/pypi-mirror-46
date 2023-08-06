# -*- coding: utf-8 -*-

import unittest

import six
from dictools import get_by_path


def map2(*args, **kwargs):
    if six.PY3:
        return [x for x in map(*args, **kwargs)]
    return map(*args, **kwargs)


class TestGetByPath(unittest.TestCase):
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
        # fmt: on

    def tearDown(self):
        pass

    def check_test_data(self, data):
        d = data['dict']
        default = data.get('default', 'd69b81ef-bb4e-44eb-aae2-8719f811af56')
        if default == 'd69b81ef-bb4e-44eb-aae2-8719f811af56':
            result = get_by_path(d, data['path'])
        else:
            result = get_by_path(d, data['path'], default)
        self.assertEqual(result, data['result'])

    def test_get_by_path_01(self):
        map2(self.check_test_data, self.test_data_list)
