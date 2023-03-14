"""
All prompts are defined here.
"""
import datetime


PROMPT_SYSTEM = f"You are ChatGPT, a large language model trained by OpenAI. "\
                "Answer as concisely as possible. "\
                f"Current date: {datetime.datetime.today()}"


PROMPT_EXPLAIN = "{text} \n\n 위 문맥에서 (({h_text}))의 의미가 뭐야? 사전적 정의말고 문맥에서 지니는 의미를 한국어로 설명해줘."


PROMPT_SUGGEST = "Considering this reader's previous Q&A history and the common difficulties in reading foreign language texts, please suggest five questions that the reader is most likely to curious about especially in terms of expression usages. \
           Please encourage extensive learning not to be just limited to this text itself. \
           Exclude any unnecessary comment except for your suggestions while answering."