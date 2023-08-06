from enum import Enum
from typing import Union

import numpy as np
from numpy.linalg import norm

from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.core.word import Word


class VectorModelType(Enum):
    LSA = 0,
    LDA = 1,
    WORD2VEC = 2,
    FASTTEXT = 3,
    GLOVE = 4


class VectorModel:
    def __init__(self, type: VectorModelType, name: str, lang: Lang, size: int = 300):
        self.lang = lang
        self.type = type
        self.name = name
        self.size = size
        self.vectors = {}

    def get_vector(self, elem: Union[str, TextElement]) -> np.array:
        if isinstance(elem, str):
            return self.vectors[elem]
        if not self in elem.vectors:
            if isinstance(elem, Word):
                if elem.text in self.vectors:
                    elem.vectors[self] = self.vectors[elem.text]
                elif elem.lemma in self.vectors:
                    elem.vectors[self] = self.vectors[elem.lemma]
                else:
                    return None
            else:
                elem.vectors[self] = np.sum([child for child in elem.components])
        return elem.vectors[self]
            
    
    def similarity(self, a: Union[TextElement, np.array], b: Union[TextElement, np.array]) -> float:
        if isinstance(a, TextElement) and isinstance(b, TextElement) and a == b:
            return 1.0
        if isinstance(a, TextElement):
            a = self.get_vector(a)
        if isinstance(b, TextElement):
            b = self.get_vector(b)
        if a is None or b is None:
            return 0.0
        return np.dot(a, b) / (norm(a) * norm(b))
