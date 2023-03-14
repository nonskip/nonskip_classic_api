from . import Dialogue


def suggest(d: Dialogue) -> list[str]:
<<<<<<< HEAD
    prompt = "Considering this reader's previous Q&A history and the common difficulties in reading foreign language texts, please suggest five questions that the reader is most likely to be curious about especially in terms of expression usages. \
        Please encourage extensive learning not to be just limited to this text itself. \
        Exclude any unnecessary comment except for your suggestions while answering."
        
    response = openai.ChatCompletion.create(
        model = d.model,
        messages = [{"role": "assistant", "content": prompt}]
    )
    result = response["choices"][0].message.content.split('\n')
    
    
    return result
=======
    return [
        "좀 더 쉽게 설명해줘.",
        "비슷한 표현으론 뭐가 있어?",
        "자주 쓰이는 표현이야?"
    ]
>>>>>>> bfc1499f1ff849301cb56ba44033cd2bfa8bf421
