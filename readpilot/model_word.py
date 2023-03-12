from dataclasses import dataclass


@dataclass
class Word:
    lemma: str
    definition: str
