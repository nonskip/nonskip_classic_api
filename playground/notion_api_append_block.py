"""
appends a block to a page
https://developers.notion.com/reference/patch-block-children
"""
import requests
import os
from pprint import pprint
from datetime import datetime

page_id = os.environ['NOTION_VOCAB_LOG_PAGE_ID']

toggle_text = f'{datetime.now()} - h_text / book'
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
print(toggle_id)

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
                                                            'plain_text': '(대화기록)',
                                                            'text': {'content': '(대화기록)',
                                                                     'link': None},
                                                            'type': 'text'}]},
                               'type': 'paragraph'
                           },
                           {
                               'divider': {},
                               'object': 'block',
                               'type': 'divider'
                           },
                           {
                               'bulleted_list_item': {'color': 'default',
                                                      'rich_text': [{'annotations': {'bold': False,
                                                                                     'code': False,
                                                                                     'color': 'default',
                                                                                     'italic': False,
                                                                                     'strikethrough': False,
                                                                                     'underline': False},
                                                                     'href': None,
                                                                     'plain_text': '단어: def',
                                                                     'text': {'content': '단어: '
                                                                                         'def',
                                                                              'link': None},
                                                                     'type': 'text'}]},
                               'object': 'block',
                               'type': 'bulleted_list_item'
                           },
{
                               'bulleted_list_item': {'color': 'default',
                                                      'rich_text': [{'annotations': {'bold': False,
                                                                                     'code': False,
                                                                                     'color': 'default',
                                                                                     'italic': False,
                                                                                     'strikethrough': False,
                                                                                     'underline': False},
                                                                     'href': None,
                                                                     'plain_text': '단어: def',
                                                                     'text': {'content': '단어: '
                                                                                         'def',
                                                                              'link': None},
                                                                     'type': 'text'}]},
                               'object': 'block',
                               'type': 'bulleted_list_item'
                           }
                       ]
                   })
r.raise_for_status()
pprint(r.json())
