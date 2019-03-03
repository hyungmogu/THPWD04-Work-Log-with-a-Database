import unittest

from main import Program

# --------
# General
# --------

# --------
# Main Page
# --------
class TestGetErrorMessageMainPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('main')

    def test_return_error_message_if_menu_is_empty(self):
        expected = "Sorry. There are no items in menu. Please exit program (Ctrl + c) and try again."

        result = self.program._get_error_message_main_page('h',[])

        self.assertEqual(expected, result)

    def test_return_error_message_if_response_is_empty(self):
        expected = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(self.menu) - 1))

        result = self.program._get_error_message_main_page('', self.menu)

        self.assertEqual(expected, result)

    def test_return_error_message_if_response_is_other_than_letters(self):
        expected = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(self.menu) - 1))

        result1 = self.program._get_error_message_main_page('*', self.menu)
        result2 = self.program._get_error_message_main_page('1', self.menu)
        result3 = self.program._get_error_message_main_page(' ', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_error_message_if_response_is_other_than_whats_assigned_to_menu(self):
        expected = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(self.menu) - 1))

        result1 = self.program._get_error_message_main_page('z', self.menu)
        result2 = self.program._get_error_message_main_page('d', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_none_if_response_is_within_whats_assigned(self):
        expected = ''

        result1 = self.program._get_error_message_main_page('a', self.menu)
        result2 = self.program._get_error_message_main_page('c', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
# --------

class TestIsResponseValidMainPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('main')

    def test_return_false_if_response_is_empty(self):
        expected = False

        result = self.program._is_response_valid_main_page('', self.menu)

        self.assertEqual(expected, result)

    def test_return_false_if_response_is_other_than_letters(self):
        expected = False

        result1 = self.program._is_response_valid_main_page('*', self.menu)
        result2 = self.program._is_response_valid_main_page('1', self.menu)
        result3 = self.program._is_response_valid_main_page(' ', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_false_if_response_is_other_than_whats_assigned_to_menu(self):
        expected = False

        result1 = self.program._is_response_valid_main_page('z', self.menu)
        result2 = self.program._is_response_valid_main_page('d', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_true_if_response_is_within_whats_assigned(self):
        expected = True

        result1 = self.program._is_response_valid_main_page('a', self.menu)
        result2 = self.program._is_response_valid_main_page('c', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
# --------
# Add Page
# --------

# --------
# Search Page
# --------

# --------
# Search By Date Page
# --------

# --------
# Search By Time Page
# --------

# --------
# Search By Regex or Exact Words Page
# --------

# --------
# Display Page
# --------


if __name__ == '__main__':
    unittest.main()