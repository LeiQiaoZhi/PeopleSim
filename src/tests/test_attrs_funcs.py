import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
print(parent)
sys.path.insert(0, parent)

try:
    import unittest
    from standards import *
    from attributes import *
    from person import Person
    from attr_funcs import *
except:
    print("Can't load packages")
    quit()


class TestAttrsFuncs(unittest.TestCase):
    def test_mort_rate_100_is_mid_point(self):
        basic_attrs = BasicAttributes.get_random_attributes(
            age_bounds=(100, 101))
        mort_rate = get_mortality_rate(basic_attrs)
        self.assertEqual(mort_rate, 0.5)


if __name__ == '__main__':
    unittest.main()
