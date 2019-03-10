import unittest
import peewee as p

from main import Program
from model_service import ModelService
from models import Entries

# --------
# Model Serivce
# --------


class TestGetAllEntries(unittest.TestCase):
    def setUp(self):
        # 1. delete pre-existing database if it exists
        self.db = p.SqliteDatabase('workLog.db')
        self.db.connect()
        self.db.drop_tables([Entries])

        # 2. register entries
        self.model_service = ModelService()

        prompts = self.model_service.prompts_add_page

        input1 = {'employee_name': 'Hello', 'time_amt': 20, 'notes': 'World'}
        input2 = {'employee_name': 'Hello2', 'time_amt': 30, 'notes': 'World2'}
        input3 = {'employee_name': 'Hello3', 'time_amt': 40, 'notes': 'World3'}

        self.model_service.add_entry(prompts, input1)
        self.model_service.add_entry(prompts, input2)
        self.model_service.add_entry(prompts, input3)

    def tearDown(self):
        self.db.drop_tables([Entries])
        self.db.close()

    def test_return_size_of_3_when_all_items_are_retrieved(self):
        expected = 3

        result = self.model_service.get_all_entries().count()

        self.assertEqual(expected, result)

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
class TestIsResponseValidAddPageEmployeeName(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('main')
        self.prompts = self.program.model_service.get_prompts()

    def test_return_false_if_response_is_empty(self):
        expected = False

        result1 = self.program._is_response_valid_add_page_employee_name('')
        result2 = self.program._is_response_valid_add_page_employee_name('   ')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_true_if_not_empty(self):
        expected = True

        result1 = self.program._is_response_valid_add_page_employee_name('hello')
        result2 = self.program._is_response_valid_add_page_employee_name('*')

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


class TestGetErrorMessageAddPageEmployeeName(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('main')
        self.prompts = self.program.model_service.get_prompts()

    def test_return_error_message_if_response_is_empty(self):
        expected = 'Please enter non-empty value'

        result1 = self.program._get_error_message_add_page_employee_name('')
        result2 = self.program._get_error_message_add_page_employee_name('     ')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_empty_if_otherwise(self):
        expected = ''

        result1 = self.program._get_error_message_add_page_employee_name('hello')
        result2 = self.program._get_error_message_add_page_employee_name('*')

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

class TestIsResponseValidSearchByDatePage(unittest.TestCase):
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
        expected = 'There are no data in database. Please return to main (R), and add an item.'

        result1 = self.program._get_error_message_search_by_date_page('', 'empty_data')
        result2 = self.program._get_error_message_search_by_date_page('hello', 'empty_data')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_error_message_if_response_not_a_date_and_not_single_character(self):
        expected = 'Please enter item in correct format (yyyy-mm-dd) or value (R)'

        result1 = self.program._get_error_message_search_by_date_page('aaaa','not_valid_response')
        result2 = self.program._get_error_message_search_by_date_page('a a b','not_valid_response')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_error_message_if_response_is_a_character_but_not_R_and_not_a_date(self):
        expected = 'Please enter item in correct format (yyyy-mm-dd) or value (R)'

        result1 = self.program._get_error_message_search_by_date_page('a','not_valid_response')
        result2 = self.program._get_error_message_search_by_date_page('r','not_valid_response')
        result3 = self.program._get_error_message_search_by_date_page('*','not_valid_response')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_error_message_if_response_is_a_date_but_not_in_a_correct_format(self):
        expected = 'Please enter item in correct format (yyyy-mm-dd) or value (R)'

        result = self.program._get_error_message_search_by_date_page('02-23-2019','not_valid_response')

        self.assertEqual(expected, result)

    def test_return_error_message_if_day_is_out_of_range(self):
        expected = 'Day is out of range for month'

        result = self.program._get_error_message_search_by_date_page('2019-02-31','not_valid_response')

        self.assertEqual(expected, result)

    def test_return_error_message_if_month_is_out_of_range(self):
        expected = 'Month must be in 1..12'

        result = self.program._get_error_message_search_by_date_page('2019-13-02','not_valid_response')

        self.assertEqual(expected, result)

    def test_return_empty_response_if_response_is_R_or_of_correct_date(self):
        expected = ''

        result1 = self.program._get_error_message_search_by_date_page('R','not_valid_response')
        result2 = self.program._get_error_message_search_by_date_page('2019-12-23','not_valid_response')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_error_message_if_response_is_of_correct_date_but_has_empty_data(self):
        expected = 'Retrieved result is empty.'

        result = self.program._get_error_message_search_by_date_page('2019-02-23','empty_results')

        self.assertEqual(expected, result)

# --------
# Search By Time Page
# --------

class TestIsResponseValidSearchByTimeSpentPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('search_page')

    def test_return_false_if_response_is_empty(self):
        expected = False

        result = self.program._is_response_valid_search_by_time_page('')

        self.assertEqual(expected, result)

    def test_return_false_if_response_is_not_integer(self):
        expected = False

        result1 = self.program._is_response_valid_search_by_time_page('false')
        result2 = self.program._is_response_valid_search_by_time_page('hello world')
        result3 = self.program._is_response_valid_search_by_time_page('20 12')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

    def test_return_false_if_response_is_not_non_negative_integer(self):
        expected = False

        result1 = self.program._is_response_valid_search_by_time_page('-10')
        result2 = self.program._is_response_valid_search_by_time_page('-100')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_true_if_response_is_zero_or_positive_integer(self):
        expected = True

        result1 = self.program._is_response_valid_search_by_time_page('10')
        result2 = self.program._is_response_valid_search_by_time_page('100')
        result3 = self.program._is_response_valid_search_by_time_page('0')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)

class TestGetErrorMessageSearchByTimeSpentPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('search_page')

    def test_return_error_message_if_data_is_empty(self):
        expected = 'There are no data in database. Please return to main (R), and add an item.'

        result = self.program._get_error_message_search_by_time_spent_page('empty_data')

        self.assertEqual(expected, result)

    def test_return_error_message_if_response_is_not_valid(self):
        expected = 'Please enter item in correct format (non-negative integer) or value (R)'

        result = self.program._get_error_message_search_by_time_spent_page('not_valid_response')

        self.assertEqual(expected, result)

    def test_return_error_message_if_empty_results_are_returned(self):
        expected = 'Retrieved result is empty.'

        result = self.program._get_error_message_search_by_time_spent_page('empty_results')

        self.assertEqual(expected, result)

# --------
# Search By Regex or Exact Words Page
# --------

class TestIsResponseValidSearchByRegexOrExactWordsPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
        self.menu = self.program.model_service.get_menu('search_page')

    def test_return_false_if_response_is_empty(self):
        expected = False

        result1 = self.program._is_response_valid_search_by_search_term_page('')
        result2 = self.program._is_response_valid_search_by_search_term_page('    ')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_true_if_response_not_empty(self):
        expected = True

        result1 = self.program._is_response_valid_search_by_search_term_page('hello')
        result2 = self.program._is_response_valid_search_by_search_term_page('*')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)


