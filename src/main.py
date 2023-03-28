import openai
from fastapi import FastAPI
from .models import Dialogue, Message
from .prompts import SUGGEST, EXPLAIN


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/chat")
def chat(prompt: str, d: Dialogue = None) -> Dialogue:
    """
    Chat via Openai's ChatCompletion API.
    refer to:
    https://platform.openai.com/docs/guides/chat/introduction
    """
    if d is None:
        d = Dialogue()
    d.messages.append(Message(role="user", content=prompt))
    r = openai.ChatCompletion.create(**d.dict(exclude={'context', 's_text'}))
    d.messages.append(Message(role="assistant", content=r.choices[0].message.content))
    return d


@app.post("/explain")
def explain(context: str, s_text: str) -> Dialogue:
    """
    Explain the selected text.
    """
    # create a prompt out of the text and the highlighted text.
    context = context.replace(s_text, f"(({s_text}))")
    prompt = EXPLAIN.format(context=context, s_text=s_text)
    d = Dialogue(context=context, s_text=s_text)
    d = chat(prompt, d)
    return d


@app.post("/suggest")
def suggest(d: Dialogue) -> list[str]:
    prompt = SUGGEST.format(s_text=d.s_text)
    d = chat(prompt, d)
    suggestions = d.messages[-1].content.split('\n')
    return suggestions


@app.post("/log")
def log(d: Dialogue, h_text: str) -> Dialogue:
    # log the dialogue to a database. For the time being, we will use a local database.
    # param d: a Dialogue object.
    # param h_text: the highlighted text to find vocabulary from.
    # return: a Dialogue object with the new vocabulary added.
    # get the vocabulary from the highlighted text
    # add the vocabulary to the dialogue
    return d

