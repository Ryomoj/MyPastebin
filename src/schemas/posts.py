from pydantic import BaseModel


class PostAddSchema(BaseModel):
    text: str

class PostSchema(PostAddSchema):
    id: int