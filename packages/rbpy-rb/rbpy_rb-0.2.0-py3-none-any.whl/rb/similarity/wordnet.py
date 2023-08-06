from typing import Callable, List, Tuple, Union

from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from rb.core.lang import Lang
from rb.core.word import Word

from rb.parser.spacy_parser import SpacyParser

lang_dict = {
    Lang.EN: 'eng',
    Lang.NL: 'nld',
    Lang.FR: 'fra',
    Lang.RO: 'ron',
    Lang.IT: 'ita'
}

def compute_similarity(a: str, b: str, lang: Lang, sim: Callable[[Synset, Synset], float]) -> float:
    if lang not in lang_dict:
        return 0
    lang = lang_dict[lang]
    return min([
        sim(syn_a, syn_b)
        for syn_a in wn.synsets(a, lang=lang)
        for syn_b in wn.synsets(b, lang=lang)],
        default=0)

def path_similarity(a: str, b: str, lang: Lang) -> float:
    return compute_similarity(a, b, lang, wn.path_similarity)

def leacock_chodorow_similarity(a: str, b: str, lang: Lang) -> float:
    return compute_similarity(a, b, lang, wn.lch_similarity)

def wu_palmer_similarity(a: str, b: str, lang: Lang) -> float:
    return compute_similarity(a, b, lang, wn.wup_similarity)

def get_synonyms(word: Union[str, Word], lang: Lang = None, pos: str = None) -> List[str]:
    if isinstance(word, Word):
        pos = word.pos.to_wordnet()
        lang = word.lang
        word = word.lemma
    if lang not in lang_dict:
        return []
    return list({other
        for ss in wn.synsets(word, pos=pos, lang=lang_dict[lang]) 
        for other in ss.lemma_names(lang=lang_dict[lang]) 
        if SpacyParser.get_instance().is_dict_word(other, lang)})

def get_hypernyms(word: Union[str, Word], lang: Lang = None, pos: str = None) -> List[str]:
    if isinstance(word, Word):
        pos = word.pos.to_wordnet()
        lang = word.lang
        word = word.lemma
    if lang not in lang_dict:
        return []
    return list({other
        for ss in wn.synsets(word, pos=pos, lang=lang_dict[lang]) 
        for parent in ss.hypernyms() 
        for other in parent.lemma_names(lang=lang_dict[lang]) 
        if SpacyParser.get_instance().is_dict_word(other, lang)})
        

if __name__ == "__main__":
    print(path_similarity('hond', 'kat', 'nl'))
