
from app.main import chat


def test_chat_works_cold_start():
    d = chat("요즘 사랑이란 무엇인지에 대해 깊게 고민하고 있어. 사랑에 대해 앞서 고민해본 작가가 쓴 영문고전을 추천해줄 수 있어?")
    print(d)
    # should return more than 10 characters / just a dead-simple test
    assert len(d.messages[-1].content) > 10


def test_chat_works_continued():
    d = chat("요즘 사랑이란 무엇인지에 대해 깊게 고민하고 있어. 사랑에 대해 앞서 고민해본 작가가 쓴 영문고전을 추천해줄 수 있어?")
    d = chat("추천해줘서 고마워!", d)
    print(d)
    # should return more than 10 characters / just a dead-simple test
    assert len(d.messages[-1].content) > 10
