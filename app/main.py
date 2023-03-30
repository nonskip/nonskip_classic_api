from datetime import datetime
import requests
from fastapi import FastAPI
from .models import Dialogue, Message
from . import SUGGEST, EXPLAIN
from promptlayer import openai
import os

app = FastAPI()


@app.post("/chat")
def chat(prompt: str,
         d: Dialogue = None) -> Dialogue:
    """
    Chat with GPT3.5 via Openai's ChatCompletion API.
    """
    if d is None:
        d = Dialogue()
    d.messages.append(Message(role="user", content=prompt))
    r = openai.ChatCompletion.create(**d.dict())
    d.messages.append(Message(role="assistant", content=r.choices[0].message.content))
    return d


@app.post("/explain")
def explain(context: str,
            s_text: str) -> Dialogue:
    """
    Explain the selected text in context.
    """
    # create a prompt out of the text and the highlighted text.
    context = context.replace(s_text, f"(({s_text}))")
    prompt = EXPLAIN.format(context=context, s_text=s_text)
    d = chat(prompt, Dialogue())
    return d


@app.post("/suggest")
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
                                                                'href': None,
                                                                'plain_text': str(d),
                                                                'text': {'content': str(d),
                                                                         'link': None},
                                                                'type': 'text'}]},
                                   'type': 'paragraph'
                               }
                           ]
                       })
    r.raise_for_status()
    return r.json()







