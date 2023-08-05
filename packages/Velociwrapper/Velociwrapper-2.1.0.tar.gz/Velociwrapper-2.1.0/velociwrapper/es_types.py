from __future__ import absolute_import, unicode_literals
from six import iteritems, string_types, add_metaclass
from past.builtins import unicode, long

from datetime import date, datetime
import re

from .config import logger

__all__ = [
    'create_es_type', 'is_analyzed', 'ESType', 'Array', 'String', 'Number', 'Float', 'Double', 'Integer', 'Long',
    'Short', 'Byte', 'TokenCount', 'DateTime', 'Date', 'Boolean', 'IP', 'GeoPoint', 'GeoShape', 'Attachment'
]


# check the python type and return the appropriate ESType class
def create_es_type(value):
    # check if we're already an es type
    try:
        if type(value).__class__ == ESType:
            return value
    except AttributeError:
        pass

    if isinstance(value, string_types):
        # strings could be a lot of things
        # try to see if it might be a date

        # dateutil isn't good at determining if we have a date (ok at parsing if we know there's a date).
        # To that end we'll only accept a couple of valid formats
        test_date = value.strip()
        test_date = re.sub("(?:Z|\s*[\+\-]\d\d:?\d\d)$", '', test_date)

        try:
            test_date = datetime.strptime(test_date, '%Y-%m-%d %H:%M:%S')
            return DateTime(test_date)

        except ValueError:
            try:
                test_date = datetime.strptime(test_date, '%Y-%m-%dT%H:%M:%S')
                return DateTime(test_date)
            except ValueError:

                try:
                    test_date = datetime.strptime(test_date, '%Y-%m-%dT%H:%M:%S.%f')
                    return DateTime(test_date)
                except ValueError:
                    try:
                        test_date = datetime.strptime(test_date, '%Y-%m-%d')
                        return Date(test_date.date())
                    except ValueError:
                        pass

        # see if it might be an ip address
        try:
            matches = re.search('^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$', value)
            if matches:
                valid_ip = True
                for g in matches.groups():
                    g = int(g)
                    if g < 1 or g > 254:
                        # nope
                        valid_ip = False

                if valid_ip:
                    return IP(value)
        except:
            pass

        if isinstance(value, string_types):
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    return String(value)

    if isinstance(value, int):
        return Integer(value)

    if isinstance(value, bool):
        return Boolean(value)

    if isinstance(value, long):
        return Long(value)

    if isinstance(value, float):
        return Float(value)

    if isinstance(value, datetime):
        return DateTime(value)

    if isinstance(value, date):
        return Date(value)

    # if here, just return the value as is
    return value


# this is to determine if the field should be analyzed
# based on type and settings. Used a lot to determine whether to use
# term filters or matches
# works with estypes and non-estypes
def is_analyzed(value):
    analyzed = True
    check_defaults = False
    try:
        if type(value).__class__ == ESType:
            if isinstance(value, String) or isinstance(value, Array):
                analyzed = value.es_args().get('analyzed')
                if analyzed == None:
                    analyzed = True
            else:
                analyzed = False
        else:
            check_defaults = True
    except AttributeError:
        check_defaults = True

    if check_defaults:
        analyzed = False
        if isinstance(value, object):  # this likely should't happen
            analyzed = True
        else:
            checklist = []
            if isinstance(value, list):
                checklist = value
            else:
                checklist = [value]

            for item in checklist:
                if isinstance(value, string_types):
                    analyzed = True
                    break

    return analyzed


