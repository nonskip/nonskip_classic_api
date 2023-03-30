from pydantic import BaseModel, validator
from . import SYSTEM


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


class Dialogue(BaseModel):
    """
    To be used with the official ChatGPT api.
    refer to:
    # https://platform.openai.com/docs/guides/chat/introduction
    """
    model: str = "gpt-3.5-turbo"
    messages: list[Message] = [
        Message(role="system", content=SYSTEM)
    ]

    @classmethod
    @validator('model', allow_reuse=True)
    def model_must_be_gpt_3_5_turbo(cls, v):
        if v != 'gpt-3.5-turbo':
            raise ValueError('model must be gpt-3.5-turbo, but was ' + v)
        return v

    def __str__(self) -> str:
        return "\n".join([str(m) for m in self.messages])


