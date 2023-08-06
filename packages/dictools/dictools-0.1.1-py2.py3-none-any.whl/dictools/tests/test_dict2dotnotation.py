# -*- coding: utf-8 -*-

import unittest

import six
from dictools import dict2dotnotation


def map2(*args, **kwargs):
    if six.PY3:
        return [x for x in map(*args, **kwargs)]
    return map(*args, **kwargs)


class TestDict2DotNotation(unittest.TestCase):
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
                'result': {
                    'k1.k11.k111': 'v111',
                    'k2.k21.k211': 'v211',
                    'k2.k21.k212': 'v212',
                }
            },
        ]
        # fmt: on

    def tearDown(self):
        pass

    def test_dict2dotnotation_01(self):
        def check_test_data(data):
            d = data['dict']
            result = dict2dotnotation(d)
            self.assertEqual(result, data['result'])

        map2(check_test_data, self.test_data_list)
