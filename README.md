# py-urbandict

[![Build
Status](https://travis-ci.org/novel/py-urbandict.svg?branch=master)](https://travis-ci.org/novel/py-urbandict)

py-urbandict is a client for urbandictionary.com.

Project page on github: https://github.com/novel/py-urbandict
PyPI: https://pypi.org/project/urbandict/

## Installation

Just run:

  `sudo setup.py install`

## Usage

To use it from command line, just use 'urbancli' tool like that:

```
$ urbandicli xterm
1. xterm
  Godly creature, omnipotent, guru in every way imaginable.
  
  Examples:
  
  * I wish i was an xterm

$
```

Usage from Python:

```
$ python3.2
Python 3.2 (r32:88445, Feb 27 2011, 09:51:00) 
[GCC 4.2.1 20070719  [FreeBSD]] on freebsd8
Type "help", "copyright", "credits" or "license" for more information.
>>> import urbandict
>>> urbandict.define('xterm')
[{'word': 'xterm', 'example': 'I wish i was an xterm', 'def': 'Godly creature, omnipotent, guru in every way imaginable.'}]
>>> 
```

It returns list of defitinitions for a term. Each list item is a dict with the following keys:

* word -- the word itself
* def -- definition of the term
* example -- example of its usage (could be empty)
