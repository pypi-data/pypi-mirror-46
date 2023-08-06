# -*- coding: utf-8 -*-


class FakeS3Object(object):
    def __init__(self, key=None, last_modified=None, e_tag=None, content_length=None):
        self.key = key
        self.last_modified = last_modified
        self.e_tag = e_tag
        self.content_length = content_length
