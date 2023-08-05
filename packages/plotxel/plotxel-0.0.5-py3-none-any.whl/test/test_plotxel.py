import unittest
import numpy as np
from plotxel import smart_ticks, smart_limits


class TestSmartTicks(unittest.TestCase):

    def test_simple(self):
        a = smart_ticks([1, 2, 3, 4], [2, 3])
        a = [round(i, 1) for i in a]
        self.assertEqual([2.0, 2.2, 2.4, 2.6, 2.8], a)

    def test_non_number(self):
        data = ['howdy!', 1, 2, 3, 4]
        pass

    def test_non_iterable(self):
        data = 1
        pass

    def test_zero_range(self):
        data = [1, 1]

    def test_negative(self):
        pass

    def test_lengths(self):
        lengths = []
        for i in range(1000):
            data = np.random.rand(2)
            data -= .5
            temp_length = len(smart_ticks(data))
            lengths.append(temp_length)
        print(min(lengths), max(lengths))
        self.assertTrue(min(lengths) >= 4 and max(lengths) <= 8)


#class TestSmartLimits(unittest.TestCase):
#    def test_negative(self):
#        self.assertEqual(4, 4)

if __name__ == '__main__':
    #print(smart_ticks([0.44350199, 0.44856951]))
    #print(smart_limits([0.44350199, 0.44856951]))
    unittest.main()

