import csv
import peewee as p
import datetime

from models import Entries

class ModelService:
    menu_main = ["Add Entry", "Search Existing Entry", "Quit"]
    menu_search_page = ["Find By Date", "Find by Time Spent", "Find by Exact Search", "Find by Pattern", "Return to Main"]

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

    def get_all_entries(self):
        items = Entries.select()
        return items

