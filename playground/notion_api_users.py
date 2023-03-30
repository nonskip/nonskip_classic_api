"""
Notion Page를 맘대로 접근할 수 있음! - 웹에 공개 중인 페이지라면 가능하다.
"""
from pprint import pprint
import os
import requests


"""
curl 'https://api.notion.com/v1/users' \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Notion-Version: 2022-06-28"
"""

r = requests.get('https://api.notion.com/v1/users',
                 headers={'Notion-Version': '2022-06-28',
                          'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}"})
r.raise_for_status()
pprint(r.json())