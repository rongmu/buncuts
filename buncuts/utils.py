# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import codecs
import re

default_delimeter = "。！？▲"
default_quote_dict = {"「": "」", "『": "』"}


def split_into_sentences(text=sys.stdin, sentence_delim=default_delimeter,
                         quote_dict=default_quote_dict,
                         output=sys.stdout, append=False,
                         is_dir=False, limit=float('inf'),
                         echo=False):
    # TODO: implement the echo and limit option.
    # TODO: implement encoding option.
    # TODO: implement chunk_size option.

    count = 0

    # create a list from chars in a string
    sentence_delim = list(sentence_delim)

    if append:
        mode = 'a'
    else:
        mode = 'w'

    if text is not sys.stdin:
        text_file = codecs.open(text, 'r', 'sjis')
    else:
        text_file = text

    if output is not sys.stdout:
        if is_dir:
            path = os.path.join(output, os.path.basename(text))
            output_file = codecs.open(path, mode, 'sjis')
        else:
            output_file = codecs.open(output, mode, 'sjis')
    else:
        output_file = output

    for line in text_file:
        # [todo] - skip empty line.
        count += 1

        # strip half/full width spaces
        # strip() somehow don't work very well.
        # use re instead.
        line = re.sub(r"^[ 　\n]+|[ 　]+$", "", line)

        line_splitted, count_added = chunk_splitter(line,
                                                    sentence_delim, quote_dict)

        output_file.write(line_splitted)
        count += count_added

    # close files
    if text is not sys.stdin:
        text_file.close()

    if output is not sys.stdout:
        output_file.close()


def chunk_splitter(chunk,
                   sentence_delim=default_delimeter,
                   quote_dict=default_quote_dict):
    """Chunk splitter.
    Reads in a chunk, returns the splitted string and a count as a tuple:
    (result, count)
    """
    result = ""
    count = 0

    length = len(chunk)

    outside_quote = True
    quote_chars = quote_dict.keys()
    current_quote = ""
    current_close_quote = ""

    for i in xrange(length):
        char = chunk[i]
        result = ''.join((result, char))  # append char to the result

        # TODO: Should use a FILO to avoid multiple embeded quotations.
        if outside_quote:
            if char in quote_chars:
                outside_quote = False
                current_quote = char
                current_close_quote = quote_dict[current_quote]

            elif char in sentence_delim:
                count += 1

                # add a newline after a sentence delimeter.
                if i < length - 1 and chunk[i+1] != '\n':
                    result = ''.join((result, '\n'))
                elif i == length - 1:
                    result = ''.join((result, '\n'))

        elif char == current_close_quote:
            outside_quote = True

    return result, count
