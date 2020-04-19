# -*- coding: utf-8 -*-
"""
    :Source - https://github.com/un33k/python-slugify
 
    :HOWTO

    from slugify import slugify

    txt = "This is a test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = "___This is a test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = "___This is a test___"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = "This -- is a ## test ---"
    r = slugify(txt)
    self.assertEqual(r, "this-is-a-test")

    txt = '影師嗎'
    r = slugify(txt)
    self.assertEqual(r, "ying-shi-ma")

    txt = 'C\'est déjà l\'été.'
    r = slugify(txt)
    self.assertEqual(r, "c-est-deja-l-ete")

    txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
    r = slugify(txt)
    self.assertEqual(r, "nin-hao-wo-shi-zhong-guo-ren")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt)
    self.assertEqual(r, "jaja-lol-mememeoo-a")

    txt = 'Компьютер'
    r = slugify(txt)
    self.assertEqual(r, "kompiuter")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=9)
    self.assertEqual(r, "jaja-lol")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=15)
    self.assertEqual(r, "jaja-lol-mememe")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=50)
    self.assertEqual(r, "jaja-lol-mememeoo-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=15, word_boundary=True)
    self.assertEqual(r, "jaja-lol-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=17, word_boundary=True)
    self.assertEqual(r, "jaja-lol-mememeoo")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=18, word_boundary=True)
    self.assertEqual(r, "jaja-lol-mememeoo")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=19, word_boundary=True)
    self.assertEqual(r, "jaja-lol-mememeoo-a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True, separator=".")
    self.assertEqual(r, "jaja.lol.mememeoo.a")

    txt = 'jaja---lol-méméméoo--a'
    r = slugify(txt, max_length=20, word_boundary=True, separator="ZZZZZZ")
    self.assertEqual(r, "jajaZZZZZZlolZZZZZZmememeooZZZZZZa")

    txt = 'one two three four five'
    r = slugify(txt, max_length=13, word_boundary=True, save_order=True)
    self.assertEqual(r, "one-two-three")

    txt = 'one two three four five'
    r = slugify(txt, max_length=13, word_boundary=True, save_order=False)
    self.assertEqual(r, "one-two-three")

    txt = 'one two three four five'
    r = slugify(txt, max_length=12, word_boundary=True, save_order=False)
    self.assertEqual(r, "one-two-four")

    txt = 'one two three four five'
    r = slugify(txt, max_length=12, word_boundary=True, save_order=True)
    self.assertEqual(r, "one-two")

    txt = 'this has a stopword'
    r = slugify(txt, stopwords=['stopword'])
    self.assertEqual(r, 'this-has-a')

    txt = 'the quick brown fox jumps over the lazy dog'
    r = slugify(txt, stopwords=['the'])
    self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')

    txt = 'Foo A FOO B foo C'
    r = slugify(txt, stopwords=['foo'])
    self.assertEqual(r, 'a-b-c')

    txt = 'Foo A FOO B foo C'
    r = slugify(txt, stopwords=['FOO'])
    self.assertEqual(r, 'a-b-c')

    txt = 'the quick brown fox jumps over the lazy dog in a hurry'
    r = slugify(txt, stopwords=['the', 'in', 'a', 'hurry'])
    self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')

    txt = 'foo &amp; bar'
    r = slugify(txt)
    self.assertEqual(r, 'foo-bar')
"""

import re
import unicodedata
import types
import sys

try:
    from html.entities import name2codepoint
    _unicode = str
    _unicode_type = str
except ImportError:
    from html.entities import name2codepoint
    _unicode = str
    _unicode_type = str
    chr = chr

#import unidecode


__all__ = ['slugify']


