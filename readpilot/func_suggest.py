from . import Dialogue


def suggest(d: Dialogue) -> list[str]:
    prompt = "Considering this reader's previous Q&A history and the common difficulties in reading foreign language texts, please suggest five questions that the reader is most likely to curious about especially in terms of expression usages. \
        Please encourage extensive learning not to be just limited to this text itself. \
        Exclude any unnecessary comment except for your suggestions while answering."
        
    response = openai.ChatCompletion.create(
        model = d.model,
        messages = [{"role": "assistant", "content": prompt}]
    )
    result = response["choices"][0].message.content.split('\n')
    
    
    return result