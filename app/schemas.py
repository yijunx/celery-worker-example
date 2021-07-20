from pydantic import BaseModel


class Job(BaseModel):
    id: str
    name: str
    size: str
    rows: int
    finished_rows: int
    done: bool

    class Config:
        orm_mode = True