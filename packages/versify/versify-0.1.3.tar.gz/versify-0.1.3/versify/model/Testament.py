#!/usr/bin/env python
# -*- coding: utf-8 -*-

from versify.model.Book import Book
from versify.model.Chapter import Chapter


class Testament:
    def __init__(self, name, damn_id, type, version):
        self.name = name
        self.damn_id = damn_id
        self.type = type
        self.version = version

    def __repr__(self):
        return super().__repr__()

    def get_books(self, dbt):
        book_list = []
        url = dbt.get_api_url("/library/book", {"dam_id": self.damn_id})
        books = dbt.get_request(url)

        for book in books:
            b = Book(self,
                     book['book_name'],
                     book['book_id'],
                     book['book_order'])
            list_chapters = book['chapters'].split(',')
            for c in list_chapters:
                b.chapters.append(Chapter(b, c))
            book_list.append(b)

        return book_list
