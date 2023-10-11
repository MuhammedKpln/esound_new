from peewee import (AutoField, CharField, DateTimeField, IntegerField, Model,
                    SqliteDatabase)

db = SqliteDatabase(None)


class Song(Model):

    id = AutoField()
    esound_song_id = IntegerField(index=True, unique=True)
    song_title = CharField()
    created_at = DateTimeField()

    class Meta:
        database = db


class User(Model):
    id = AutoField()
    email = CharField(index=True, unique=True)
    password = CharField()
    access_token = CharField()

    class Meta:
        database = db


def initialize_database():
    db.init('data.db')
    db.connect(reuse_if_open=True)
    db.create_tables([Song, User])
