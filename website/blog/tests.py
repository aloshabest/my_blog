from django.test import TestCase

class TestStringMethods(TestCase):
    def test_length(self):
        self.assertEqual(len('blog'), 4)

    def test_show_msg(self):
        self.assertTrue(False, msg="Важная проверка на истинность")