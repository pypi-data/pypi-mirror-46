# -*- coding: utf-8 -*-

"""Unit tests for the JSON serializers."""

import sys
import unittest
import numpy as np

from pypif.pif import Scalar, Property, Value

from htdefects.mixing.serializers import jsonify
from htdefects.mixing.serializers import JSONifyError


class TestSerializers(unittest.TestCase):
    """Unit tests for :class:`htdefects.mixing.serializers`."""

    def test_jsonify(self):
        # bool
        self.assertIsInstance(jsonify(False), bool)

        # int
        self.assertEqual(jsonify(42), 42)

        # float
        self.assertEqual(jsonify(42.42), 42.42)

        # str
        self.assertEqual(jsonify("42.42"), "42.42")

        # list
        self.assertListEqual(jsonify([True, False]), [True, False])
        self.assertListEqual(jsonify([42, 23]), [42, 23])
        self.assertListEqual(jsonify([42.42, 23.23]), [42.42, 23.23])
        self.assertListEqual(jsonify(["42", "23"]), ["42", "23"])

        # numpy array
        self.assertListEqual(jsonify(np.array([42, 23])), [42, 23])
        self.assertIsInstance(jsonify(np.array([42, 23])), list)

        self.assertListEqual(jsonify(np.array([42.42, 23.23])), [42.42, 23.23])
        self.assertIsInstance(jsonify(np.array([42.42, 23.23])), list)

        self.assertListEqual(jsonify(np.array(["42", "23"])), ["42", "23"])
        self.assertIsInstance(jsonify(np.array(["42", "23"])), list)

        # numpy int
        self.assertIsInstance(jsonify(np.int64(42)), int)

        # numpy float
        self.assertIsInstance(jsonify(np.float64(42.42)), float)

        # numpy bool
        self.assertIsInstance(jsonify(np.bool(42)), bool)

        # dict
        data = {
            'a': 42,
            'b': np.float64(123),
            'c': {
                'a2': 'this is nested',
                'b2': {
                    'c2': ['another level', np.float64(42)]
                }
            }
        }
        self.assertDictEqual(jsonify(data),
                             {'a': 42, 'b': 123.,
                              'c': {'a2': 'this is nested',
                                    'b2': {'c2': ['another level', 42.]}}})

        # Scalar
        self.assertEqual(jsonify(Scalar(value=42)), 42)
        self.assertEqual(jsonify(Scalar(value="DON'T PANIC!")), "DON'T PANIC!")

        # Property
        prop = Property(name='Life, the Universe and Everything',
                        scalars=[Scalar(value=42)],
                        units='Towel/person')
        self.assertDictEqual(jsonify(prop), {
            'name': 'Life, the Universe and Everything',
            'values': [42],
            'units': 'Towel/person'
        })

        self.assertDictEqual(jsonify(Property(units='E')), {
            'name': None,
            'values': None,
            'units': 'E',
        })

        # failure without exception
        self.assertIsNone(jsonify(Value(name='towel', scalars=[42])))

        # failure
        with self.assertRaises(JSONifyError):
            self.assertIsNone(jsonify(Value(name='towel', scalars=[42]),
                                      ignore_failures=False))


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)

