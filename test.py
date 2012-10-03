import unittest

from mock import Mock
from mock import patch

from urbandict import define


class DefineTest(unittest.TestCase):

    EASY = open('fixtures/easy.html').read().encode('utf-8')
    SHORT = open('fixtures/short.html').read().encode('utf-8')

    @patch('urbandict.urlopen')
    def test_can_run_twice_and_get_different_results(self, urlopen):
        urlopen.return_value = Mock(read=lambda: self.EASY)
        self.assertEqual({'word': 'easy',
                          'example': 'Teacher: DO YOUR WORK NOW!!!!'
                                     'Student: Easy.....',
                          'def': 'A way to say calm the fuck down without '
                                 'getting in trouble, you little shit.......'},
                          define('easy')[0])

        urlopen.return_value = Mock(read=lambda: self.SHORT)
        self.assertEqual({'word': 'short', 'example': '',
                          'def': 'Someone under the 25th percentile for '
                                 'stature for their age, sex, and country.\n'
                                 "(5'7 and under for men and 5'2 and under for "
                                 'women in the US)'}, define('short')[0])


if __name__ == '__main__':
    unittest.main()
