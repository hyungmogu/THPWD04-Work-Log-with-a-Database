import peewee as p
import datetime

db = p.SqliteDatabase('workLog.db')

class Entries(p.Model):
    date = DateTimeField(default=datetime.datetime.now)
    task_name = CharField(max_length=255, unique=False)
    time_amt = IntegerField(default=0)
    notes = TextField()

    # tells SQLite which database it belongs to
    class Meta:
        database = db
