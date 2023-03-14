from . import Dialogue
import openai
import os
import re
from dotenv import load_dotenv
import spacy

load_dotenv()

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv('API_KEY')

engine = "gpt-3.5-turbo"

def method_1(d: Dialogue) -> str:
    prompt = "Split the following text into phrasal verbs or words to search the dictionary: \"" + d.h_text + "\""
    response = openai.ChatCompletion.create(
    model=d.model,
    messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def get_chunks(text: str, d: Dialogue) -> Dialogue:
    text_list = text.split('\n')
    print(text_list)
    text_list = [re.sub(r'[^a-zA-Z ]+', '', ele) for ele in text_list]
    text_list = [ele for ele in text_list if ele!='']
    print(text_list)
    d.messages.append("Your words in the highlighted text: " + ", ".join(text_list))
    
    return d


def method_2(d: Dialogue):
    # nlp = spacy.load("en_core_web_sm")
    # matcher = PhraseMatcher(nlp.vocab)
    # matches = matcher(d.h_text)
    # for match_id, start, end in matches:
    #     span = d.h_text[start:end]
    #     print(span.text)
    

    # for match_id, start, end
    return ""

def log(d: Dialogue) -> Dialogue:
    """
    log the dialogue to the database. For the time being, we will use a local database.
    :param d: a Dialogue object.
    :return: a Dialogue object.
    """
    #pass
    # Method 1: ask ChatGPT
    text = method_1(d)
    d= get_chunks(text, d)
    # Method 2: Use other APIs: spaCy
    return d