class ESType(type):
    @classmethod
    def build_map(cls, d):

        if isinstance(d, list):
            out_list = []
            for i in d:
                out_list.append(cls.build_map(i))
            return out_list

        elif isinstance(d, dict):
            output = {}

            for k, v in iteritems(d):
                if isinstance(v, dict):
                    output[k] = cls.build_map(v)
                else:
                    try:
                        if type(v).__class__ == ESType:
                            output[k] = v.prop_dict()
                        else:
                            output[k] = v
                    except:
                        output[k] = v
            return output

        return {}  # I *think* we should never end up here

    def __new__(cls, clsname, bases, dct):
        # default accepted properties on various classes
        # the values are set by ES and are only here for completeness
        dct['__es_properties__'] = {
            'Any': {
                'index_name': '',
                'store': False,
                'boost': '1.0',
                'null_value': None,
                'include_in_all': True,
                'doc_values': False,
                'fielddata': {},
                'copy_to': '',
                'similarity': 'default',
                'fields': {},
                'meta_': {}
            },
            'String': {
                'analyzed': True,
                'norms': False,
                'index_options': None,
                'analyzer': 'default',
                'index_analyzer': 'default',
                'search_analyzer': 'default',
                'ignore_above': 'default',
                'position_offset_gap': 0,
                'value_': '',
                'boost_': '1.0'
            },
            'Number': {
                'type_': 'float',
                'index_': 'no',
                'precision_step': 16,
                'ignore_malformed': False,
                'coerce': True
            },
            'Integer': {
                'type_': 'float',
                'index_': 'no',
                'precision_step': 16,
                'ignore_malformed': False,
                'coerce': True
            },
            'Long': {
                'type_': 'long',
                'index_': 'no',
                'precision_step': 16,
                'ignore_malformed': False,
                'coerce': True
            },
            'Date': {
                'format': 'dateOptionalTime',
                'precision_step': 16,
                'ignore_malformed': False
            },
            'DateTime': {
                'type_': 'date',  # set explicitly because ES only has type as "date"
                'format': 'dateOptionalTime',
                'precision_step': 16,
                'ignore_malformed': False
            },
            'Binary': {
                'compress': False,
                'compress_threshold': -1
            },
            'IP': {
                'precision_step': 16
            },
            'GeoPoint': {
                'type_': 'geo_point',
                'lat_lon': False,
                'geohash': False,
                'geohash_precision': 12,
                'geohash_prefix': False,
                'validate': False,
                'validate_lat': False,
                'validate_lon': False,
                'normalize': True,
                'normalize_lat': False,
                'normalize_lon': False,
                'precision_step': 16
            },
            'GeoShape': {
                'tree': 'geohash',
                'tree_levels': '',
                'distance_error_pct': 0.5
            }
            # attachment not specified because it has no other args
        }

        dct['__es_properties__']['Array'] = {}
        for k, v in iteritems(dct['__es_properties__']):
            if k == 'Array':
                continue

            dct['__es_properties__']['Array'].update(v)

        def get_prop_dict(self):
            es_type = self.__class__.__name__.lower()
            prop_dict = {"type": es_type}

            valid = []
            for obj in self.__class__.mro():
                if obj.__name__ in self.__es_properties__:
                    valid.extend(list(self.__es_properties__.get(obj.__name__)))

            valid.extend(list(self.__es_properties__.get('Any')))

            for k in dir(self):
                if k in valid:
                    v = getattr(self, k)

                    keyname = k
                    if k[len(k) - 1] == "_":
                        if k in ['meta_', 'value_', 'boost_']:
                            keyname = '_' + k[0:len(k) - 1]
                        else:
                            keyname = k[0:len(k) - 1]

                    elif k == 'analyzed':
                        keyname = 'index'
                        if v or v == None:
                            v = 'analyzed'
                        else:
                            v = 'not_analyzed'

                    if v != None:
                        if isinstance(v, dict) or isinstance(v, list):
                            v = self.__class__.build_map(v)

                        prop_dict[keyname] = v

            return prop_dict

        # for recreating the arguments in a new instance
        def get_es_arguments(self):
            arg_dict = {}
            valid = {}
            valid.update(self.__es_properties__.get('Any'))

            try:
                valid.update(self.__es_properties__.get(self.__class__.__name__))
            except TypeError:
                pass

            for k in dir(self):
                if k in valid:
                    v = getattr(self, k)
                    arg_dict[k] = v
            return arg_dict

        dct['prop_dict'] = get_prop_dict
        dct['es_args'] = get_es_arguments

        return super(ESType, cls).__new__(cls, clsname, bases, dct)

    def __call__(cls, *args, **kwargs):
        # we have to split kw args going to the base class
        # and args that are for elastic search
        # annoying but not a big deal
        base_kwargs = {}
        es_kwargs = {}
        _name_ = cls.__name__

        valid = []
        for obj in cls.mro():
            if obj.__name__ in cls.__es_properties__:
                valid.extend(list(cls.__es_properties__.get(obj.__name__)))
        valid.extend(list(cls.__es_properties__.get('Any')))

        for k, v in iteritems(kwargs):
            if k in valid:
                es_kwargs[k] = v
            else:
                base_kwargs[k] = v

        # fix for datetime calls. I really dont like this but I can't seem
        # to hook it anywhere

        if len(args) == 1:
            a = args[0]
            if cls == DateTime and isinstance(a, datetime):
                args = [a.year, a.month, a.day, a.hour, a.minute, a.second]

                if a.tzinfo:
                    base_kwargs['tzinfo'] = a.tzinfo

            elif cls == Date and isinstance(a, date):
                args = [a.year, a.month, a.day]

        inst = super(ESType, cls).__call__(*args, **base_kwargs)

        for k, v in iteritems(es_kwargs):
            setattr(inst, k, v)  # testing

        return inst


