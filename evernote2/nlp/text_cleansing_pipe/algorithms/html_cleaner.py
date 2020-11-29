import re
import string

from html.parser import HTMLParser

from .space import collapse_spaces

h = HTMLParser()

regex_html = re.compile('<.*?>')

# Chinese punctuations are not removed, which is not good
regex_punctuation = re.compile('[%s]' % re.escape(string.punctuation))


def clean_html_entity(text):
    return h.unescape(text)


def clean_text_for_hash(text, keep_new_line=False):

    text = clean_html_entity(text)

    text = regex_html.sub(' ', text)
    text = regex_punctuation.sub(' ', text)

    text = collapse_spaces(text, keep_new_line)

    return text
