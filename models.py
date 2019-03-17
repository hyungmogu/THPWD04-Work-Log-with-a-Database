import peewee as p
import datetime

db = p.SqliteDatabase('workLog.db')


class Entries(p.Model):
    date = p.DateTimeField(default=datetime.datetime.now)
    employee_name = p.CharField(max_length=255, unique=False)
    task_name = p.CharField(max_length=255, unique=False)
    time_amt = p.IntegerField(default=0)
    notes = p.TextField()

    # tells SQLite which database it belongs to
    class Meta:
        database = db
