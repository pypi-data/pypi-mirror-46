#!/usr/bin/env python
# -*- coding: utf-8 -*-


class WikipediaItem:

    def __init__(self, pageid, title, original_title, url, summary):
        self.pageid = pageid
        self.title = title
        self.original_title = original_title
        self.url = url
        self.summary = summary

    def __str__(self):
        return self.summary
