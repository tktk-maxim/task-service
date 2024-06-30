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
    time_complete_in_days: int | None = Field(default=None, null=True)
    project_id: int

    @field_validator('name', 'description')
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError('Field cannot be empty')
        return value


class TaskIn(TaskCreate):
    id: int
