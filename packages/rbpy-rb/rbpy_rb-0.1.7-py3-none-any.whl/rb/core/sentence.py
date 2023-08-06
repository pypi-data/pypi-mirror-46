from rb.parser.spacy_parser import SpacyParser

from spacy.tokens.doc import Doc

from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.core.word import Word
from rb.core.text_element_type import TextElementType

from typing import Tuple, List
Dependency = Tuple[Word, Word, str]
Dependencies = List[Dependency]

class Sentence(TextElement):


    def __init__(self, lang: Lang, text: str,
                 depth: int = TextElementType.SENT.value,
                 container: TextElement = None):

        TextElement.__init__(self, lang=lang, text=text,
                             depth=depth, container=container)
        self.doc = SpacyParser.get_instance().parse(text, lang.value)

        for token in self.doc:
            word = Word(lang, token, container=self)
            self.components.append(word)

    def get_dependencies(self) -> Dependencies:
        return [(self.components[word.token.head.i], word, word.token.dep_) 
                for word in self.components 
                if word.token.head != word.token]
            
    def get_sentences(self) -> List["Sentence"]:
        return [self]