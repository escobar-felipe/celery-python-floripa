from pydantic import BaseModel


class AddRequest(BaseModel):
    x: int
    y: int
