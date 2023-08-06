# -*- coding: utf-8 -*-

import unittest

import six
from dictools import dict_del_vals


def map2(*args, **kwargs):
    if six.PY3:
        return [x for x in map(*args, **kwargs)]
    return map(*args, **kwargs)


class TestDictDelVals(unittest.TestCase):
    def setUp(self):
        # fmt: off
        self.test_data_list = [
            {
                'dict': {
                    'a': 1,
                    'b': 'bbb',
                    'c': 'c3c',
                    4: 'd',
                    'e': 5,
                    'f': None,
                    'g': [],
                    'h': {},
                },
                'del_vals': ['d', 1, 'bbb', 'c3c', 'not_exists'],
                'result': {
                    'e': 5,
                    'f': None,
                    'g': [],
                    'h': {}
                }
            },
            {
                'dict': {
                    "k1": {
                        "k11": {
                            "k111": "v111"
                        }
                    },
                    "k2": {
                        "k21": {
                            "k211": "v211",
                            "k212": "v212"
                        }
                    },
                    "k3": 3,
                    "k4": [],
                    "k5": None
                },
                'del_vals': ["v212", "v111", {}, [], None],
                'result': {
                    "k2": {
                        "k21": {
                            "k211": "v211",
                        }
                    },
                    "k3": 3,
                }
            },
        ]
        # fmt: on

    def tearDown(self):
        pass

    def check_test_data(self, data):
        d = data['dict']
        result = dict_del_vals(d, data['del_vals'])
        self.assertEqual(result, data['result'])

    def test_dict_del_vals_01(self):
        map2(self.check_test_data, self.test_data_list)
