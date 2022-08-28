import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
print(parent)
sys.path.insert(0, parent)

try:
    import unittest
    from standards import *
    from person import Person
except:
    print("Can't load packages")
    quit()


class TestHeightStds(unittest.TestCase):
    def test_default_func_without_param(self):
        person = Person.generate_random_person()
        std = HeightStandard.LOWER_THE_BETTER()
        score = std.score_fn(person, 0)
        self.assertGreater(score, 0)

    def test_lower_the_better_with_param(self):
        person = Person.generate_random_person()
        std = HeightStandard.LOWER_THE_BETTER(half_score_height=170)
        score = std.score_fn(person, 160)
        self.assertGreater(score, 0.5)
        score = std.score_fn(person, 180)
        self.assertLess(score, 0.5)

    def test_higher_the_better_with_param(self):
        person = Person.generate_random_person()
        std = HeightStandard.HIGHER_THE_BETTER(half_score_height=170)
        score = std.score_fn(person, 180)
        self.assertGreater(score, 0.5)
        score = std.score_fn(person, 160)
        self.assertLess(score, 0.5)

    def test_must_higher_than_with_param(self):
        person = Person.generate_random_person()
        std = HeightStandard.MUST_ABOVE_HEIGHT(min_height=170)
        score = std.score_fn(person, 180)
        self.assertEqual(score, 1)
        score = std.score_fn(person, 160)
        self.assertEqual(score, 0)

    def test_must_higher_than_without_param(self):
        person = Person.generate_random_person()
        person.physical_attrs.height = 170
        std = HeightStandard.MUST_ABOVE_HEIGHT()
        score = std.score_fn(person, 180)
        self.assertEqual(score, 1)
        score = std.score_fn(person, 160)
        self.assertEqual(score, 0)

    def test_must_lower_than_with_param(self):
        person = Person.generate_random_person()
        std = HeightStandard.MUST_BELOW_HEIGHT(max_height=170)
        score = std.score_fn(person, 160)
        self.assertEqual(score, 1)
        score = std.score_fn(person, 180)
        self.assertEqual(score, 0)

    def test_must_lower_than_without_param(self):
        person = Person.generate_random_person()
        person.physical_attrs.height = 170
        std = HeightStandard.MUST_BELOW_HEIGHT()
        score = std.score_fn(person, 160)
        self.assertEqual(score, 1)
        score = std.score_fn(person, 180)
        self.assertEqual(score, 0)

    def test_no_height_std(self):
        person = Person.generate_random_person()
        std = HeightStandard.NO_HEIGHT_STANDARD()
        score = std.score_fn(person, 0)
        self.assertEqual(score, 1)
        score = std.score_fn(person, 180)
        self.assertEqual(score, 1)


if __name__ == '__main__':
    unittest.main()
