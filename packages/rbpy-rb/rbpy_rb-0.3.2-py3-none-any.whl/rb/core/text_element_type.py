from enum import Enum, unique

@unique
class TextElementType(Enum):
    WORD = 0
    SENT = 1
    BLOCK = 2
    DOC = 3