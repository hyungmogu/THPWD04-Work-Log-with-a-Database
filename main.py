import os
import re
import sys
import datetime

from model_service import ModelService
from view_service import ViewService


class Program:  # this is controller (from MVC architecture.)
    def __init__(self, model_service=ModelService, view_service=ViewService):
        self.quit_program = False

        self.view_service = ViewService()
        self.model_service = ModelService()

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _quit(self):
        print("Thank You and Take Care")
        self.quit_program = True

    def _get_all_entries(self):
        return self.model_service.get_all_entries()

    def _get_response(self):
        response = ''

        if sys.version_info < (3, 0):
            response = raw_input("> ").strip()
        else:
            response = input("> ").strip()

        return response

    def _get_err_msg_main_page(self, response, menu):
        error_message = ''
        # 1. if menu is empty, then set menu is empty error
        if len(menu) == 0:
            error_message = (
                "Sorry. There are no items in menu. Please exit "
                "program (Ctrl + c) and try again.")

        # 2. if menu has value other than what's available, set value error
        elif (not len(response) == 1 or
                not (ord(response) >= 97 and ord(response) < 97 + len(menu))):
            error_message = (
                "Please enter correct value ({}-{})"
                .format(chr(97), chr(97 + len(menu) - 1)))

        return error_message

    def _is_res_valid_main_page(self, response, menu):
        # 1. if response contains characters other than letters, return false
        if len(re.findall(r"[^a-zA-Z]", response)) > 0:
            return False

        # 2. if response contains characters of length greater than 1, then
        # return false
        if len(response) > 1 or len(response) == 0:
            return False

        # 3. if response contains character of value less than ASCII value of
        # 97 and greater than or equal to 97 + len(main_items), then return
        # false
        if ord(response) < 97 or ord(response) >= 97 + len(menu):
            return False

        # 4. otherwise, return true
        return True

    def _is_res_valid_search_page(self, response, menu):
        # 1. if response contains characters other than letters, return false
        if len(re.findall(r"[^a-zA-Z]", response)) > 0:
            return False

        # 2. if response contains characters of length greater than 1 or 0,
        # then return false
        if len(response) > 1 or len(response) == 0:
            return False

        # 3. otherwise, return true
        return True

    def _get_err_msg_search_page(self, response, menu):
        error_message = ''

        # 1. if menu is empty, then set menu is empty error
        if len(menu) == 0:
            error_message = (
                "Sorry. There are no items in menu. Please exit "
                "program (Ctrl + c) and try again.")

        # 2 if response is empty, then return message saying to add a correct
        # value
        elif response.strip() == '':
            error_message = (
                "Please enter correct value ({}-{})"
                .format(chr(97), chr(97 + len(menu) - 1)))
        # 3. if menu has value other than what's available, set value error
        elif (not len(response) == 1 or
                not (ord(response) >= 97 and ord(response) < 97 + len(menu))):
            error_message = (
                "Please enter correct value ({}-{})"
                .format(chr(97), chr(97 + len(menu) - 1)))

        return error_message

    def _get_page_title(self, page_type):
        output = ''

        if page_type == 'main':
            output = 'Main Page'
        elif page_type == 'search_page':
            output = 'Search Page'

        return output

    def run_menu_page(self, page_type):
        self.view_service.page_title = self._get_page_title(page_type)
        menu = self.model_service.get_menu(page_type)
        exit_page = False

        while not exit_page:
            self._clear_screen()

            self.view_service.get_menu_page(menu, page_type)

            response = self._get_response()

            if (page_type == 'main' and
                    not self._is_res_valid_main_page(response, menu)):
                self.view_service.error_message = (
                    self._get_err_msg_main_page(response, menu))
                continue
            elif (page_type == 'search_page' and
                    not self._is_res_valid_search_page(response, menu)):
                self.view_service.error_message = (
                    self._get_err_msg_search_page(response, menu))
                continue

            exit_page = True

        self.view_service.clear_error_message()

        if page_type == 'main':
            if response == 'a':
                self.run_add_page()
            elif response == 'b':
                self.run_menu_page('search_page')
            else:
                self._clear_screen()
                self._quit()

        elif page_type == 'search_page':
            if response == 'a':
                self.run_search_by_page('employee_name')
            elif response == 'b':
                self.run_search_by_page('date')
            elif response == 'c':
                self.run_search_by_page('time_spent')
            elif response == 'd':
                self.run_search_by_page('task_name_and_notes')
            elif response == 'e':
                self._clear_screen()
                self.run_menu_page('main')
            else:
                self.run_menu_page(page_type)

    def _is_res_valid_add_page_names(self, response):
        # 1. Return false if response is empty
        if response.strip() == '':
            return False

        return True

    def _is_res_valid_add_page_time_amt(self, response):

        # 1. Return false if response is empty
        if response.strip() == '':
            return False

        # 2. return false if response is non-empty but has numbers
        if re.search(r'[^0-9]', response) is not None:
            return False

        return True

    def _get_err_msg_add_page_names(self, response):
        output = ''

        if response.strip() == '':
            output = 'Please enter non-empty value'

        return output

    def _get_err_msg_add_page_time_amt(self, response):
        output = ''

        if response.strip() == '':
            output = 'Please enter non-negative integer value'
        elif re.search(r'[^0-9]', response) is not None:
            output = 'Please enter non-negative integer value'

        return output

    def run_add_page(self):
        self.view_service.page_title = 'Add Entry Page'
        prompts = self.model_service.get_prompts()
        output = {}

        # 1. Walk through each prompt and store value in output
        for prompt in prompts:
            correct = False
            while not correct:
                self._clear_screen()
                self.view_service.get_add_page(prompt['label'])

                res = self._get_response()

                if ((prompt['model'] == 'employee_name' or
                    prompt['model'] == 'task_name') and
                        not self._is_res_valid_add_page_names(res)):
                    self.view_service.error_message = (
                        self._get_err_msg_add_page_names(res))
                    continue
                elif (prompt['model'] == 'time_amt' and
                        not self._is_res_valid_add_page_time_amt(res)):
                    self.view_service.error_message = (
                            self._get_err_msg_add_page_time_amt(res))
                    continue

                output[prompt['model']] = res
                correct = True

            self.view_service.clear_error_message()

        # 2. Store / append output in csv
        item = self.model_service.add_entry(prompts, output)

        self.run_display_page('add_page', [item])

    def _get_err_msg_search_by_date_page(self, response, message_type):
        output = ''

        if message_type == 'empty_data':
            output = (
                "There are no data in database. Please return to main (R)"
                ", and add an item.")

        elif message_type == 'not_valid':
            # 1. check if correct format has been registered
            if not response or len(response) == 0:
                output = (
                    "Please enter item in correct format (yyyy-mm-dd) or "
                    "value (R)")
            elif response and len(response) == 1:
                if response.strip() != 'R':
                    output = (
                        "Please enter item in correct format (yyyy-mm-dd) or "
                        "value (R)")
                else:
                    output = ''
            elif (response and
                  re.match(r'\d{4}\-\d{2}\-\d{2}', response.strip()) is not
                  None):

                year, month, day = response.split('-')
                try:
                    datetime.datetime(int(year), int(month), int(day))
                except ValueError as e:
                    output = str(e).capitalize()

            else:
                output = (
                    "Please enter item in correct format (yyyy-mm-dd) or "
                    "value (R)")

        elif message_type == 'empty_results':
            output = 'Retrieved result is empty.'

        return output

    def _is_res_valid_search_by_date_page(self, response):
        # 1. ck if response is non-empty
        if not response or len(response) == 0:
            return False

        # 2. if response is a single letter, then check to see if it has
        # entered correct value corresponding menu
        if len(response) == 1:
            if response != 'R':
                return False
            return True
        # 3. if response is in date format, then check to see if it has a
        # correct value
        elif re.match(r'\d{4}\-\d{2}\-\d{2}', response) is not None:
            year, month, day = response.split('-')
            try:
                datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                return False

            return True
        # 4. for other cases, return False
        else:
            return False

    def run_search_by_page(self, search_type):
        self.view_service.page_title = 'Search Page'
        exit_page = False
        items = []

        if (search_type == 'date' and
                len(self.model_service.get_all_entries()) == 0):
            self.view_service.error_message = (
                self._get_err_msg_search_by_date_page('', 'empty_data'))
        elif (search_type == 'time_spent' and
                len(self.model_service.get_all_entries()) == 0):
            self.view_service.error_message = (
                self._get_err_msg_search_by_time_spent_page('empty_data'))
        elif ((search_type == 'employee_name' or
               search_type == 'task_name_and_notes') and
                len(self.model_service.get_all_entries()) == 0):
            self.view_service.error_message = (
                self._get_err_msg_search_by_search_term_page('empty_data'))

        while not exit_page:
            # 1. Clear screen
            self._clear_screen()

            # 2. Load page
            self.view_service.get_search_by_page(search_type)

            # 3. Load prompt
            res = self._get_response()

            # 4. if data not empty and response typed, check and see if typed
            # value is correct
            if (search_type == 'date' and
                    not self._is_res_valid_search_by_date_page(res)):
                self.view_service.error_message = (
                    self._get_err_msg_search_by_date_page(res, 'not_valid'))
                continue
            elif (search_type == 'date' and
                    not self._is_res_valid_search_by_search_term_page(res)):
                self.view_service.error_message = (
                    self._get_err_msg_search_by_search_term_page('not_valid'))
                continue
            elif (search_type == 'time_spent' and
                    not self._is_res_valid_search_by_time_page(res)):
                self.view_service.error_message = (
                    self._get_err_msg_search_by_time_spent_page('not_valid'))
                continue
            elif ((search_type == 'employee_name' or
                    search_type == 'task_name_and_notes') and
                    not self._is_res_valid_search_by_search_term_page(res)):
                self.view_service.error_message = (
                    self._get_err_msg_search_by_search_term_page('not_valid'))
                continue

            # 5. if response is 'R', then return to search page
            if res == 'R':
                exit_page = True
                continue

            # 6. If data is empty, then raise error saying data is empty, so
            # try again once it has been added
            if len(self.model_service.get_all_entries()) == 0:
                self.view_service.error_message = (
                    "There are no data in database. Please return to main "
                    "(R), and add an item.")
                continue

            # 7. Grab all results by search term in either by employee name or
            # both employee name and notes
            if search_type == 'date':
                items = self.model_service.get_entries_by_date(res)
            elif search_type == 'time_spent':
                items = self.model_service.get_entries_by_time_amt(res)
            elif (search_type == 'employee_name' or
                  search_type == 'task_name_and_notes'):
                items = (
                    self.model_service.
                    get_entries_by_search_term(res, search_type))

            # 8. Once grabbed, check and see if it has length equal to zero.
            # If so, then raise error saying nothing found
            if items.count() == 0:
                self.view_service.error_message = 'Retrieved result is empty.'
                continue

            exit_page = True

        self.view_service.clear_error_message()

        # 8. bring data to display page
        if res == 'R':
            self.run_menu_page('search_page')
        else:
            self.run_display_page('search_page', items)

    def _is_res_valid_search_by_time_page(self, response):
        output = False

        # 1. check if response is non-empty
        if not response or len(response) == 0:
            return output

        # 2. if response is a single letter, then check to see if it has
        # entered correct value corresponding menu
        if len(response) > 0 and re.match(r'[^\-0-9]', response) is not None:

            output = True if response.strip() == 'R' else False

            return output

        # 3. if response is in time spent, then check to see if it has a
        # correct value
        if len(response) > 0 and re.match(r'[^\-0-9]', response) is None:
            try:
                tempVal = int(response)
            except ValueError:
                return output

            output = True if tempVal >= 0 else False

            return output

        # 4. for other cases, return False
        return output

    def _get_err_msg_search_by_time_spent_page(self, message_type):
        output = ''

        if message_type == 'empty_data':
            output = (
                "There are no data in database. Please return to main (R), "
                "and add an item.")

        if message_type == 'not_valid':
            output = (
                "Please enter item in correct format (non-negative "
                "integer) or value (R)")

        if message_type == 'empty_results':
            output = 'Retrieved result is empty.'

        return output

    def _is_res_valid_search_by_search_term_page(self, response):
        if response.strip() == '':
            return False
        return True

    def _get_err_msg_search_by_search_term_page(self, error_type):
        if error_type == 'empty_data':
            output = (
                "There are no data in database. Please return to main "
                "(R), and add an item.")

        if error_type == 'not_valid':
            output = 'Please enter non-empty characters or value (R)'

        if error_type == 'empty_results':
            output = 'Retrieved result is empty.'

        return output

    def _is_res_valid_display_page(self, response, path):
        if path == 'search_page':
            choices = ['N', 'P', 'R']
        else:
            choices = ['R']

        # if the response is empty, warn user to type the correct value
        if response not in choices:
            return False
        return True

    def _get_err_msg_display_page(self, response, path):
        if path == 'search_page':
            choices = ['N', 'P', 'R']
        else:
            choices = ['R']

        # if the response is empty, warn user to type the correct value
        if response not in choices:
            return (
                "Please choose correct value(s) ({})"
                .format(",".join(choices)))

    def run_display_page(self, path, items):
        exit_page = False
        self.view_service.page_title = 'Display Page'
        index = 0

        while not exit_page:
            # while quit page is not registered, allow users to navigate
            # through items
            self._clear_screen()

            self.view_service.get_display_page(path, items, index)

            response = self._get_response()

            if not self._is_res_valid_display_page(response, path):
                self.view_service.error_message = (
                    self._get_err_msg_display_page(response, path))
                continue

            if response == 'N':
                if len(items) == 0 or index == len(items) - 1:
                    continue
                else:
                    index = index + 1 if (index+1) < len(items) else index
            elif response == 'P':
                if len(items) == 0 or index == 0:
                    continue
                else:
                    index = index - 1 if (index - 1) >= 0 else index
            elif response == 'R':
                exit_page = True

        self.view_service.clear_error_message()

        if response == 'R':
            self._clear_screen()
            if path == 'search_page':
                self.run_menu_page('search_page')
            else:
                self.run_menu_page('main')

if __name__ == "__main__":
    program = Program()
    program.run_menu_page('main')