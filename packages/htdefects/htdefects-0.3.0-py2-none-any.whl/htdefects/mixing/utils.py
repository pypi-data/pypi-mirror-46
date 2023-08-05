import six
import numpy
from pypif.pif import Property
from pypif.pif import Scalar


class JSONableError(Exception):
    """Base class to handle errors associated with JSON-serializing data."""
    pass


def jsonable(data, ignore_failures=True):
    """Convert data into JSON-serializable format."""
    if data is None:
        return
    elif isinstance(data, (bool, int, float, six.string_types)):
        return data
    elif isinstance(data, list):
        return [jsonable(v) for v in data]
    elif isinstance(data, numpy.ndarray):
        return jsonable(data.tolist())
    elif isinstance(data, (numpy.integer, numpy.floating, numpy.bool_)):
        return numpy.asscalar(data)
    elif isinstance(data, dict):
        json_data = {}
        for k, v in data.items():
            json_data[k] = jsonable(v)
        return json_data
    elif isinstance(data, Scalar):
        return jsonable(data.value)
    elif isinstance(data, Property):
        if not data.name:
            return
        else:
            return {data.name: {'value': jsonable(data.scalars), 'units': data.units}}
    else:
        if ignore_failures:
            return
        else:
            error_message = 'Cannot serialize data type {}'.format(type(data))
            raise JSONableError(error_message)

