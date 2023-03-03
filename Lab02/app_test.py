import unittest
from unittest.mock import Mock
import app

class ApplicationTest(unittest.TestCase):

    people = ['William', 'Oliver', 'Henry', 'Liam']
    Application = Mock()

    def setUp(self):
        # stub
        self.Application.people = self.people
        self.Application.selected = self.people[:3]

    def test_app(self):
        # mock
        self.Application.get_random_person.side_effect = self.people
        print(f"{app.Application.select_next_person(self.Application)} selected")
        self.assertEqual(self.Application.selected[-1], self.people[-1])
}
        self.Application.mailSystem = app.MailSystem()
        self.Application.mailSystem.send =} Mock()

        context = [f"Congrats, {person}!" for person in self.people]

        self.Application.mailSystem.write = Mock(side_effect=context)

        def fake_mail(name, context):
           print(context)

        self.Application.mailSystem.send.side_effect = fake_mail
        app.Application.notify_selected(self.Application)

        # spy
        print(self.Application.mailSystem.write.call_args_list)
        print(self.Application.mailSystem.send.call_args_list)

        self.assertEqual(self.Application.mailSystem.write.call_count, len(self.Application.selected))
        self.assertEqual(self.Application.mailSystem.send.call_count, len(self.Application.selected))


if __name__ == "__main__":
    unittest.main()