CHAR_ENTITY_PATTERN = re.compile('&(%s);' % '|'.join(name2codepoint))
DECIMAL_PATTERN = re.compile('&#(\d+);')
HEX_PATTERN = re.compile('&#x([\da-fA-F]+);')
QUOTE_PATTERN = re.compile(r'[\']+')
ALLOWED_CHARS_PATTERN = re.compile(r'[^-a-z0-9]+')
DUPLICATE_DASH_PATTERN = re.compile('-{2,}')
NUMBERS_PATTERN = re.compile('(?<=\d),(?=\d)')
#test
DISALLOWED_CHARS_PATTERN = re.compile(r'[\/\?\#\s&]+')


def smart_truncate(string, max_length=0, word_boundaries=False, separator=' ', save_order=False):
    """
    Truncate a string.
    :param string (str): string for modification
    :param max_length (int): output string length
    :param word_boundaries (bool):
    :param save_order (bool): if True then word order of output string is like input string
    :param separator (str): separator between words
    :return:
    """

    string = string.strip(separator)

    if not max_length:
        return string

    if len(string) < max_length:
        return string

    if not word_boundaries:
        return string[:max_length].strip(separator)

    if separator not in string:
        return string[:max_length]

    truncated = ''
    for word in string.split(separator):
        if word:
            next_len = len(truncated) + len(word)
            if next_len < max_length:
                truncated += '{0}{1}'.format(word, separator)
            elif next_len == max_length:
                truncated += '{0}'.format(word)
                break
            else:
                if save_order:
                    break
    if not truncated:
        truncated = string[:max_length]
    return truncated.strip(separator)


def slugify(text, entities=True, decimal=True, hexadecimal=True, max_length=0, word_boundary=False,
            separator='-', save_order=False, stopwords=()):
    """
    Make a slug from the given text.
    :param text (str): initial text
    :param entities (bool):
    :param decimal (bool):
    :param hexadecimal (bool):
    :param max_length (int): output string length
    :param word_boundary (bool):
    :param save_order (bool): if parameter is True and max_length > 0 return whole words in the initial order
    :param separator (str): separator between words
    :param stopwords (iterable): words to discount
    :return (str):
    """

    # ensure text is unicode
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')

    # replace quotes with dashes - pre-process
    text = QUOTE_PATTERN.sub('-', text)
    
#     # decode unicode
#     text = unidecode.unidecode(text)
# 
#     # ensure text is still in unicode
#     if not isinstance(text, _unicode_type):
#         text = _unicode(text, 'utf-8', 'ignore')

    # character entity reference
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: chr(name2codepoint[m.group(1)]), text)
    
    # decimal character reference
    if decimal:
        try:
            text = DECIMAL_PATTERN.sub(lambda m: chr(int(m.group(1))), text)
        except:
            pass

    # hexadecimal character reference
    if hexadecimal:
        try:
            text = HEX_PATTERN.sub(lambda m: chr(int(m.group(1), 16)), text)
        except:
            pass
    
#     #translate
#     text = unicodedata.normalize('NFKD', text)
#     if sys.version_info < (3,):
#         text = text.encode('ascii', 'ignore')
    
    # make the text lowercase
    text = text.lower()
    
    # remove generated quotes -- post-process
    text = QUOTE_PATTERN.sub('', text)

    # replace unwanted characters
    text = NUMBERS_PATTERN.sub('', text)
#     text = ALLOWED_CHARS_PATTERN.sub('-', text)
    text = DISALLOWED_CHARS_PATTERN.sub('-', text)
    
    # remove redundant -
    text = DUPLICATE_DASH_PATTERN.sub('-', text).strip('-')
    
    # remove stopwords
    if stopwords:
        stopwords_lower = [s.lower() for s in stopwords]
        words = [w for w in text.split('-') if w not in stopwords_lower]
        text = '-'.join(words)
    
    # smart truncate if requested
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, '-', save_order)
    
    if separator != '-':
        text = text.replace('-', separator)
    
    return text


def main():
    if len(sys.argv) < 2:
        print(("Usage %s TEXT TO SLUGIFY" % sys.argv[0]))
    else:
        text = ' '.join(sys.argv[1:])
        print((slugify(text)))