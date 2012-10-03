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
        self.inside_index_item = False
        self.inside_word_section = False
        self.inside_def_section = False
        self.inside_example_section = False
        self.translations = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "td":
            if 'class' in attrs_dict:
                if attrs_dict['class'] == 'index':
                    self.inside_index_item = True
                elif attrs_dict['class'] == 'word':
                    self.inside_word_section = True
        elif tag == "div":
            if 'class' in attrs_dict:
                if attrs_dict['class'] == 'definition':
                    self.inside_def_section = True
                elif attrs_dict['class'] == 'example':
                    self.inside_example_section = True

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inside_def_section is True:
                self.inside_def_section = False
            elif self.inside_example_section is True:
                self.inside_example_section = False

    def handle_data(self, data):
        if self.inside_index_item is True:
            self.translations.append({})
            self.translations[-1]['def'] = ''
            self.translations[-1]['example'] = ''
            self.inside_index_item = False
        elif self.inside_word_section is True:
            self.translations[-1]['word'] = data.strip()
            self.inside_word_section = False
        elif self.inside_def_section is True:
            self.translations[-1]['def'] += data.replace('\r', '\n')
        elif self.inside_example_section is True:
            self.translations[-1]['example'] += data.replace('\r', '\n')


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
