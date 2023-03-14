from pydantic import BaseModel, validator


class Message(BaseModel):
    role: str
    content: str

    @classmethod
    @validator('role', allow_reuse=True)
    def role_must_be_either_system_assistant_user(cls, v):
        if v not in ('system', 'assistant', 'user'):
            raise ValueError('role must be either system / assistant / user, but was ' + v)
        return v

    def __str__(self) -> str:
        return f"{self.role}: {self.content}"
