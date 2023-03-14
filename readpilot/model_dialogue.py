from pydantic import BaseModel, validator
from .model_message import Message
import datetime


class Dialogue(BaseModel):
    # https://platform.openai.com/docs/guides/chat/introduction
    model: str = "gpt-3.5-turbo"
    messages: list[Message] = [
        Message(role="system", content=f"You are ChatGPT, a large language model trained by OpenAI."
                                       " Answer as concisely as possible."
                                       f" Current date: {datetime.datetime.today()}")
    ]

    @classmethod
    @validator('model')
    def model_must_be_gpt_3_5_turbo(cls, v):
        if v != 'gpt-3.5-turbo':
            raise ValueError('model must be gpt-3.5-turbo, but was ' + v)
        return v

    def __str__(self) -> str:
        return "\n".join([str(m) for m in self.messages])
