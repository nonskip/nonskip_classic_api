"""
creates a page named "Nonskip Classic (DEV)"
https://developers.notion.com/reference/post-page
"""
import requests
import os
from pprint import pprint

page_id = "21dca7d6-d6ef-4941-bde3-bb2730d12ff3"
r = requests.get(f'https://api.notion.com/v1/blocks/{page_id}/children?page_size=100',
                 headers={
                     'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}",
                     'Notion-Version': '2022-06-28'
                 })
r.raise_for_status()  # why does this return a 404?
pprint(r.json())
