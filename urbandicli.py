#!/usr/bin/env python
#
# Simple interface to urbandictionary.com
#
# Author: Roman Bogorodskiy <bogorodskiy@gmail.com>

import urllib2
import sys
from HTMLParser import HTMLParser
from urllib import quote as urlquote

class UrbanDictParser(HTMLParser):
    inside_index_item = False
    inside_word_section = False
    inside_def_section = False
    inside_example_section = False
    current_index = None
    translations = {}

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            if len(attrs) > 0:
                if attrs[0][0] == 'class' and attrs[0][1] == 'index':
                    self.inside_index_item = True
                elif attrs[0][0] == 'class' and attrs[0][1] == 'word':
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
            self.current_index = data.strip()[:-1]
            self.translations[self.current_index] = {}
            self.translations[self.current_index]['def'] = ''
            self.translations[self.current_index]['example'] = ''
            self.inside_index_item = False
        elif self.inside_word_section is True:
            self.translations[self.current_index]['word'] = data.strip()
            self.inside_word_section = False
        elif self.inside_def_section is True:
            self.translations[self.current_index]['def'] += data
        elif self.inside_example_section is True:
            self.translations[self.current_index]['example'] += data

    def getTranslations(self):
        return self.translations

def usage():
    print "Usage: %s <term>\n" % sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    term = urlquote(sys.argv[1])

    f = urllib2.urlopen("http://www.urbandictionary.com/define.php?term=%s" % term)
    data = f.read()

    urbanDictParser = UrbanDictParser()
    urbanDictParser.feed(data)
    translations = urbanDictParser.getTranslations()

    # pretty print them
    indexen = translations.keys()
    indexen.sort()

    for index in indexen:
        print "%s. %s" % (index, translations[index]['word'])
        print translations[index]['def'].replace('\r', '\n')
        if translations[index]['example'] != '':
            print "Examples:"
            print translations[index]['example'].replace('\r', '\n')
