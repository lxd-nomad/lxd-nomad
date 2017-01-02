# -*- coding: utf-8 -*-

import re
import unicodedata


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text):
    """ Returns a ASCII-only slug version of the considered text. """
    result = []
    for word in _punct_re.split(text.lower()):
        word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('ascii')
        if word:
            result.append(word)
    return '-'.join(result)
