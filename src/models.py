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
    estimated_days_to_complete = fields.IntField()
    actual_days_to_complete = fields.IntField(null=True)
    hours_spent = fields.IntField(null=True)
    employee_id = fields.IntField(null=True)
    project = fields.ForeignKeyField('models.Project', on_delete=fields.CASCADE)

    def __str__(self):
        return self.name
