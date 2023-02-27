import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary', 'Thomas', 'Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        #TODO
        print("Start set_name test\n\n")
        for i in range(len(self.user_name)):
            self.user_id.append(self.students.set_name(self.user_name[i]))
            print(f"{self.user_id[i]} {self.students.name[self.user_id[i]]}\n")

        self.assertEqual(self.user_name, self.students.name)
        print("\n")
        print("Finish set_name test\n\n")

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        #TODO
        print("Start get_name test\n\n")
        print(f"user_id length = {len(self.user_id)}\n")
        print(f"user_name length = {len(self.students.name)}\n\n")
        self.assertEqual(len(self.user_id), len(self.students.name))

        self.user_name.append("There is no such user")
        res = []

        for i in range(len(self.user_id)+1):
            res.append(self.students.get_name(i))
            print(f"id {i} : {res[i]}\n")

        self.assertEqual(res, self.user_name)

        print("\n")
        print("Finish get_name test\n")


