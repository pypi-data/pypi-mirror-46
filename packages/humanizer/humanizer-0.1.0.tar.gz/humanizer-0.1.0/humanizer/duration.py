
# encoding: utf-8

# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

from humanizer.base import Humanizer, HumanizerError

import re


# =========================================
#       CONSTANTS
# --------------------------------------

DEFAULT_HUMANIZER_SILENT = False
DEFAULT_HUMANIZER_EXPAND = False
DEFAULT_HUMANIZER_LETTERCASE = 'default' # casing?
DEFAULT_HUMANIZER_SPACE = True # spacing?
DEFAULT_HUMANIZER_UNIT = 's'

DURATION_UNITS = [
    # NOTE: skipping lower than `s` for now - to avoid m(x)
    # 'ns',
    # 'µs',
    # 'ms',

    's',
    'm',
    'h',
    'd',

    # NOTE: skipping higher than `day` for now - to avoid lowercase (m)inute vs (m)onth
    # 'm',
    # 'y',
]

DURATION_UNITS_FORMATTED = [
    # NOTE: skipping lower than `s` for now - to avoid m(x)
    # 'ns',
    # 'µs',
    # 'ms',

    's',
    'm',
    'h',
    'd',

    # NOTE: skipping higher than `day` for now - to avoid lowercase (m)inute vs (m)onth
    # 'm',
    # 'y',
]

DURATION_UNITS_LABELS = [
    # NOTE: skipping lower than `s` for now - to avoid m(x)
    # 'ns',
    # 'µs',
    # 'ms',

    'second',
    'minute',
    'hour',
    'day',

    # NOTE: skipping higher than `day` for now - to avoid lowercase (m)inute vs (m)onth
    # 'm',
    # 'y',
]

DURATION_UNIT_VALUE_MAP = {
    # NOTE: skipping lower than `s` for now - to avoid m(x)
    # 'ns': None,
    # 'µs': None,
    # 'ms': None,

    's': 1,
    'm': 1 * 60,
    'h': 1 * 60 * 60,
    'd': 1 * 60 * 60 * 24,

    # NOTE: skipping higher than `day` for now - to avoid lowercase (m)inute vs (m)onth
    # 'm': None,
    # 'y': None,
}

DURATION_UNIT_LABEL_MAP = {
    # NOTE: skipping lower than `s` for now - to avoid m(x)
    # 'ns': None,
    # 'µs': None,
    # 'ms': None,

    's': 'second',
    'sec': 'second',
    'min': 'minute',
    'h': 'hour',
    'hr': 'hour',
    'd': 'day',

    # NOTE: skipping higher than `day` for now - to avoid lowercase (m)inute vs (m)onth
    # 'm': None,
    # 'y': None,
}

DURATION_LABELS = DURATION_UNIT_LABEL_MAP.values()

DURATION_STRING_PARSE_PATTERN = r'({0})\s*({1})?'.format('[0-9.]+', ('|').join(DURATION_UNITS))


# =========================================
#       FUNCTIONS
# --------------------------------------

# NOTE: `enumerate(reversed(x))` don't work
def _enumerate_reversed(_list):
    for index in reversed(range(len(_list))):
        yield index, _list[index]


# =========================================
#       CLASSES
# --------------------------------------

