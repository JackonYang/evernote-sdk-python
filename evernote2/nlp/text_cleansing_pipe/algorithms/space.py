# -*- coding: utf-8 -*-
import re
# from bs4 import BeautifulSoup
# from tidylib import tidy_fragment


_NON_ASCII_WHITESPACE_CHARS = (
    r'\u0085\u00a0\u1680'
    r'\u2000\u2001\u2002\u2003\u2004\u2005'
    r'\u2006\u2007\u2008\u2009\u200a\u200b'
    r'\u2028\u2029\u202f\u205f\u3000')

_WHITESPACE_ALL_RE = re.compile(r'[\s%s]+' % _NON_ASCII_WHITESPACE_CHARS)
_WHITESPACE_NO_NEWLINE_RE = re.compile(r'[ \t%s]+' % _NON_ASCII_WHITESPACE_CHARS)

_NEWLINE_RE = re.compile('\s*\n+\s*')

# joined_ptn_1 = re.compile(r'(?:[a-z]{2,}))([A-Z]\w)')
# joined_ptn_2 = re.compile(r'\)([A-Z])')

# section_ptn = re.compile(r'(?:<(?:br)|(?:BR)\s*/?>\s*){3,}')
# section_ptn = re.compile(r'(?:<br ?/?>\s*){3,}')


def collapse_spaces(s, keep_new_line):

    if not keep_new_line:
        return collapse_spaces_no_newline(s)

    s = _WHITESPACE_NO_NEWLINE_RE.sub(' ', s.strip())
    s = _NEWLINE_RE.sub('\n\n', s)
    return s.strip()


def collapse_spaces_no_newline(s):
    s = _WHITESPACE_ALL_RE.sub(' ', s.strip())
    return s.strip()


# def pretty_html(text):
#     # text = '<br><br><br>'.join([tidy_fragment(i)[0] for i in section_ptn.split(text)])
#     # bs will keep the last \n if there is any
#     soup = BeautifulSoup(text, 'html.parser')
#     return soup.prettify(formatter=remove_space).strip()


# def split_joined_words(text):

#     text = joined_ptn_1.sub(r'\1 \2', text)
#     text = joined_ptn_2.sub(r') \1', text)

#     return text
