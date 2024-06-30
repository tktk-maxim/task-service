from tortoise.models import Model
from tortoise import fields


class Project(Model):
    name = fields.CharField(max_length=255)
    description = fields.TextField()

    def __str__(self):
        return self.name


class Task(Model):
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    time_complete_in_days = fields.IntField(null=True)
    project = fields.ForeignKeyField('models.Project', on_delete=fields.CASCADE)

    def __str__(self):
        return self.name
