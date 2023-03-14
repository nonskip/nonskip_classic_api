from pydantic import BaseModel


class Word(BaseModel):
    lemma: str
    definition: str
    url: str

