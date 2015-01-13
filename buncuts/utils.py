# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import codecs
import re

default_delimeter = list("。！？▲")
default_quote_dict = {"「": "」", "『": "』"}


def split_sentences(input_list,
                    input_enc='sjis',
                    output=sys.stdout,
                    output_enc='sjis',
                    append=False,
                    is_dir=False,
                    sentence_delim=default_delimeter,
                    quote_dict=default_quote_dict,
                    limit=float('inf'),
                    echo=False):
    """Split the text from input files into sentences.

    Args:
        input_list: A list of paths of input files.
        input_enc: Character encoding of the input files.
            Defauts to Shift-JIS.
        output: Path of output destination.
            Defauts to stdout.
        output_enc: Character encoding of the output file(s).
            Defauts to Shift-JIS.
        append: Whether append to output or not.
        is_dir: Whether the output is a directory or a regular file.
        sentence_delim: A list of sentence delimeters.
        quote_dict: A dict that maps opening quote marks
            to its closing counterpart.
        limit: The limit for maximum amout of sentences
            that should be extracted.
        echo: Whether echo the output or not.
    """
    for f in input_list:
        process_single_file(input=f,
                            output=output,
                            append=append,
                            is_dir=is_dir,
                            sentence_delim=sentence_delim,
                            quote_dict=quote_dict,
                            limit=limit,
                            echo=echo)


def process_single_file(input=sys.stdin,
                        input_enc='sjis',
                        output=sys.stdout,
                        output_enc='sjis',
                        append=False,
                        is_dir=False,
                        sentence_delim=default_delimeter,
                        quote_dict=default_quote_dict,
                        limit=float('inf'),
                        echo=False):
    """Perform line breaks on one file.

    Will call split_chunk() for each line in the input file.
    """
    count = 0

    if append:
        mode = 'a'
    else:
        mode = 'w'

    if input is not sys.stdin:
        input_file = codecs.open(input, 'r', input_enc)
    else:
        input_file = input

    if output is not sys.stdout:
        if is_dir:
            path = os.path.join(output, os.path.basename(input))
            output_file = codecs.open(path, mode, output_enc)
        else:
            output_file = codecs.open(output, mode, output_enc)
    else:
        output_file = output

    for line in input_file:
        count += 1

        # strip half/full width spaces
        # strip() somehow don't work very well.
        # use re instead.
        line = re.sub(r"^[ 　]+|[ 　]+$", "", line)

        if line == '\n':
            continue

        line_splitted, count_added = split_chunk(line,
                                                 sentence_delim,
                                                 quote_dict)

        output_file.write(line_splitted)
        count += count_added

    # close files
    if input is not sys.stdin:
        input_file.close()

    if output is not sys.stdout:
        output_file.close()


def split_chunk(chunk,
                sentence_delim=default_delimeter,
                check_quote=True,
                quote_dict=default_quote_dict):
    """Split a chunk.

    Returns:
        A tuple that contains the splitted string and the count of
        sentence delimeters in the chunk: (result, count)
    """
    result = ""
    count = 0
    length = len(chunk)

    outside_quote = True
    quote_chars = quote_dict.keys()
    current_quote = ""
    current_close_quote = ""

    for i, char in enumerate(chunk):
        # Always append original char to the result.
        result = ''.join((result, char))

        # If quotation check is required,
        # do sentence delimeter examination only when current character
        # is outside quotation and is not a quotation mark itself.
        # Otherwise continue to the next iteration.
        if check_quote:
            if outside_quote:
                if char in quote_chars:
                    outside_quote = False
                    current_quote = char
                    current_close_quote = quote_dict[current_quote]
                    continue
                else:
                    pass
            else:
                if char == current_close_quote:
                    outside_quote = True
                continue

        # Additionaly, append a newline after a sentence delimeter.
        if char in sentence_delim:
            count += 1

            if i < length - 1 and chunk[i+1] != '\n':
                result = ''.join((result, '\n'))
            elif i == length - 1:
                result = ''.join((result, '\n'))

    return result, count
