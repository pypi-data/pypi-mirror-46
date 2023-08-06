
from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.complexity.index_category import IndexCategory
from rb.utils.rblogger import Logger 
from typing import List, Iterable, Callable
from rb.core.text_element_type import TextElementType
from rb.complexity.measure_function import MeasureFunction
logger = Logger.get_logger()

class ComplexityIndex():
    """General class for any complexity index
    
    Attributes
    ----------
    lang : Lang
        language where the index is applied
    category : IndexCategory
        type of the index e.g. SURFACE, SYNTAX
    abbr : str
        short string describing the index
    reduce_depth : TextElementType
        the depth (in the document) where the reduce_function is applied
        the index is applied recursivley on all the above element types from the document tree
    reduce_function : Callable[[List], float]
        a function to summarize the results of the index (average or standard deviation)

    Methods
    -------
    process(element: TextElement)
        computes the index, overwritten for each index
    
    __repr__()
        detailed string representation of the index, should overwritten by each index
    """

    def __init__(self, lang: Lang, category: IndexCategory, abbr: str, reduce_depth: int, reduce_function: MeasureFunction):
        self.lang = lang
        self.category = category
        self.abbr = abbr
        self.reduce_function = reduce_function
        self.reduce_depth = reduce_depth

    # overwritten by each index
    def process(self, element: TextElement) -> float:
        pass

    # overwritten by each index 
    def __repr__(self):
        return self.abbr

# computed indices and saves for each TextElement in indices dictionary
def compute_indices(element: TextElement):
    logger.info('Starting computing all indices for {0} type element'.format(type(element).__name__))
    for cat in IndexCategory:
        for index in cat.value(element.lang):
            index.process(element)

    

    