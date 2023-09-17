from peewee import *
from config import db


class User(Model):
    user_id = IntegerField()
    user_role = TextField(default='cashier')
    username = TextField()

    class Meta:
        database = db


class Request(Model):
    user_id = IntegerField()
    text = TextField()
    image = TextField()
    status = IntegerField()
    branch = TextField()
    price = IntegerField()
    responsible = IntegerField()

    class Meta:
        database = db


class AppealRequest(Model):
    user_id = IntegerField()
    text = TextField()
    image = TextField()
    status = IntegerField()
    category = TextField()
    responsible = IntegerField()

    class Meta:
        database = db


class Branch(Model):
    name = TextField()

    class Meta:
        database = db


class Category(Model):
    name = TextField()
    responsible = TextField()

    class Meta:
        database = db


class Task(Model):
    user_id = IntegerField()
    text = TextField()
    date = DateTimeField()
    status = IntegerField(default=0)

    class Meta:
        database = db


class ChecklistTemplates(Model):
    name = TextField()
    is_close = BooleanField()
    photo = TextField()
    branch_id = ForeignKeyField(Branch)

    class Meta:
        database = db


class BranchesTasks(Model):
    checklist_id = ForeignKeyField(ChecklistTemplates)
    branch_id = ForeignKeyField(Branch)
    date = TextField()
    status = BooleanField(default=False)
    is_close = BooleanField()
    photo = TextField(default="")

    class Meta:
        database = db
