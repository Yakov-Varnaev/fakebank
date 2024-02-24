class Pagination:
    def __init__(self, offset: int | None = None, limit: int | None = None):
        self.offset = offset
        self.limit = limit
