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
    done = fields.BooleanField(default=False, null=True)
    project = fields.ForeignKeyField('models.Project', on_delete=fields.CASCADE)
    date_of_receiving = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
