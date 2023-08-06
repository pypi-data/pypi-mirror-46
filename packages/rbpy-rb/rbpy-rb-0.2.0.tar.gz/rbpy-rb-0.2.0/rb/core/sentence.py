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
        doc = SpacyParser.get_instance().parse(text, lang.value)

        for token in doc:
            word = Word(lang, token, container=self)
            self.components.append(word)
        for word, token in zip(self.components, doc):
            word.head = self.components[token.head.i]
            if word.head is not word:
                word.head.children.append(word)
        self.root = self.components[list(doc.sents)[0].root.i]

    def get_dependencies(self) -> Dependencies:
        return [(word.head, word, word.dep) 
                for word in self.components 
                if word.head != word]
            
    def get_sentences(self) -> List["Sentence"]:
        return [self]