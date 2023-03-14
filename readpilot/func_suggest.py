from . import Dialogue
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('API_KEY')

def method_1(d: Dialogue) -> list[str]:
    # Questions should be provided... In Progress
    pass

def parse(p: str) -> list[str]:
    # The input may be the format of following:
    # 
    # As an AI language model, I cannot predict exactly what questions someone might ask based on this dialogue. 
    # However, I can provide some possible questions that could be asked:
    # 
    # 1. ...
    # 2. ...
    # 3. ...
    # 
    # The output should be list of questions!
    # 
    return [*filter(lambda s: s != '', p.split(':')[1].split('\n'))]

def method_2(d: Dialogue) -> list[str]:
    prompt = "What are the probable questions that can be asked in this dialogue?" +\
        "The response should be formatted as following without any other comments: \n" +\
        "1. ...\n" + "2. ...\n" + "..."
    response = openai.ChatCompletion.create(
        model = d.model,
        messages = [{"role": "assistant", "content": prompt}]
    )
    result = parse(response["choices"][0]["message"]["content"])
    return result

def suggest(d: Dialogue) -> list[str]:
    # Method 1: Hard-Coded Questions
    # result = method_1(d)

    # Method 2: Ask ChatGPT to generate Questions
    result = method_2(d)

    return result
