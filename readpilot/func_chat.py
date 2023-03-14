from .model_dialogue import Dialogue
from .model_message import Message
import openai


def chat(prompt: str, d: Dialogue = None) -> Dialogue:
    """
    uses openAI API to chat with ChatGPT.
    refer to:
    https://platform.openai.com/docs/guides/chat/introduction
    :param d: a Dialogue object.
    :param prompt: the prompt to be used for the chat.
    :return: a Dialogue object.
    """
    if d is None:
        d = Dialogue()
    d.messages.append(Message(role="user", content=prompt))
    r = openai.ChatCompletion.create(**d.dict())
    d.messages.append(Message(role="assistant", content=r.choices[0].message.content))
    return d
