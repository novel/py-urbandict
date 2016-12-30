#!/usr/bin/env python
#
# Simple interface to urbandictionary.com
#
# Author: Roman Bogorodskiy <bogorodskiy@gmail.com>

import sys

if sys.version < '3':
    from urllib import quote as urlquote
    from urllib2 import urlopen
    from HTMLParser import HTMLParser
else:
    from urllib.request import urlopen
    from urllib.parse import quote as urlquote
    from html.parser import HTMLParser


class TermType(object):
    pass


class TermTypeRandom(TermType):
    pass


class UrbanDictParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._section = None
        self.translations = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag != "div":
            return

        div_class = attrs_dict.get('class')
        if div_class in ('def-header', 'meaning', 'example'):
            self._section = div_class
            if div_class == 'def-header':
                # NOTE: assume 'word' is the first section
                self.translations.append(
                    {'word': '', 'def': '', 'example': ''})

    def handle_endtag(self, tag):
        if tag == 'div':
            # NOTE: assume there is no nested <div> in the known sections
            self._section = None

    def handle_data(self, data):
        if not self._section:
            return

        if self._section == 'meaning':
            self._section = 'def'
        elif self._section == 'def-header':
            data = data.strip()
            self._section = 'word'

        self.translations[-1][self._section] += normalize_newlines(data)


def normalize_newlines(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')


def define(term):
    if isinstance(term, TermTypeRandom):
        url = "http://www.urbandictionary.com/random.php"
    else:
        url = "http://www.urbandictionary.com/define.php?term=%s" % \
              urlquote(term)

    f = urlopen(url)
    data = f.read().decode('utf-8')

    urbanDictParser = UrbanDictParser()
    urbanDictParser.feed(data)

    return urbanDictParser.translations