class DurationHumanizer(Humanizer):

    def __init__(self,
        unit = None,
        expand = None,
        lettercase = None,
        space = None,
    ):
        super(DurationHumanizer, self)

        self.lettercase = lettercase or DEFAULT_HUMANIZER_LETTERCASE
        self.space = space or DEFAULT_HUMANIZER_SPACE
        self.expand = expand or DEFAULT_HUMANIZER_EXPAND
        self.unit = unit or DEFAULT_HUMANIZER_UNIT

    def value(self, value = None):
        units = DURATION_UNITS
        units_labels = DURATION_UNITS_LABELS
        unit_seconds_unit_map = DURATION_UNIT_VALUE_MAP

        value_unit_pattern = DURATION_STRING_PARSE_PATTERN

        try:
            if value is None:
                return 0

            _value = str(value).lower()

            for index, unit in _enumerate_reversed(units):
                _unit = units[index]
                _unit_plural = '{}s'.format(_unit)

                _unit_label = units_labels[index]
                _unit_label_plural = '{}s'.format(_unit_label)

                _value = _value.replace(_unit_label_plural, _unit_label) # `seconds` => `s`, etc.
                _value = _value.replace(_unit_label, _unit) # `second` => `s`, etc.

            duration_value_unit_pattern = re.match(value_unit_pattern, _value, re.IGNORECASE)

            result = duration_value_unit_pattern and duration_value_unit_pattern.groups()

            if result is None or len(result) <= 0:
                raise MarkableDataHumanizerError(
                    'Expected valid number (`<value:int|float>`) or string (`"<value:int|float> <unit:string>"`) but got value `{0}` ({1})'.format(value, type(value)
                ), details = {
                    'value': value,
                    'result': result,
                })

            duration_value = dict(enumerate(result)).get(0)
            duration_unit = dict(enumerate(result)).get(1)

            _seconds = 0

            if duration_value:
                _seconds = float(duration_value)

                if duration_unit:
                    duration_unit = duration_unit.lower()
                    unit_seconds = unit_seconds_unit_map[duration_unit]

                    _seconds = _seconds * unit_seconds

            # _seconds = int(round(_seconds))
            _seconds = _seconds

            return _seconds

        except Exception as error:
            raise MarkableDataHumanizerError(error, details = {
                'value': value,
            })

    def human(self, value = None, unit = None, expand = None, lettercase = None, space = None):
        unit = unit or self.unit
        expand = expand or self.expand
        lettercase = lettercase or self.lettercase
        space = space or self.space

        units = DURATION_UNITS
        units_formatted = DURATION_UNITS_FORMATTED
        units_labels = DURATION_UNITS_LABELS

        unit_value_map = DURATION_UNIT_VALUE_MAP
        unit_label_map = DURATION_UNIT_LABEL_MAP

        try:
            if value is None:
                return None

            _value = value

            if isinstance(value, str):
                _value = self.value(_value)

            _value = float(_value)

            if unit == 'auto':
                raise NotImplementedError('Not implemented yet')

                # TODO/REVIEW: auto
                # for unit in reversed(units):
                #     unit_duration = unit_value_map[unit]

                #     if value >= unit_duration:
                #         value = value / unit_duration
                #         break # use current `value` and `unit`

            else:
                _unit = (unit or DEFAULT_HUMANIZER_UNIT).lower()
                _unit_duration = float(unit_value_map[_unit])
                _value = _value / _unit_duration

            if _value < 0:
                raise MarkableDataHumanizerError('Expected `value >= 0`, but was `{0}`'.format(_value), details = {
                    'value': _value,
                })

            if _value >= float('inf'):
                raise MarkableDataHumanizerError('Expected `value < ∞`, but was `{0}`'.format(_value), details = {
                    'value': _value,
                })

            if space:
                separator = ' '
            else:
                separator = ''

            format_string = '%(value)s %(unit)s'


            if _value.is_integer():
                _value = int(_value) # `1.0` => `1`, etc.

                value_string = format_string % dict(value = _value, unit = _unit)

            else:
                _value = float('%.1g' % _value) # `0.000123` => `0.0001`, etc.
                # _value = float(_value)

                value_string = format_string % dict(value = _value, unit = _unit)
                value_string = format_string % dict(value = '{0:.10f}'.format(_value).rstrip('0'), unit = _unit)

            if expand:
                for __unit in units:
                    value_string.replace(unit_value_map[__unit], unit_label_map[__unit]) # `s` => 'seconds', etc.

            if 'low' in lettercase or 'down' in lettercase:
                value_string = value_string.lower()

            elif 'up' in lettercase:
                value_string = value_string.upper()

            else:
                value_string = value_string.lower()

                for index, __unit in _enumerate_reversed(units[1:]):
                    value_string = value_string.replace(units[index], units_formatted[index]) # `h` => `H`, etc.

            return value_string

        except Exception as error:
            raise MarkableDataHumanizerError(error, details = {
                'value': value,
            })


# =========================================
#       FUNCTIONS
# --------------------------------------

def value(*args, **kvargs):
    return DurationHumanizer.default().value(*args, **kvargs)

def human(*args, **kvargs):
    return DurationHumanizer.default().human(*args, **kvargs)


# =========================================
#       EXPORTS
# --------------------------------------

Humanizer = DurationHumanizer

__all__ = [
    'Humanizer',

    'value',
    'human',
]
