from pydantic import BaseModel, Field, field_validator


class ProjectCreate(BaseModel):
    name: str
    description: str

    @field_validator('name', 'description')
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError('Field cannot be empty')
        return value


class ProjectIn(ProjectCreate):
    id: int


class TaskCreate(BaseModel):
    name: str
    description: str
    estimated_days_to_complete: int
    actual_days_to_complete: int | None = Field(default=None, null=True)
    hours_spent: int | None = Field(default=0, null=True)
    employee_id: int | None = Field(default=None, null=True)
    done: bool | None = Field(default=False, null=True)
    project_id: int

    @field_validator('name', 'description')
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError('Field cannot be empty')
        return value


class TaskIn(TaskCreate):
    id: int


class TaskUpdateEmployeeId(BaseModel):
    employee_id: int


class TaskFilter(BaseModel):
    more_days_to_complete: int | None = Field(default=None, null=True)
    less_days_to_complete: int | None = Field(default=None, null=True)
    done: bool | None = Field(default=None, null=True)
    project_id: int | None = Field(default=None, null=True)


class TaskSort(BaseModel):
    name: bool | None = Field(default=None, null=True)
    description: bool | None = Field(default=None, null=True)
    estimated_days_to_complete: bool | None = Field(default=None, null=True)
    actual_days_to_complete: bool | None = Field(default=None, null=True)
    hours_spent: bool | None = Field(default=None, null=True)
    employee_id: bool | None = Field(default=None, null=True)
    done: bool | None = Field(default=None, null=True)
    project_id: bool | None = Field(default=None, null=True)
