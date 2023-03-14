from . import Dialogue
import openai


def ask_chatgpt(d: Dialogue):
    prompt = """
    Suggest 5 probable questions about the expression or the word based on the context. 
    Only return the questions without any other comments.
    """
    model = d.model
    chat_completion = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "context": prompt}]
    )
    response = chat_completion.choices[0].message.content
    suggest_questions = response.split('\n')
    return suggest_questions


def suggest(d: Dialogue) -> list[str]:
    result = ask_chatgpt(d)
    return result

