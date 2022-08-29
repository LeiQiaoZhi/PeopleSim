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
except:
    print("Can't load packages")
    quit()


class TestAttrs(unittest.TestCase):
    def test_get_random_basic_attrs(self):
        attr = BasicAttributes.get_random_attributes(age_bounds=(99, 100))
        self.assertEqual(attr.age, 99)

    def test_get_random_basic_attrs_default_age(self):
        attr = BasicAttributes.get_random_attributes()
        self.assertEqual(attr.age, 0)


if __name__ == '__main__':
    unittest.main()
