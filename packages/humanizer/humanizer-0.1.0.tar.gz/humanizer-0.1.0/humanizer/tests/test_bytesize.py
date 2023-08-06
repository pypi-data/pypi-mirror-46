
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

from humanizer.tests import helper

from humanizer import bytesize


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    def test__import(self):
        self.assertModule(bytesize)

    def test_value(self):
        self.assertTrue(callable(bytesize.value))

        byte = 1
        kilobyte = 1024 * byte
        megabyte = 1024 * kilobyte
        gigabyte = 1024 * megabyte

        # byte: value (number)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value(None)

        self.assertEqual(result, 0)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value(0)

        self.assertEqual(result, 0)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value(1 * byte)

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value(1 * kilobyte)

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value(1 * megabyte)

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value(1 * gigabyte)

        self.assertEqual(result, 1 * gigabyte)

        # byte: value (string)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000')

        # byte: value + unit (string)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0b')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 b')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0B')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 B')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0byte')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 byte')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0bytes')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 bytes')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0Byte')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 Byte')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0Bytes')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 Bytes')

        self.assertEqual(result, 0 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1b')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 b')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1B')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 B')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1byte')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 byte')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1bytes')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 bytes')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1Byte')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 Byte')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1Bytes')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 Bytes')

        self.assertEqual(result, 1 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2b')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 b')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2B')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 B')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2byte')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 byte')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2bytes')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 bytes')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2Byte')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 Byte')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2Bytes')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 Bytes')

        self.assertEqual(result, 2 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000b')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 b')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000B')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 B')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000byte')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 byte')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000bytes')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 bytes')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000Byte')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 Byte')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000Bytes')

        self.assertEqual(result, 1000 * byte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 Bytes')

        self.assertEqual(result, 1000 * byte)

        # kilobyte

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0kb')

        self.assertEqual(result, 0 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 kb')

        self.assertEqual(result, 0 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0kB')

        self.assertEqual(result, 0 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 kB')

        self.assertEqual(result, 0 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0kilobyte')

        self.assertEqual(result, 0 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 kilobyte')

        self.assertEqual(result, 0 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0kilobytes')

        self.assertEqual(result, 0 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 kilobytes')

        self.assertEqual(result, 0 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719kb')

        self.assertEqual(result, int(round(0.214642524719 * kilobyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719 kb')

        self.assertEqual(result, int(round(0.214642524719 * kilobyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719KB')

        self.assertEqual(result, int(round(0.214642524719 * kilobyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719 KB')

        self.assertEqual(result, int(round(0.214642524719 * kilobyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719kilobyte')

        self.assertEqual(result, int(round(0.214642524719 * kilobyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719 kilobyte')

        self.assertEqual(result, int(round(0.214642524719 * kilobyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719kilobytes')

        self.assertEqual(result, int(round(0.214642524719 * kilobyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1kb')

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 kb')

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1kB')

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 kB')

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1kilobyte')

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 kilobyte')

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1kilobytes')

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 kilobytes')

        self.assertEqual(result, 1 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2kb')

        self.assertEqual(result, 2 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 kb')

        self.assertEqual(result, 2 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2kB')

        self.assertEqual(result, 2 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 kB')

        self.assertEqual(result, 2 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2kilobyte')

        self.assertEqual(result, 2 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 kilobyte')

        self.assertEqual(result, 2 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2kilobytes')

        self.assertEqual(result, 2 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 kilobytes')

        self.assertEqual(result, 2 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000kb')

        self.assertEqual(result, 1000 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 kb')

        self.assertEqual(result, 1000 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000kB')

        self.assertEqual(result, 1000 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 kB')

        self.assertEqual(result, 1000 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000kilobyte')

        self.assertEqual(result, 1000 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 kilobyte')

        self.assertEqual(result, 1000 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000kilobytes')

        self.assertEqual(result, 1000 * kilobyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 kilobytes')

        self.assertEqual(result, 1000 * kilobyte)

        # megabyte

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0mb')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 mb')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0MB')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 MB')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0megabyte')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 megabyte')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0megabytes')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 megabytes')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719mb')

        self.assertEqual(result, int(round(0.214642524719 * megabyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719 mb')

        self.assertEqual(result, int(round(0.214642524719 * megabyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719MB')

        self.assertEqual(result, int(round(0.214642524719 * megabyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719 MB')

        self.assertEqual(result, int(round(0.214642524719 * megabyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719megabyte')

        self.assertEqual(result, int(round(0.214642524719 * megabyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719 megabyte')

        self.assertEqual(result, int(round(0.214642524719 * megabyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0.214642524719megabytes')

        self.assertEqual(result, int(round(0.214642524719 * megabyte)))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 megabytes')

        self.assertEqual(result, 0 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1mb')

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 mb')

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1MB')

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 MB')

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1megabyte')

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 megabyte')

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1megabytes')

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 megabytes')

        self.assertEqual(result, 1 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2mb')

        self.assertEqual(result, 2 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 mb')

        self.assertEqual(result, 2 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2MB')

        self.assertEqual(result, 2 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 MB')

        self.assertEqual(result, 2 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2megabyte')

        self.assertEqual(result, 2 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 megabyte')

        self.assertEqual(result, 2 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2megabytes')

        self.assertEqual(result, 2 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 megabytes')

        self.assertEqual(result, 2 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000mb')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 mb')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000MB')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 MB')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000megabyte')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 megabyte')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000megabytes')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 megabytes')

        self.assertEqual(result, 1000 * megabyte)

        # gigabyte

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0gb')

        self.assertEqual(result, 0 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 gb')

        self.assertEqual(result, 0 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0GB')

        self.assertEqual(result, 0 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 GB')

        self.assertEqual(result, 0 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0gigabyte')

        self.assertEqual(result, 0 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 gigabyte')

        self.assertEqual(result, 0 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0gigabytes')

        self.assertEqual(result, 0 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('0 gigabytes')

        self.assertEqual(result, 0 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1gb')

        self.assertEqual(result, 1 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 gb')

        self.assertEqual(result, 1 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1GB')

        self.assertEqual(result, 1 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 GB')

        self.assertEqual(result, 1 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1gigabyte')

        self.assertEqual(result, 1 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 gigabyte')

        self.assertEqual(result, 1 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1gigabytes')

        self.assertEqual(result, 1 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1 gigabytes')

        self.assertEqual(result, 1 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2gb')

        self.assertEqual(result, 2 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 gb')

        self.assertEqual(result, 2 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2GB')

        self.assertEqual(result, 2 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 GB')

        self.assertEqual(result, 2 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2gigabyte')

        self.assertEqual(result, 2 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 gigabyte')

        self.assertEqual(result, 2 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2gigabytes')

        self.assertEqual(result, 2 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('2 gigabytes')

        self.assertEqual(result, 2 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000gb')

        self.assertEqual(result, 1000 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 gb')

        self.assertEqual(result, 1000 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000GB')

        self.assertEqual(result, 1000 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 GB')

        self.assertEqual(result, 1000 * gigabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000megabyte')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 megabyte')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000megabytes')

        self.assertEqual(result, 1000 * megabyte)

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.value('1000 megabytes')

        self.assertEqual(result, 1000 * megabyte)


    def test_human(self):
        self.assertTrue(callable(bytesize.human))

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human(None)

        self.assertEqual(result, None)

        # bytes => bytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human(0, 'b')

        self.assertEqual(result, '0 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human(1024, 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 b', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1b', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 B', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1B', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 byte', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1byte', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 Byte', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1Byte', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 bytes', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1bytes', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 Bytes', 'b')

        self.assertEqual(result, '1 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1Bytes', 'b')

        self.assertEqual(result, '1 B')

        # bytes => kilobytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human(0, 'kb')

        self.assertEqual(result, '0 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human(1024, 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 b', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1b', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 B', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1B', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 byte', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1byte', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 Byte', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1Byte', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 bytes', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1bytes', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 Bytes', 'kb')

        self.assertEqual(result, '0.001 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1Bytes', 'kb')

        self.assertEqual(result, '0.001 kB')

        # bytes => megabytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human(0, 'mb')

        self.assertEqual(result, '0 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human(1024, 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 b', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1b', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 B', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1B', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 byte', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1byte', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 Byte', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1Byte', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 bytes', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1bytes', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 Bytes', 'mb')

        self.assertEqual(result, '0.000001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1Bytes', 'mb')

        self.assertEqual(result, '0.000001 MB')

        # kilobytes => bytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kb', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kb', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kB', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kB', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kilobyte', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kilobyte', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kiloByte', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kiloByte', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kilobytes', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kilobytes', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kiloBytes', 'b')

        self.assertEqual(result, '1024 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kiloBytes', 'b')

        self.assertEqual(result, '1024 B')

        # kilobytes => kilobytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kb', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kb', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kB', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kB', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kilobyte', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kilobyte', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kiloByte', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kiloByte', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kilobytes', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kilobytes', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kiloBytes', 'kb')

        self.assertEqual(result, '1 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kiloBytes', 'kb')

        self.assertEqual(result, '1 kB')

        # kilobytes => megabytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kb', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kb', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kB', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kB', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kilobyte', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kilobyte', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kiloByte', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kiloByte', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kilobytes', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kilobytes', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 kiloBytes', 'mb')

        self.assertEqual(result, '0.001 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1kiloBytes', 'mb')

        self.assertEqual(result, '0.001 MB')

        # metabytes => bytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 mb', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1mb', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MB', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1MB', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 megabyte', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1megabyte', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MegaByte', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1MegaByte', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MegaBytes', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1MegaBytes', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MegaBytes', 'b')

        self.assertEqual(result, '1048576 B')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1MegaBytes', 'b')

        self.assertEqual(result, '1048576 B')

        # megabytes => kilobytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 mb', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1mb', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MB', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1MB', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 megabyte', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1megabyte', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MegaByte', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MegaByte', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 megabytes', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1megabytes', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MegaBytes', 'kb')

        self.assertEqual(result, '1024 kB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1MegaBytes', 'kb')

        self.assertEqual(result, '1024 kB')

        # megabytes => megabytes

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 mb', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1mb', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MB', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1MB', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 megabyte', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1megabyte', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 megaByte', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 megaByte', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 megabytes', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1megabytes', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1 MegaBytes', 'mb')

        self.assertEqual(result, '1 MB')

        with self.assertNotRaises(bytesize.HumanizerError):
            result = bytesize.human('1MegaBytes', 'mb')

        self.assertEqual(result, '1 MB')


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':
    helper.run(TestCase)
