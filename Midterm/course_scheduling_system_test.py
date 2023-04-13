import unittest
from unittest.mock import Mock
import course_scheduling_system

class CSSTest(unittest.TestCase):

    def test_q1_1(self):
        CSS = course_scheduling_system.CSS()
        CSS.check_course_exist = Mock()

        def check(course):
            return True
        
        CSS.check_course_exist.side_effect = check
        courses = [('Algorithms', 'Monday', 3, 4)]
        for c in courses:
            self.assertTrue(CSS.add_course(c))
        self.assertEqual(CSS.get_course_list(), courses)

    def test_q1_2(self):
        CSS = course_scheduling_system.CSS()
        CSS.check_course_exist = Mock()

        def check(course):
            return True
        
        CSS.check_course_exist.side_effect = check
        courses = [('Algorithm', 'Monday', 3, 4), ('Software Testing' , 'Monday', 4, 5)]
        for c in courses:
            rtn = CSS.add_course(c)
        self.assertFalse(rtn)
        self.assertEqual(CSS.get_course_list(), [courses[0]])
    
    def test_q1_3(self):
        CSS = course_scheduling_system.CSS()
        CSS.check_course_exist = Mock()

        def check(course):
            return False
        
        CSS.check_course_exist.side_effect = check
        courses = [('Algorithm', 'Monday', 3, 4)]
        for c in courses:
            self.assertFalse(CSS.add_course(c))
    
    def test_q1_4(self):
        CSS = course_scheduling_system.CSS()
        CSS.check_course_exist = Mock()

        def check(course):
            return True

        CSS.check_course_exist.side_effect = check
        courses = [('Algorithm', 'Monday', 3)]
        with self.assertRaises(TypeError):
            for c in courses:
                CSS.add_course(c)

    def test_q1_5(self):
        CSS = course_scheduling_system.CSS()
        CSS.check_course_exist = Mock()

        def check(course):
            return True

        CSS.check_course_exist.side_effect = check
        courses = [('Algorithm', 'Monday', 3, 4), ('Software Testing', 'Thursday', 5, 6), ('Machine Learning', 'Thursday', 3, 4)]
        for c in courses:
            CSS.add_course(c)
        CSS.remove_course(courses[1])
        self.assertEqual(CSS.get_course_list(), courses[::2])
        self.assertEqual(CSS.check_course_exist.call_count, len(courses)+1) 
        print(CSS.__str__())

if __name__ == '__main__':
    unittest.main()