class TestGetErrorMessageSearchByRegexOrExactWordsPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()

    def test_return_error_message_if_data_is_empty(self):
        expected = 'There are no data in database. Please return to main (R), and add an item.'

        result = self.program._get_error_message_search_by_search_term_page('empty_data')

        self.assertEqual(expected, result)

    def test_return_error_message_if_response_is_not_valid(self):
        expected = 'Please enter non-empty characters or value (R)'

        result = self.program._get_error_message_search_by_search_term_page('not_valid_response')

        self.assertEqual(expected, result)

    def test_return_error_message_if_empty_results_are_returned(self):
        expected = 'Retrieved result is empty.'

        result = self.program._get_error_message_search_by_search_term_page('empty_results')

        self.assertEqual(expected, result)

# --------
# Display Page
# --------

class TestIsResponseValidDisplayPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()

    def test_return_false_if_response_is_empty(self):
        expected = False

        result1 = self.program._is_response_valid_display_page('', 'search_page')
        result2 = self.program._is_response_valid_display_page('    ', 'search_page')
        result3 = self.program._is_response_valid_display_page('', 'add_page')
        result4 = self.program._is_response_valid_display_page('    ', 'add_page')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)
        self.assertEqual(expected, result4)

    def test_return_false_if_incorrect_response_is_given_for_display_from_search_page(self):
        expected = False

        result1 = self.program._is_response_valid_display_page('*', 'search_page')
        result2 = self.program._is_response_valid_display_page('n', 'search_page')
        result3 = self.program._is_response_valid_display_page('p', 'search_page')
        result4 = self.program._is_response_valid_display_page('r', 'search_page')
        result5 = self.program._is_response_valid_display_page('hello world', 'search_page')
        result6 = self.program._is_response_valid_display_page('0', 'search_page')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)
        self.assertEqual(expected, result4)
        self.assertEqual(expected, result5)
        self.assertEqual(expected, result6)

    def test_return_false_if_incorrect_response_is_given_for_display_from_add_page(self):
        expected = False

        result1 = self.program._is_response_valid_display_page('*', 'add_page')
        result2 = self.program._is_response_valid_display_page('n', 'add_page')
        result3 = self.program._is_response_valid_display_page('p', 'add_page')
        result4 = self.program._is_response_valid_display_page('r', 'add_page')
        result5 = self.program._is_response_valid_display_page('hello world', 'add_page')
        result6 = self.program._is_response_valid_display_page('0', 'add_page')
        result7 = self.program._is_response_valid_display_page('N', 'add_page')
        result8 = self.program._is_response_valid_display_page('P', 'add_page')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)
        self.assertEqual(expected, result4)
        self.assertEqual(expected, result5)
        self.assertEqual(expected, result6)
        self.assertEqual(expected, result7)
        self.assertEqual(expected, result8)

    def test_return_true_if_correct_response_is_given(self):
        expected = True

        result1 = self.program._is_response_valid_display_page('N', 'search_page')
        result2 = self.program._is_response_valid_display_page('P', 'search_page')
        result3 = self.program._is_response_valid_display_page('R', 'search_page')
        result4 = self.program._is_response_valid_display_page('R', 'add_page')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)
        self.assertEqual(expected, result4)


