import myparser

class Client:

    def __init__(self, id):
        self.id_ = id
        self.books_ = {}
        self.writer_ = ""
        self.book_ = -1
        self.max_book_ = -1
        self.max_page_ = -1
        self.page_ = -1
        self.maxLine_ = -1
        self.line_ = -1
        self.all_writers_ = {}

    def append_writer(self, name_of_writer):
        self.writer_ = name_of_writer

    def append_books(self, name_of_writer, name_of_books):
        self.books_ = myparser.get_books(name_of_writer, name_of_books)
