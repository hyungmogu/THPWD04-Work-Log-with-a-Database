import csv
import peewee as p
import datetime
import re

from models import Entries


class ModelService:
    menu_main = ["Add Entry", "Search Existing Entry", "Quit"]

    menu_search_page = [
        "Find by Employee Name", "Find By Date", "Find by Time Spent",
        "Find by Search Term", "Return to Main"]

    prompts_add_page = [
        {'label': "Employee Name", 'model': 'employee_name'},
        {'label': "# of Minutes", 'model': 'time_amt'},
        {'label': "Additional Notes", 'model': 'notes'}]

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
            if prompt['model'] in output:
                entry[prompt['model']] = output[prompt['model']]
            else:
                entry[prompt['model']] = ''

        item = Entries.create(**entry)

        return item

    def get_entries_by_date(self, date):
        # grab all dates of that date
        target_date_lb = datetime.datetime.strptime(date, '%Y-%m-%d')
        target_date_ub = target_date_lb + datetime.timedelta(days=1)
        query_cond = (
            Entries.date >= target_date_lb and
            Entries.date < target_date_ub)

        items = Entries.select().where(query_cond)

        return items

    def get_entries_by_time_amt(self, time_amt):
        items = Entries.select().where(Entries.time_amt == int(time_amt))
        return items

    def get_entries_by_search_term(self, words, search_type):
        if search_type == 'employee_name':
            query_cond = Entries.employee_name.contains(words)
            items = Entries.select().where(query_cond)
        else:
            query_cond1 = Entries.employee_name.contains(words)
            query_cond2 = Entries.notes.contains(words)

            items_1 = Entries.select().where(query_cond1)
            items_2 = Entries.select().where(query_cond2)
            items = items_1 + items_2

        return items

    def get_all_entries(self):
        items = Entries.select()
        return items

