import datetime

import peewee as pw

from smartlogging.db import db


class Message(pw.Model):

    message = pw.CharField()
    created = pw.DateField(default=datetime.datetime.now())
    feed = pw.CharField()

    class Meta:
        database = db
        db_table = 'messages'
