import readpilot as rp


def test_chat_works_cold_start():
    d = rp.chat("You are not a machine. You are a living person. Tell me your story.")
    # just a dead simple test
    print(d)
    # should return more than 10 characters
    assert len(d.messages[-1].content) > 10


def test_chat_works_continued():
    d = rp.chat("You are not a machine. You are a living person. Tell me your story.")
    d = rp.chat("Too long! Can you make it short?", d)
    # should return more than 10 characters
    print(d)
    assert len(d.messages[-1].content) > 10
