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

    def test_return_false_if_response_contains_more_than_one_character(self):
        expected = False

        result1 = self.program._is_response_valid_main_page('aa', self.menu)
        result2 = self.program._is_response_valid_main_page('abc', self.menu)
        result3 = self.program._is_response_valid_main_page('def', self.menu)

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
class TestIsResponseValidAddPageTaskName(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('main')
        self.prompts = self.program.model_service.get_prompts()

    def test_return_false_if_response_is_empty(self):
        expected = False

        result1 = self.program._is_response_valid_add_page_task_name('')
        result2 = self.program._is_response_valid_add_page_task_name('   ')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_true_if_not_empty(self):
        expected = True

        result1 = self.program._is_response_valid_add_page_task_name('hello')
        result2 = self.program._is_response_valid_add_page_task_name('*')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

class TestIsResponseValidAddPageTimeAmt(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('main')
        self.prompts = self.program.model_service.get_prompts()

    def test_return_false_if_response_is_empty(self):
        expected = False

        result1 = self.program._is_response_valid_add_page_time_amt('')
        result2 = self.program._is_response_valid_add_page_time_amt('   ')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_false_if_is_not_non_negative_integer(self):
        expected = False

        result1 = self.program._is_response_valid_add_page_time_amt('-10')
        result2 = self.program._is_response_valid_add_page_time_amt('hello')
        result3 = self.program._is_response_valid_add_page_time_amt('*')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_true_otherwise(self):
        expected = True

        result = self.program._is_response_valid_add_page_time_amt('60')
        result = self.program._is_response_valid_add_page_time_amt('0')

        self.assertEqual(expected, result)


class TestGetErrorMessageAddPageTaskName(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('main')
        self.prompts = self.program.model_service.get_prompts()

    def test_return_error_message_if_response_is_empty(self):
        expected = 'Please enter non-empty value'

        result1 = self.program._get_error_message_add_page_task_name('')
        result2 = self.program._get_error_message_add_page_task_name('     ')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_empty_if_otherwise(self):
        expected = ''

        result1 = self.program._get_error_message_add_page_task_name('hello')
        result2 = self.program._get_error_message_add_page_task_name('*')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

class TestGetErrorMessageAddPageTimeAmt(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('main')
        self.prompts = self.program.model_service.get_prompts()

    def test_return_error_message_if_response_empty(self):
        expected = 'Please enter non-negative integer value'

        result1 = self.program._get_error_message_add_page_time_amt('')
        result2 = self.program._get_error_message_add_page_time_amt('    ')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_error_message_if_is_not_non_negative_integer(self):
        expected = 'Please enter non-negative integer value'

        result1 = self.program._get_error_message_add_page_time_amt('-10')
        result2 = self.program._get_error_message_add_page_time_amt('hello')
        result3 = self.program._get_error_message_add_page_time_amt('*')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_empty_otherwise(self):
        expected = ''

        result1 = self.program._get_error_message_add_page_time_amt('60')
        result2 = self.program._get_error_message_add_page_time_amt('0')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
# --------
# Search Page
# --------

class TestIsResponseValidSearchPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('search_page')
        self.prompts = self.program.model_service.get_prompts()

    def test_return_false_if_response_is_empty(self):
        expected = False

        result1 = self.program._is_response_valid_search_page('', self.menu)
        result2 = self.program._is_response_valid_search_page('    ', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_false_if_response_is_other_than_letters(self):
        expected = False

        result1 = self.program._is_response_valid_main_page('*', self.menu)
        result2 = self.program._is_response_valid_main_page('1', self.menu)
        result3 = self.program._is_response_valid_main_page('ab cd', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_false_if_response_contains_more_than_one_character(self):
        expected = False

        result1 = self.program._is_response_valid_main_page('aa', self.menu)
        result2 = self.program._is_response_valid_main_page('abc', self.menu)
        result3 = self.program._is_response_valid_main_page('def', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_false_if_response_is_other_than_whats_assigned_to_menu(self):
        expected = False

        result1 = self.program._is_response_valid_main_page('z', self.menu)
        result2 = self.program._is_response_valid_main_page('f', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_true_if_response_is_correct(self):
        expected = True

        result1 = self.program._is_response_valid_main_page('a', self.menu)
        result2 = self.program._is_response_valid_main_page('e', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)


class TestGetErrorMessageSearchPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('search_page')

    def test_return_false_if_menu_has_no_items(self):
        expected = "Sorry. There are no items in menu. Please exit program (Ctrl + c) and try again."

        result = self.program._get_error_message_search_page('', [])

        self.assertEqual(expected, result)

    def test_return_error_message_if_response_is_empty(self):
        expected = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(self.menu) - 1))

        result1 = self.program._get_error_message_search_page('', self.menu)
        result2 = self.program._get_error_message_search_page('    ', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_error_message_if_response_is_other_than_letters(self):
        expected = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(self.menu) - 1))

        result1 = self.program._get_error_message_search_page('*', self.menu)
        result2 = self.program._get_error_message_search_page('1', self.menu)
        result3 = self.program._get_error_message_search_page('ab cd', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_error_message_if_response_contains_more_than_one_character(self):
        expected = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(self.menu) - 1))

        result1 = self.program._get_error_message_search_page('aa', self.menu)
        result2 = self.program._get_error_message_search_page('abc', self.menu)
        result3 = self.program._get_error_message_search_page('def', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_error_message_if_response_is_other_than_whats_assigned_to_menu(self):
        expected = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(self.menu) - 1))

        result1 = self.program._get_error_message_search_page('z', self.menu)
        result2 = self.program._get_error_message_search_page('f', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_empty_if_response_is_correct(self):
        expected = ''

        result1 = self.program._get_error_message_search_page('a', self.menu)
        result2 = self.program._get_error_message_search_page('e', self.menu)

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

# --------
# Search By Date Page
# --------

class TestIsResponseValidSearchByDatePageEmptyData(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('search_page')

    def test_return_false_if_response_is_empty(self):
        expected = False

        result1 = self.program._is_response_valid_search_by_date_page('', )
        result2 = self.program._is_response_valid_search_by_date_page('    ')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_false_if_response_not_a_date_and_not_single_character(self):
        expected = False

        result1 = self.program._is_response_valid_search_by_date_page('aaaa')
        result2 = self.program._is_response_valid_search_by_date_page('a a b')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_false_if_response_is_a_character_but_not_R_and_not_a_date(self):
        expected = False

        result1 = self.program._is_response_valid_search_by_date_page('a')
        result2 = self.program._is_response_valid_search_by_date_page('r')
        result3 = self.program._is_response_valid_search_by_date_page('*')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_false_if_response_is_a_date_but_not_in_a_correct_format(self):
        expected = False

        result1 = self.program._is_response_valid_search_by_date_page('02-23-2019')
        result2 = self.program._is_response_valid_search_by_date_page('2019-02-31')
        result3 = self.program._is_response_valid_search_by_date_page('2019-13-02')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_true_if_date_is_R_or_date_of_correct_format(self):
        expected = True

        result1 = self.program._is_response_valid_search_by_date_page('R')
        result2 = self.program._is_response_valid_search_by_date_page('2019-12-23')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)



class TestGetErrorMessageSearchByDatePage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('search_page')

    def test_return_error_message_if_data_is_empty(self):
        expected = 'Tnere are no data in database. Please return to main (R), and add an item.'

        result1 = self.program._get_error_message_search_by_date_page('', 'empty_data')
        result2 = self.program._get_error_message_search_by_date_page('hello', 'empty_data')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_error_message_if_response_not_a_date_and_not_single_character(self):
        expected = 'Please enter item in correct format (yyyy-mm-dd) or value (R)'

        result1 = self.program._get_error_message_search_by_date_page('aaaa')
        result2 = self.program._get_error_message_search_by_date_page('a a b')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_error_message_if_response_is_a_character_but_not_R_and_not_a_date(self):
        expected = 'Please enter item in correct format (yyyy-mm-dd) or value (R)'

        result1 = self.program._get_error_message_search_by_date_page('a')
        result2 = self.program._get_error_message_search_by_date_page('r')
        result3 = self.program._get_error_message_search_by_date_page('*')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_error_message_if_response_is_a_date_but_not_in_a_correct_format(self):
        expected = 'Please enter item in correct format (yyyy-mm-dd) or value (R)'

        result1 = self.program._get_error_message_search_by_date_page('02-23-2019')
        result2 = self.program._get_error_message_search_by_date_page('2019-02-31')
        result3 = self.program._get_error_message_search_by_date_page('2019-13-02')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_empty_response_if_response_is_R_or_of_correct_date(self):
        expected = ''

        result1 = self.program._get_error_message_search_by_date_page('R')
        result2 = self.program._get_error_message_search_by_date_page('2019-12-23')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
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