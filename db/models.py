from config import DATABASE_URI
from peewee import SqliteDatabase, Model
from peewee import CharField, DateTimeField
import datetime

master_db = SqliteDatabase(DATABASE_URI)


class BaseModel(Model):
    """
    BaseModel to extend for all other models.
    """
    class Meta:
        database = master_db


class Video(BaseModel):
    id = CharField(unique=True, null=False, primary_key=True)
    channel_id = CharField(null=False)
    title = CharField(null=False)
    description = CharField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    published_at = DateTimeField(null=False, index=True)


class RunnerMeta(BaseModel):
    id = CharField(unique=True, primary_key=True)
    last_run = DateTimeField(default=datetime.datetime.now)


def init():
    """
    Initialize the database connection
    """
    master_db.connect()
    with master_db:
        master_db.create_tables([Video, RunnerMeta])

