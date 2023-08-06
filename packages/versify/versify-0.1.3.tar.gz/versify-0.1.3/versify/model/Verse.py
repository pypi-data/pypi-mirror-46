#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Verse:
    def __init__(self, chapter, verse_number, text):
        self.verse_number = verse_number
        self.chapter = chapter
        self.text = text

    def __str__(self):
        return "<{}>".format(self.text)

    def __repr__(self):
        return "<{}>".format(self.text)
