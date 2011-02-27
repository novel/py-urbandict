#!/usr/bin/env python3.2
#
# Simple interface to urbandictionary.com
#
# Author: Roman Bogorodskiy <bogorodskiy@gmail.com>

import urllib.request, urllib.error, urllib.parse
import sys
import textwrap
from html.parser import HTMLParser
from urllib.parse import quote as urlquote

class UrbanDictParser(HTMLParser):
    inside_index_item = False
    inside_word_section = False
    inside_def_section = False
    inside_example_section = False
#    current_index = 0
    translations = []

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            attrs_dict = dict(attrs)

            if 'class' in attrs_dict:
                if attrs_dict['class'] == 'index':
                    self.inside_index_item = True
                elif attrs_dict['class'] == 'word':
                    self.inside_word_section = True
        elif tag == "div":
            if len(attrs) > 0:
                if attrs[0][0] == 'class' and attrs[0][1] == 'definition':
                    self.inside_def_section = True
                elif attrs[0][0] == 'class' and attrs[0][1] == 'example':
                    self.inside_example_section = True

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inside_def_section is True:
                self.inside_def_section = False
            elif self.inside_example_section is True:
                self.inside_example_section = False

    def handle_data(self, data):
        if self.inside_index_item is True:
 #           self.current_index += 1
            self.translations.append({})
#            self.translations[:-1] = {}
#            print(self.translations[-1])
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

    def getTranslations(self):
        return self.translations

def usage():
    print("Usage: %s <term>\n" % sys.argv[0])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    term = urlquote(sys.argv[1])

    f = urllib.request.urlopen("http://www.urbandictionary.com/define.php?term=%s" % term)
    data = f.read().decode('utf-8')

    urbanDictParser = UrbanDictParser()
    urbanDictParser.feed(data)
    translations = urbanDictParser.getTranslations()

    for index in range(len(translations)):
        print("%s. %s" % (index + 1, translations[index]['word']))
        print('\n'.join(textwrap.wrap(translations[index]['def'])))

        if translations[index]['example'] != '':
            print("Examples:")
            print('\n'.join(textwrap.wrap(translations[index]['example'])))
        print("\n")
