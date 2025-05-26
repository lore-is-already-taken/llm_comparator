from pydantic import BaseModel


class QuestionImage(BaseModel):
    size: int
    hash: str
    name: str
    content_type: str
    uri: str = ""
