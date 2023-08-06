
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

from humanizer.tests import helper

from humanizer import duration


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    def test__import(self):
        self.assertModule(duration)

    def test_value(self):
        self.assertTrue(callable(duration.value))

        second = 1
        minute = 60 * second
        hour = 60 * minute
        day = 24 * hour

        # second: value (number)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value(None)

        self.assertEqual(result, 0)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value(0)

        self.assertEqual(result, 0)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value(1 * second)

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value(1 * minute)

        self.assertEqual(result, 1 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value(1 * hour)

        self.assertEqual(result, 1 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value(1 * day)

        self.assertEqual(result, 1 * day)

        # second: value (string)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000')

        # second: value + unit (string)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0s')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 s')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0second')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 second')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0seconds')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 seconds')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0Second')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 Second')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0Seconds')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 Seconds')

        self.assertEqual(result, 0 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1s')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 s')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1second')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 second')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1seconds')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 seconds')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1Second')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 Second')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1Seconds')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 Seconds')

        self.assertEqual(result, 1 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2s')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 s')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2second')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 second')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2seconds')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 seconds')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2Second')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 Second')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2Seconds')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 Seconds')

        self.assertEqual(result, 2 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000s')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 s')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000second')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 second')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000seconds')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 seconds')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000Second')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 Second')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000Seconds')

        self.assertEqual(result, 1000 * second)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 Seconds')

        self.assertEqual(result, 1000 * second)

        # minute

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0m')

        self.assertEqual(result, 0 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 m')

        self.assertEqual(result, 0 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0M')

        self.assertEqual(result, 0 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 M')

        self.assertEqual(result, 0 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0minute')

        self.assertEqual(result, 0 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 minute')

        self.assertEqual(result, 0 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0minutes')

        self.assertEqual(result, 0 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 minutes')

        self.assertEqual(result, 0 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719minute')

        self.assertEqual(result, 0.214642524719 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719 minute')

        self.assertEqual(result, 0.214642524719 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719minutes')

        self.assertEqual(result, 0.214642524719 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1m')

        self.assertEqual(result, 1 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 m')

        self.assertEqual(result, 1 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1minute')

        self.assertEqual(result, 1 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 minute')

        self.assertEqual(result, 1 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1minutes')

        self.assertEqual(result, 1 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 minutes')

        self.assertEqual(result, 1 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2m')

        self.assertEqual(result, 2 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 m')

        self.assertEqual(result, 2 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2minute')

        self.assertEqual(result, 2 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 minute')

        self.assertEqual(result, 2 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2minutes')

        self.assertEqual(result, 2 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 minutes')

        self.assertEqual(result, 2 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000m')

        self.assertEqual(result, 1000 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 m')

        self.assertEqual(result, 1000 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000minute')

        self.assertEqual(result, 1000 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 minute')

        self.assertEqual(result, 1000 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000minutes')

        self.assertEqual(result, 1000 * minute)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 minutes')

        self.assertEqual(result, 1000 * minute)

        # hour

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0h')

        self.assertEqual(result, 0 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 h')

        self.assertEqual(result, 0 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0hour')

        self.assertEqual(result, 0 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 hour')

        self.assertEqual(result, 0 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0hours')

        self.assertEqual(result, 0 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 hours')

        self.assertEqual(result, 0 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719h')

        self.assertEqual(result, 0.214642524719 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719 h')

        self.assertEqual(result, 0.214642524719 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719H')

        self.assertEqual(result, 0.214642524719 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719 H')

        self.assertEqual(result, 0.214642524719 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719hour')

        self.assertEqual(result, 0.214642524719 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719 hour')

        self.assertEqual(result, 0.214642524719 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0.214642524719hours')

        self.assertEqual(result, 0.214642524719 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 hours')

        self.assertEqual(result, 0 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1h')

        self.assertEqual(result, 1 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 h')

        self.assertEqual(result, 1 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1hour')

        self.assertEqual(result, 1 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 hour')

        self.assertEqual(result, 1 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1hours')

        self.assertEqual(result, 1 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 hours')

        self.assertEqual(result, 1 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2h')

        self.assertEqual(result, 2 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 h')

        self.assertEqual(result, 2 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2hour')

        self.assertEqual(result, 2 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 hour')

        self.assertEqual(result, 2 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2hours')

        self.assertEqual(result, 2 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 hours')

        self.assertEqual(result, 2 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000h')

        self.assertEqual(result, 1000 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 h')

        self.assertEqual(result, 1000 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000hour')

        self.assertEqual(result, 1000 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 hour')

        self.assertEqual(result, 1000 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000hours')

        self.assertEqual(result, 1000 * hour)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 hours')

        self.assertEqual(result, 1000 * hour)

        # day

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0d')

        self.assertEqual(result, 0 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 d')

        self.assertEqual(result, 0 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0D')

        self.assertEqual(result, 0 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 D')

        self.assertEqual(result, 0 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0day')

        self.assertEqual(result, 0 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 day')

        self.assertEqual(result, 0 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0days')

        self.assertEqual(result, 0 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('0 days')

        self.assertEqual(result, 0 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1d')

        self.assertEqual(result, 1 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 d')

        self.assertEqual(result, 1 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1day')

        self.assertEqual(result, 1 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 day')

        self.assertEqual(result, 1 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1days')

        self.assertEqual(result, 1 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1 days')

        self.assertEqual(result, 1 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2d')

        self.assertEqual(result, 2 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 d')

        self.assertEqual(result, 2 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2day')

        self.assertEqual(result, 2 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 day')

        self.assertEqual(result, 2 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2days')

        self.assertEqual(result, 2 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('2 days')

        self.assertEqual(result, 2 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000d')

        self.assertEqual(result, 1000 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 d')

        self.assertEqual(result, 1000 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000day')

        self.assertEqual(result, 1000 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 day')

        self.assertEqual(result, 1000 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000days')

        self.assertEqual(result, 1000 * day)

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.value('1000 days')

        self.assertEqual(result, 1000 * day)

    def test_human(self):
        self.assertTrue(callable(duration.human))

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human(None)

        self.assertEqual(result, None)

        # seconds => seconds

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human(0, 's')

        self.assertEqual(result, '0 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human(1000, 's')

        self.assertEqual(result, '1000 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 s', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1s', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 S', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1S', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 second', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1second', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 seconds', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1seconds', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Second', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Second', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Seconds', 's')

        self.assertEqual(result, '1 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Seconds', 's')

        self.assertEqual(result, '1 s')

        # seconds => minutes

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human(0, 'm')

        self.assertEqual(result, '0 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 s', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1s', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 second', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1second', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 seconds', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1seconds', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Second', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Second', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Seconds', 'm')

        self.assertEqual(result, '0.02 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Seconds', 'm')

        self.assertEqual(result, '0.02 m')

        # seconds => hours

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human(0, 'h')

        self.assertEqual(result, '0 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 s', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1s', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 second', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1second', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 seconds', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1seconds', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Second', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Second', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Seconds', 'h')

        self.assertEqual(result, '0.0003 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Seconds', 'h')

        self.assertEqual(result, '0.0003 h')

        # minutes => seconds

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 m', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1m', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minute', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minute', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minutes', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minutes', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minute', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minute', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minutes', 's')

        self.assertEqual(result, '60 s')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minutes', 's')

        self.assertEqual(result, '60 s')

        # minutes => minutes

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 m', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1m', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minute', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minute', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minutes', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minutes', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minute', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minute', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minutes', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minutes', 'm')

        self.assertEqual(result, '1 m')

        # minutes => hours

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 m', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1m', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minute', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minute', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minutes', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minutes', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minute', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minute', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minutes', 'h')

        self.assertEqual(result, '0.02 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minutes', 'h')

        self.assertEqual(result, '0.02 h')

        # minutes => days

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 m', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1m', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minute', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minute', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minutes', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minutes', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minute', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minute', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minutes', 'd')

        self.assertEqual(result, '0.0007 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minutes', 'd')

        self.assertEqual(result, '0.0007 d')

        # hours => seconds

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 m', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1m', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minute', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minute', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 minutes', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1minutes', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minute', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minute', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Minutes', 'm')

        self.assertEqual(result, '1 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Minutes', 'm')

        self.assertEqual(result, '1 m')

        # hours => minutes

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 h', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1h', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 hour', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1hour', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 hours', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1hours', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Hour', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Hour', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Hours', 'm')

        self.assertEqual(result, '60 m')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Hours', 'm')

        self.assertEqual(result, '60 m')

        # hours => hours

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 h', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1h', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 hour', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1hour', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 hours', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1hours', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Hour', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Hour', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Hours', 'h')

        self.assertEqual(result, '1 h')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Hours', 'h')

        self.assertEqual(result, '1 h')

        # hours => days

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 h', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1h', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 hour', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1hour', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 hours', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1hours', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Hour', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Hour', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1 Hours', 'd')

        self.assertEqual(result, '0.04 d')

        with self.assertNotRaises(duration.HumanizerError):
            result = duration.human('1Hours', 'd')

        self.assertEqual(result, '0.04 d')


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':
    helper.run(TestCase)
