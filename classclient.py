class Client:

    def __init__(self, id):
        self.id_ = id
        self.books_ = {}
        self.lines_ = []
        self.writer_ = ""
        self.book_ = -1
        self.max_book_ = -1
        self.max_page_ = -1
        self.page_ = -1
        self.max_line_ = -1
        self.line_ = -1
        self.all_writers_ = {}
