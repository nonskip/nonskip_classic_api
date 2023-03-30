"""
https://developers.notion.com/reference/post-search
make sure your page is shared with Nonskip Classic integration
https://www.notion.so/help/create-integrations-with-the-notion-api
"""
import os
from pprint import pprint

import requests

r = requests.post('https://api.notion.com/v1/search',
                  headers={
                      'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}",
                      'Notion-Version': '2022-06-28'
                  },
                  # if you do not specify any queries, you get all pages that have been shared with your integration
                  json={}
                  )
r.raise_for_status()
pprint(r.json())
