import csv
import peewee as p

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
            print(prompt)
            entry[prompt['model']] = output[prompt['model']] if prompt['model'] in output else ''

        Entries.create(**entry)

    def get_entry(self):
        try:
            with open('work_log.csv','r') as csvFile:
                output = csvFile.read()
        except IOError:
            output = ''

        return output

    def get_all_entries(self):
        try:
            with open('work_log.csv','r') as csvFile:
                output = [ x.strip() for x in csvFile.readlines()]
        except IOError:
            output = []

        return output

