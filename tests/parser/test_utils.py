import unittest
from datetime import datetime

from ogn.parser.utils import dmsToDeg, createTimestamp
from ogn.parser.exceptions import AmbigousTimeError


class TestStringMethods(unittest.TestCase):
    def test_dmsToDeg(self):
        dms = 50.4830
        self.assertAlmostEqual(dmsToDeg(dms), 50.805, 5)

    def test_createTimestamp(self):
        test_data = [
            ('000001', datetime(2015, 1, 10, 0, 0, 1), datetime(2015, 1, 10, 0, 0, 1)),      # packet from current day (on the tick)
            ('235959', datetime(2015, 1, 10, 0, 0, 1), datetime(2015, 1, 9, 23, 59, 59)),    # packet from previous day (2 seconds old)
            ('110000', datetime(2015, 1, 10, 0, 0, 1), None),                                # packet 11 hours from future or 13 hours old
            ('123500', datetime(2015, 1, 10, 23, 50, 0), datetime(2015, 1, 10, 12, 35, 0)),  # packet from current day (11 hours old)
            ('000001', datetime(2015, 1, 10, 23, 50, 0), datetime(2015, 1, 11, 0, 0, 1))     # packet from next day (11 minutes from future)
        ]

        for test in test_data:
            if test[2]:
                timestamp = createTimestamp(test[0], reference=test[1])
                self.assertEqual(timestamp, test[2])
            else:
                with self.assertRaises(AmbigousTimeError):
                    createTimestamp(test[0], reference=test[1])


if __name__ == '__main__':
    unittest.main()