class TestGetErrorMessageDisplayPage(unittest.TestCase):
    def setUp(self):
        self.program = Program()
    def test_return_error_message_if_response_is_empty_for_display_from_add_page(self):
        expected = "Please choose correct value(s) (R)"

        result = self.program._get_error_message_display_page('', 'add_page')

        self.assertEqual(expected, result)

    def test_return_error_message_if_response_is_empty_for_display_from_search_page(self):
        expected = "Please choose correct value(s) (N,P,R)"

        result = self.program._get_error_message_display_page('', 'search_page')

        self.assertEqual(expected, result)

    def test_return_error_message_if_incorrect_response_is_given_for_display_from_add_page(self):
        expected = "Please choose correct value(s) (R)"

        result1 = self.program._get_error_message_display_page('*', 'add_page')
        result2 = self.program._get_error_message_display_page('n', 'add_page')
        result3 = self.program._get_error_message_display_page('p', 'add_page')
        result4 = self.program._get_error_message_display_page('r', 'add_page')
        result5 = self.program._get_error_message_display_page('hello world', 'add_page')
        result6 = self.program._get_error_message_display_page('0', 'add_page')
        result7 = self.program._get_error_message_display_page('N', 'add_page')
        result8 = self.program._get_error_message_display_page('P', 'add_page')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)
        self.assertEqual(expected, result4)
        self.assertEqual(expected, result5)
        self.assertEqual(expected, result6)
        self.assertEqual(expected, result7)
        self.assertEqual(expected, result8)

    def test_return_error_message_if_incorrect_response_is_given_for_display_from_search_page(self):
        expected = "Please choose correct value(s) (N,P,R)"

        result1 = self.program._get_error_message_display_page('*', 'search_page')
        result2 = self.program._get_error_message_display_page('n', 'search_page')
        result3 = self.program._get_error_message_display_page('p', 'search_page')
        result4 = self.program._get_error_message_display_page('r', 'search_page')
        result5 = self.program._get_error_message_display_page('hello world', 'search_page')
        result6 = self.program._get_error_message_display_page('0', 'search_page')

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)
        self.assertEqual(expected, result3)
        self.assertEqual(expected, result4)
        self.assertEqual(expected, result5)
        self.assertEqual(expected, result6)

if __name__ == '__main__':
    unittest.main()