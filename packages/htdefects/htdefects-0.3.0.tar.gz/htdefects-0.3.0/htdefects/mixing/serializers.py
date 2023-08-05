# -*- coding: utf-8 -*-

"""Some helper utilities to serialize data."""

import six
import numpy as np

from pypif.pif import Property
from pypif.pif import Scalar


class JSONifyError(Exception):
    """Base class to handle errors associated with JSON-serializing data."""
    pass


def jsonify(data, ignore_failures=True):
    """Convert data into JSON-serializable format.

    Parameters
    ----------

    data:
        Data to be serialized.

    ignore_failures: bool, optional
        Should errors raise exceptions instead of simply returning None?

    Returns
    -------

    Serialized data if successful, else None.

    Raises
    ------

    JSONifyError if input data cannot be serialized and it is specified to
    not ignore a failed serialization.

    """
    if data is None:
        return
    elif isinstance(data, (bool, int, float, six.string_types)):
        return data
    elif isinstance(data, list):
        return [jsonify(v) for v in data]
    elif isinstance(data, np.ndarray):
        return jsonify(data.tolist())
    elif isinstance(data, (np.integer, np.floating, np.bool_)):
        return data.item()
    elif isinstance(data, dict):
        json_data = {}
        for k, v in data.items():
            json_data[k] = jsonify(v)
        return json_data
    elif isinstance(data, Scalar):
        return jsonify(data.value)
    elif isinstance(data, Property):
        return {
            'name': jsonify(data.name),
            'values': jsonify(data.scalars),
            'units': jsonify(data.units),
        }
    else:
        if ignore_failures:
            return
        else:
            error_message = 'Cannot serialize data type {}'.format(type(data))
            raise JSONifyError(error_message)

