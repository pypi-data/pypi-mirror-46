from __future__ import unicode_literals

import datetime
import json
import re
import sys

import bleach as bleach
import pytz
from dateutil.parser import parse
from django.conf import settings

if sys.version_info[0] > 2:
    from future.types.newstr import unicode
    from future.standard_library import install_aliases

    # For the future library so we can be Python 2 and 3 compatible
    install_aliases()


def clean_api_results(api_result, **kwargs):
    """
    This function will accept, a list, dictionary, or string.
    If a list or dictionary is provided, it will recursively traverse through it, and run bleach on all string values.
    If a string is provided, it will bleach that string.
    Any other data type is simply returned as-is.

    :param input_dict:
    :return:
    """
    retn = None

    if isinstance(api_result, (str, unicode)):

        retn = bleach.clean(api_result)

    elif isinstance(api_result, dict):
        retn = {}

        for k, v in api_result.items():

            if isinstance(v, (str, unicode)):
                retn[k] = bleach.clean(v)

            else:
                retn[k] = clean_api_results(v)

    elif isinstance(api_result, list):
        retn = []

        for list_item in api_result:
            if isinstance(list_item, (str, unicode)):

                retn.append(bleach.clean(list_item))

            elif isinstance(list_item, (dict, list)):

                retn.append(clean_api_results(list_item))

            else:
                retn.append(list_item)

    else:
        retn = api_result

    return retn


def dict_key_search(key_name, dict_to_search):
    retn = False
    if isinstance(dict_to_search, dict):
        keys = dict_to_search.keys()

        for key in keys:
            if key_name.lower() in key.lower():
                retn = key
                break

    return retn


def get_fuzzy(input_dict, dict_key):
    if dict_key in input_dict:
        key = dict_key

    else:
        key = dict_key_search(dict_key, input_dict)

    return input_dict.get(key)


def snake_to_camel(value, **kwargs):
    """
    Converts a snake_case key name to a camelCase key name, or vice versa.
    :param value: A string that you want to convert to another string type.
    :param kwargs:
        reverse - Convert from camelCase to snake_case
    :return: a converted string
    """
    do_reverse = kwargs.get('reverse', False)
    upper_case = kwargs.get('upper', False)

    parts_ex = '([A-Z])' if do_reverse else '(_[A-Za-z])'
    parts = re.findall(parts_ex, value)

    for part in parts:
        if do_reverse:
            value = value.replace(part, '_%s' % part.lower())
        else:
            value = value.replace(part, part.upper().replace('_', ''))

    if upper_case:
        value = '%s%s' % (value[0].upper(), value[1:])

    return value


def convert_keys(input_value):
    """
    Convert all of the keys in a dict (or list of dicts) recursively from CamelCase to snake_case.
    Also strips leading and trailing whitespace from string values.
    :param input_value:
    :return:
    """
    retn = None

    if isinstance(input_value, dict):
        retn = {}

        for k, v in input_value.items():
            new_key = snake_to_camel(k, reverse=True)
            if isinstance(v, dict):
                retn[new_key] = convert_keys(v)

            elif isinstance(v, list):
                retn[new_key] = convert_keys(v)

            else:
                if isinstance(v, (str, unicode)):
                    retn[new_key] = v.strip()
                else:
                    retn[new_key] = v

    elif isinstance(input_value, list):
        retn = []

        for list_item in input_value:
            if isinstance(list_item, (dict, list)):
                retn.append(convert_keys(list_item))
            else:
                if isinstance(list_item, (str, unicode)):
                    retn.append(list_item.strip())

                else:
                    retn.append(list_item)

    return retn


def make_aware_date(input_date=datetime.datetime.now()):
    """
    Adds Timezone info to a date.
    :param input_date:
    :return:
    """
    if input_date.tzinfo is None or input_date.tzinfo.utcoffset(input_date) is None:
        if not isinstance(input_date, (datetime.datetime, datetime.date)):
            input_date = format_date(input_date, return_type='datetime')

        time_zone = getattr(settings, 'TIME_ZONE', 'UTC')
        localtz = pytz.timezone(time_zone)
        aware_date = localtz.localize(input_date)

    else:
        aware_date = input_date

    return aware_date


def format_date(input_date, **kwargs):
    """
    Takes a date in many common formats and returns the date in a desired format.

    :param input_date:
    :param kwargs:
    :return:
    """
    return_type = kwargs.get('return_type', 'datetime')
    ftime_format = kwargs.get('format', '%c')
    tz_aware = kwargs.get('timezone_aware', True)

    retn = None

    if not input_date:
        input_date = datetime.datetime.now()

    if isinstance(input_date, dict):
        retn = format_dates(input_date)

    elif isinstance(input_date, (str, unicode)):
        try:
            input_date = parse(input_date)

        except ValueError:
            retn = input_date

    if isinstance(input_date, (datetime.datetime, datetime.date)):
        if tz_aware:
            input_date = make_aware_date(input_date)

        if return_type == 'datetime':
            retn = input_date

        elif return_type == 'YYYY-MM-DD':
            retn = input_date.isoformat()[0:10]

        elif return_type in ['str', 'string', 'u', 'unicode', 'text']:
            retn = input_date.strftime(ftime_format)

        else:
            retn = input_date.isoformat()

    return retn


def format_dates(input_value, **kwargs):
    """
    Format all items in a dict (or list of dicts) that have the word date in their key to YYYY-MM-DD format
    :param input_value:
    :return:
    """
    retn = None

    if isinstance(input_value, dict):
        retn = {}

        for k, v in input_value.items():
            if '_date' in k:
                retn[k] = format_date(v, **kwargs)

            elif isinstance(v, (list, dict)):
                retn[k] = format_dates(v)

            else:
                retn[k] = v

    elif isinstance(input_value, list):
        retn = []

        for list_item in input_value:
            if isinstance(list_item, (dict, list)):
                retn.append(format_dates(list_item))
            else:
                retn.append(list_item)

    return retn


def make_bool(input_value):
    retn = False

    if isinstance(input_value, bool):
        retn = input_value

    elif isinstance(input_value, (str, unicode)):
        if input_value.lower() in ['y', 't', 'true', 'yes', 'ok']:
            retn = True

    elif isinstance(input_value, int):
        retn = input_value > 0

    return retn


def make_list(thing_that_should_be_a_list):
    """If it is not a list.  Make it one. Return a list."""
    if thing_that_should_be_a_list is None:
        thing_that_should_be_a_list = []

    if not isinstance(thing_that_should_be_a_list, list):
        thing_that_should_be_a_list = [thing_that_should_be_a_list]

    return thing_that_should_be_a_list


def to_dict(input_ordered_dict):
    return json.loads(json.dumps(input_ordered_dict))
