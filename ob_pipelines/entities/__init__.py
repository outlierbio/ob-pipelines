from mongoengine import Document, StringField, DateTimeField, DictField, UUIDField
from mongoengine.fields import ReferenceField


class Experiment(Document):
    user_id = StringField(required=True)


class Job(Document):
    experiment = ReferenceField(Experiment, required=True)
    params = DictField(required=True)


class Task(Document):
    job = ReferenceField(Job, required=True)
    name = StringField(required=True)
    started_at = DateTimeField(null=True)
    completed_at = DateTimeField(null=True)
    exception = StringField()