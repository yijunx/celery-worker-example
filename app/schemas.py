from pydantic import BaseModel


class JobCreate(BaseModel):
    name: str


class JobUpdate(BaseModel):
    finished_rows: int


class Job(JobCreate):
    id: str
    size: str
    rows: int
    finished_rows: int
    done: bool

    class Config:
        orm_mode = True
