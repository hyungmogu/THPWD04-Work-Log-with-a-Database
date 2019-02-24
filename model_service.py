import csv

class ModelService:
    menu_main = ["Add Entry", "Search Existing Entry", "Quit"]
    menu_search_page = ["Find By Date", "Find by Time Spent", "Find by Exact Search", "Find by Pattern", "Return to Main"]

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
        with open("work_log.csv", "a" ) as csvFile:
            csvHeaders = ['date'] + [x['model'] for x in prompts]
            csvWriter = csv.DictWriter(csvFile, fieldnames=csvHeaders)

            if self._file_is_empty(csvFile):
                csvWriter.writeheader()
            csvWriter.writerow(output)

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

