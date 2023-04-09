import requests
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .models import Dialogue, Message
from . import SUGGEST, EXPLAIN, SYSTEM_EXPLAIN, SYSTEM_REFLECT, SYSTEM_COFFEECHAT
from promptlayer import openai
import os
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def chat(d: Dialogue, prompt: Optional[str] = None) -> Dialogue:
    """
    Chat with GPT3.5 via Openai's ChatCompletion API.
    """
    if prompt:
        d.messages.append(Message(role="user", content=prompt))
    r = openai.ChatCompletion.create(**d.dict())
    d.messages.append(Message(role="assistant", content=r.choices[0].message.content))
    return d


@app.get("/explain")
def explain(context: str, s_text: str) -> Dialogue:
    """
    Explain the selected text in context.
    """
    # create a prompt out of the text and the highlighted text.
    context = context.replace(s_text, f"(({s_text}))")
    prompt = EXPLAIN.format(context=context, s_text=s_text)
    d = chat(Dialogue(messages=[Message(role="system", content=SYSTEM_EXPLAIN)]), prompt)
    return d


@app.get("/reflect")
def reflect() -> Dialogue:
    """
    Reflect on the selected text in context.
    """
    # create a prompt out of the text and the highlighted text.
    d = chat(Dialogue(messages=[Message(role="system", content=SYSTEM_REFLECT)]))
    return d


@app.get("/coffeechat")
def coffeechat() -> Dialogue:
    """
    Coffee Chat.
    """
    d = chat(Dialogue(messages=[Message(role="system", content=SYSTEM_COFFEECHAT)]))
    return d


@app.post("/log")
def log(context: str,
        s_text: str,
        d: Dialogue) -> dict:
    """
    Log the dialogue, context, selected text to a Notion Table.
    """
    page_id = os.environ['NOTION_VOCAB_LOG_PAGE_ID']
    toggle_text = f'{datetime.now()} - {s_text}'
    r = requests.patch(f'https://api.notion.com/v1/blocks/{page_id}/children',
                       headers={
                           'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}",
                           'Notion-Version': '2022-06-28'
                       },
                       json={
                           "children": [
                               {
                                   'toggle': {'color': 'default',
                                              'rich_text': [{'annotations': {'bold': False,
                                                                             'code': False,
                                                                             'color': 'default',
                                                                             'italic': False,
                                                                             'strikethrough': False,
                                                                             'underline': False},
                                                             'href': None,
                                                             'plain_text': toggle_text,
                                                             'text': {'content': toggle_text,
                                                                      'link': None},
                                                             'type': 'text'}]},
                                   'type': 'toggle',
                               }
                           ]
                       })
    toggle_id = r.json()['results'][0]['id']
    time.sleep(3.0)
    r = requests.patch(f'https://api.notion.com/v1/blocks/{toggle_id}/children',
                       headers={
                           'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}",
                           'Notion-Version': '2022-06-28'
                       },
                       json={
                           "children": [
                               {
                                   'object': 'block',
                                   'paragraph': {'color': 'default',
                                                 'rich_text': [{'annotations': {'bold': False,
                                                                                'code': False,
                                                                                'color': 'default',
                                                                                'italic': False,
                                                                                'strikethrough': False,
                                                                                'underline': False},
                                                                'plain_text': str(d),
                                                                'text': {'content': str(d)},
                                                                'type': 'text'}]},
                                   'type': 'paragraph'
                               }
                           ]
                       })
    r.raise_for_status()
    return r.json()


# --- deprecated API's --- #

@app.post("/suggest", deprecated=True)
def suggest(context: str,
            s_text: str,
            d: Dialogue) -> list[str]:
    """
    Suggest useful questions for the user.
    """
    prompt = SUGGEST.format(s_text=s_text)
    d = chat(prompt, d)
    suggestions = d.messages[-1].content.split('\n')
    return suggestions






