from enum import Enum
from enum import IntEnum

class BookType(Enum):
    English = 1
    English_plus = 1
    Math = 2
    Chinese = 3
    Physics = 4
    Chemistry = 5

    def __init__(self, num):
        self.num = num


book_type = BookType(2)
print(BookType.English)
print(BookType.English.value)
print(BookType.English.name)
print(BookType["English"])
print(BookType["English_plus"] == BookType["English"])
print("----------------------")
print(book_type)
print("----------------------")
for b in BookType.__members__:
    print(b)
