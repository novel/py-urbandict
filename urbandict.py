#!/usr/bin/env python3.2
#
# Simple interface to urbandictionary.com
#
# Author: Roman Bogorodskiy <bogorodskiy@gmail.com>

import urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser
from urllib.parse import quote as urlquote

class UrbanDictParser(HTMLParser):
    inside_index_item = False
    inside_word_section = False
    inside_def_section = False
    inside_example_section = False
    translations = []

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
    f = urllib.request.urlopen(("http://www.urbandictionary.com/"
            "define.php?term=%s") % urlquote(term))
    data = f.read().decode('utf-8')

    urbanDictParser = UrbanDictParser()
    urbanDictParser.feed(data)

    return urbanDictParser.translations
