from enum import Enum
from rb.complexity.surface.factory import create as surface
from rb.complexity.syntax.factory import create as syntax
from rb.complexity.morphology.factory import create as morphology
from functools import partial

class IndexCategory(Enum):
    SURFACE = partial(surface)
    MORPHOLOGY = partial(morphology)
    SYNTAX = partial(syntax)
