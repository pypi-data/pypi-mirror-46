#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Book:
    def __init__(self, testament, name, code, position):
        self.testament = testament
        self.name = name
        self.code = code
        self.position = position
        self.chapters = []

    def get_chapters(self):
        """
        Get list of chapters of this book
        :return: list of chapter of book
        """
        return self.chapters
