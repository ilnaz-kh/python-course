## Ex 13 - Q 01
class Book:
    def __init__(self, title, author, publication_year) -> None:
        self.title = title
        self.author = author
        self.pulication_year = publication_year
    def __str__(self) -> str:
        return f"Title: {self.title}, Author: {self.author}, Publication Year: {self.pulication_year}"
    def get_book_info(self):
        print(self) # calling __str__ method
        # print(f"Title: {self.title}, Author: {self.author}, Publication Year: {self.pulication_year}")

book1 = Book("A", "aut", 1984) # calling __init__ method
book2 = Book("B", "aut", 1988) # calling __init__ method
book1.get_book_info()
book2.get_book_info()
