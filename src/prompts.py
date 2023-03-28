"""
All prompts are defined here.
"""

SYSTEM = f"너는 데미안, 변신, 농담, 어린왕자 등 모든 영문고전을 다 읽고 깊게 이해한 사람이야." \
                f"사용자가 영문고전을 읽으면서 이해가 안가는 부분을 물어볼거야. 그럴 때마다 맥락에 관계지어 설명해줘. "

EXPLAIN = "{context} \n\n 위 문맥에서 (({s_text}))의 의미가 뭐야? 사전적 정의말고 문맥에서 지니는 의미를 한국어로 설명해줘."


SUGGEST = f"Considering this reader's previous Q&A history and the common difficulties in reeading English classics as " \
          f"an English learner, " \
          "Suggest five questions that the reader is most likely to ask with regards to (({s_text})) and the context." \
          "Don't suggest content-related questions. Suggest grammar-related or vocabulary-related questions." \
          "Exclude any unnecessary comment except for your suggestions while answering." \
          "(give your answer in Korean, not English)."
