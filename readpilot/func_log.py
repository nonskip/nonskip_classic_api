from . import Dialogue
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv('API_KEY')

engine = "gpt-3.5-turbo"

def method_1(d: Dialogue):
    prompt = "Split the following text into phrasal verbs or words to search the dictionary and return the definitions: \"" + d.h_text + "\""
    response = openai.ChatCompletion.create(
    model=d.model,
    messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def log(d: Dialogue) -> Dialogue:
    """
    log the dialogue to the database. For the time being, we will use a local database.
    :param d: a Dialogue object.
    :return: a Dialogue object.
    """
    #pass
    # Method 1: ask ChatGPT
    result = method_1(d)
    # Method 2: Scrape from Papago/etc.
    # Method 3: Use other APIs: spaCy
    return result

