class ViewService:
    def __init__(self):
        self.error_message = ''
        self.page_title = ''

    def _get_header(self):
        print("Work Log ({})\n".format(self.page_title))

    def _get_error_message(self):
        if self.error_message:
            print("Error: {}".format(self.error_message))
            print("Please try again:\n")

    def clear_error_message(self):
        self.error_message = ''

    def get_menu_page(self, menu_items, page_type):
        self._get_header()

        if page_type == 'main':
            print("Please select an item from menu\n")
        elif page_type == 'search_page':
            print("Please select one of the following options\n")

        for index, item in enumerate(menu_items):
            if index != len(menu_items) - 1:
                print("{0}. {1}".format(chr(index+97), item))
            else:
                print("{0}. {1}\n".format(chr(index+97), item))

        self._get_error_message()

    def get_add_page(self, prompt_phrase):
        self._get_header()

        print("Please enter value to the following\n")

        print("{}:\n".format(prompt_phrase))

        self._get_error_message()

    def _get_title_search_by_page(self, search_type):
        output = ''

        if search_type == 'date':
            output = "Please enter full date (yyyy-MM-dd):\n"
        elif search_type == 'task_name':
            output = "Please enter name of task:\n"
        elif search_type == 'time_spent':
            output = "Please enter amount of time (Non-negative integer):\n"
        elif search_type == 'employee_name':
            output = "Please enter employee name:\n"
        elif search_type == 'task_name_and_notes':
            output = "Please enter search term:\n"

        return output

    def get_search_by_page(self, search_type):
        self._get_header()

        title = self._get_title_search_by_page(search_type)

        print(title)

        print("[R] Return to Search Page\n")

        self._get_error_message()

    def _get_options_display_page(self, path, items, index):
        output = ''

        if path == 'search_page':
            if len(items) == 1:
                output = "[R] Return to Search Page\n"
            elif index == 0:
                output = "[N] Next Item [R] Return to Search Page\n"
            elif index > 0 and index < len(items) - 1:
                output = (
                    "[N] Next Item [P] Previous Item [R] Return to "
                    "Search Page\n")
            else:
                output = "[P] Previous Item [R] Return to Search Page\n"
        else:
            output = "[R] Return to Main Page\n"

        return output

    def get_display_page(self, path, items, index):
        self._get_header()
        item = items[index]

        print("Employee Name: {}".format(item.employee_name))
        print("Task Name: {}".format(item.task_name))
        print("Created Date: {}".format(item.date.strftime('%Y-%m-%d')))
        print("Time Spent: {}".format(item.time_amt))
        print("Notes: {}\n".format(item.notes))

        title_submenu = self._get_options_display_page(path, items, index)

        if path == 'search_page':
            print("Displaying Item ({} of {})\n".format(index+1, len(items)))

        print(title_submenu)

        self._get_error_message()

