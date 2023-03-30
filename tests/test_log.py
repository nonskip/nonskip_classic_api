from pprint import pprint
from app.main import explain, log


def test_log_little_prince():
    context = """
    “My drawing was not a picture of a hat.  It was a picture of a boa constrictor digesting an elephant.  But since the grown-ups were not able to understand it, I made another drawing:  I drew the inside of the boa constrictor, so that the grown-ups could see it clearly.  They always need to have things explained.  My Drawing Number Two looked like this:”

Excerpt From
The Little Prince
Antoine de Saint-Exupery
This material may be protected by copyright."""
    s_text = "a boa constrictor"
    d = explain(context, s_text)
    r = log(context, s_text, d)
    pprint(r)

