import unittest

import mock

import urbandict


class DefineUnitTest(unittest.TestCase):

    @mock.patch("urbandict.urlquote")
    @mock.patch("urbandict.urlopen")
    def test_define_word(self, urlopen_mock, urlquote_mock):
        test_data = open('fixtures/test_data.html')
        urlopen_mock.return_value = test_data
        urlquote_mock.return_value = "xterm"

        ret = urbandict.define("xterm")
        urlopen_mock.assert_called_once()
        urlquote_mock.assert_called_once_with("xterm")
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0]['word'].strip(), 'xterm')
        self.assertTrue('def' in ret[0] and 'example' in ret[0])

    @mock.patch("urbandict.urlquote")
    @mock.patch("urbandict.urlopen")
    def test_define_random(self, urlopen_mock, urlquote_mock):
        test_data = open('fixtures/test_data.html')
        urlopen_mock.return_value = test_data
        urlquote_mock.return_value = "xterm"

        ret = urbandict.define(urbandict.TermTypeRandom())
        # as we don't pass any specific data, there's nothing
        # to quote
        urlquote_mock.assert_not_called()
        urlopen_mock.assert_called_once()
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 1)
