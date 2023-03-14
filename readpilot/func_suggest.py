from . import Dialogue


def suggest(d: Dialogue) -> list[str]:
    return [
        "좀 더 쉽게 설명해줘.",
        "비슷한 표현으론 뭐가 있어?",
        "자주 쓰이는 표현이야?"
    ]