# lists
@add_metaclass(ESType)
class Array(list):
    type_ = 'string'  # default


# converts strings to unicode
@add_metaclass(ESType)
class String(unicode):
    pass


@add_metaclass(ESType)
class Number(float):
    precision_step = 8
    coerce_ = True


@add_metaclass(ESType)
class Float(Number):
    type_ = 'float'


@add_metaclass(ESType)
class Double(Number):
    type_ = 'double'
    precision_step = 16


@add_metaclass(ESType)
class Integer(int):
    precision_step = 8
    coerce_ = True
    type_ = 'integer'


@add_metaclass(ESType)
class Long(long):
    coerce_ = True
    type_ = 'long'
    precision_step = 16


@add_metaclass(ESType)
class Short(Integer):
    type_ = 'short'


@add_metaclass(ESType)
class Byte(Number):
    type_ = 'byte'
    precision_step = 2147483647  # wat? (its from the ES docs)


@add_metaclass(ESType)
class TokenCount(Number):
    analyzer = 'standard'


@add_metaclass(ESType)
class DateTime(datetime):
    type_ = 'date'
    precision_step = 16
    ignore_malformed = False

    def date(self):
        value = super(DateTime, self).date()
        return Date(value)

        # TODO allow format changes
        # for now just does default


@add_metaclass(ESType)
class Date(date):
    precision_step = 16
    ignore_malformed = False


@add_metaclass(ESType)
class Boolean(object):
    # can't extend bool :(
    # making it extend int did weird things in ES
    # so it extends object and tries to act like a bool
    # in base this class is detected and regular bools are always set as the attribute to be sent

    def __init__(self, value, **kwargs):
        self.value = bool(value)
    
    def __bool__(self):
        return self.value

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        return str(self.value)


@add_metaclass(ESType)
class Binary(object):
    compress = False
    compress_threshold = -1


@add_metaclass(ESType)
class IP(String):
    pass


@add_metaclass(ESType)
class GeoPoint(object):
    type_ = 'geo_point'
    lat_lon = False
    geohash = False
    geohash_precision = None  # use default
    geohash_prefix = False
    validate = False
    validate_lat = False
    validate_lon = False
    normalize = True
    normalize_lat = False
    normalize_lon = False


@add_metaclass(ESType)
class GeoShape(object):
    tree = 'geohash'
    precision = 'meters'

    # TODO - do we want to internally implement all the GeoJSON that goes along with this?


@add_metaclass(ESType)
class Attachment(object):
    pass
