"""
creates a page named "Nonskip Classic (DEV)"
https://developers.notion.com/reference/post-page
"""
import requests
import os
from pprint import pprint

page_id = "868b6634-8508-4b4c-b502-fc5741929419"
r = requests.get(f'https://api.notion.com/v1/pages/{page_id}',
                 headers={
                     'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}",
                     'Notion-Version': '2022-06-28'
                 })
r.raise_for_status()  # why does this return a 404?
pprint(r.json())
