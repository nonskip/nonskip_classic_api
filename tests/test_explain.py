
import readpilot as rp


def test_explain_example_1():
    text = ...
    highlighted_text = ...
    expected = ...
    actual = rp.explain(rp.Dialogue(), text, highlighted_text)
    assert expected == actual
