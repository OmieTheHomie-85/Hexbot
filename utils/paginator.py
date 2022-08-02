from typing import List

from nextcord import Embed


class Paginator:
    def __init__(self, *, pages: List[Embed]):
        self.pages = pages
        self.current_page = 0
        self.total_pages = len(pages) - 1  # Index starts at 0.

    def last(self):
        self.current_page = -1
        return self.current()

    def previous(self):
        self.current_page -= 1

        if self.current_page < -self.total_pages:
            return self.first()

        return self.pages[self.current_page]

    def current(self):
        return self.pages[self.current_page]

    def next(self):
        self.current_page += 1

        if self.current_page > self.total_pages:
            return self.first()

        return self.pages[self.current_page]

    def first(self):
        self.current_page = 0
        return self.current()
