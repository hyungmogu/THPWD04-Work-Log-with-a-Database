import csv
import peewee as p
import datetime
import re

from models import Entries

class ModelService:
    menu_main = ["Add Entry", "Search Existing Entry", "Quit"]
    menu_search_page = ["Find by Employee Name","Find By Date", "Find by Time Spent", "Find by Search Term", "Return to Main"]

    prompts_add_page = [{'label': "Employee Name", 'model': 'employee_name'}, {'label': "# of Minutes", 'model': 'time_amt'}, {'label':"Additional Notes", 'model': 'notes'}]

    def __init__(self, Entries=Entries):
        self.db = p.SqliteDatabase('workLog.db')
        self.db.connect()
        self.db.create_tables([Entries], safe=True)

    def __delete__(self):
        self.db.close()

    def get_menu(self, name):
        output = []

        if hasattr(self, 'menu_{}'.format(name)):
            output = getattr(self, 'menu_{}'.format(name))

        return output

    def get_prompts(self):
        return self.prompts_add_page

    def _file_is_empty(self, file):
        if file.tell() == 0:
            return True
        return False

    def add_entry(self, prompts, output):
        entry = {}

        for prompt in prompts:
            entry[prompt['model']] = output[prompt['model']] if prompt['model'] in output else ''

        item = Entries.create(**entry)

        return item


    def get_entries_by_date(self, date):
        # grab all dates of that date
        target_date_lb = datetime.datetime.strptime(date, '%Y-%m-%d')
        target_date_ub = target_date_lb + datetime.timedelta(days=1)
        items = Entries.select().where(Entries.date >= target_date_lb and Entries.date < target_date_ub)

        return items

    def get_entries_by_time_amt(self, time_amt):
        items = Entries.select().where(Entries.time_amt == int(time_amt))
        return items

    def get_entries_by_regex(self, regex):
        output = []

        items = Entries.select()

        if len(items) == 0:
            return output

        for item in items:
            result_1 = re.search(r'{}'.format(regex), item.notes)
            result_2 = re.search(r'{}'.format(regex), item.employee_name)

            if result_1:
                output.append(item)

            if result_2:
                output.append(item)

        return output

    def get_entries_by_search_term(self, words):
        items_1 = Entries.select().where(Entries.employee_name.contains(words))
        items_2 = Entries.select().where(Entries.notes.contains(words))
        items = items_1 + items_2

        return items

    def get_all_entries(self):
        items = Entries.select()
        return items

