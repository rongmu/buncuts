# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import re

default_delimeter = set("。！？▲")
default_quote_dict = {"「": "」", "『": "』"}

default_input_enc = 'sjis'
default_output_enc = default_input_enc


class _QuoteChecker:
    """Quote checker.

    The instance is expected to be used in an iteration,
    to check whether a character is inside a (nested) quotatoin
    in a sequence of text.
    """
    def __init__(self, quote_dict):
        self.quote_dict = quote_dict
        self.open_quotes = quote_dict.keys()
        self.quotes_remained = []
        self.first_append_index = None
        self.first_pop_index = None

    def is_outside_quote(self, char, i):
        """Return True if the char is outside a quotation, False if not."""
        if char in self.open_quotes:
            close_quote = self.quote_dict[char]
            self.quotes_remained.append(close_quote)

            if self.first_append_index is None:
                self.first_append_index = i
        elif (len(self.quotes_remained) != 0
                and char == self.quotes_remained[-1]):
            self.quotes_remained.pop()

        if len(self.quotes_remained) == 0:
            if self.first_pop_index is None:
                self.first_pop_index = i
            return True
        else:
            return False


class TextSplitter:
    def __init__(self,
                 input_list,
                 output_path,
                 input_enc=default_input_enc,
                 output_enc=default_output_enc,
                 output_newline=None,
                 output_is_dir=False,
                 output_append=False,
                 delimiters=default_delimeter,
                 quote_dict=default_quote_dict,
                 check_quote=True):
        self.input_list = input_list
        self.input_enc = input_enc

        self.output_path = output_path
        self.output_enc = output_enc
        self.output_newline = output_newline
        self.output_is_dir = output_is_dir
        if output_append:
            self.write_mode = 'a'
        else:
            self.write_mode = 'w'

        self.delimiters = delimiters
        self.quote_dict = quote_dict
        self.check_quote = check_quote

    def _process_single_file(self, input_path, output_file):
        input_file = io.open(input_path,
                             mode='r',
                             encoding=self.input_enc)
        try:
            for line in input_file:
                line = re.sub(r"^[ 　]+|[ 　\n]+$", "", line)

                if line == '':
                    continue

                line_splitted = split_line(line,
                                           self.delimiters,
                                           self.quote_dict,
                                           self.check_quote)
                output_file.write(line_splitted)
        finally:
            input_file.close()

    def _output_to_dir(self):
        for file_path in self.input_list:
            if self.output_newline is None:
                output_newline = _get_newline(file_path,
                                              self.input_enc)
            else:
                output_newline = self.output_newline

            output_path = os.path.join(self.output_path,
                                       os.path.basename(file_path))
            output_file = io.open(output_path,
                                  mode=self.write_mode,
                                  encoding=self.output_enc,
                                  newline=output_newline)

            try:
                self._process_single_file(file_path, output_file)
            finally:
                output_file.close()

    def _output_to_file(self):
        if self.output_newline is None:
            output_newline = _get_newline(self.input_list[0],
                                          self.input_enc)
        else:
            output_newline = self.output_newline

        output_file = io.open(self.output_path,
                              mode=self.write_mode,
                              encoding=self.output_enc,
                              newline=output_newline)

        try:
            for file_path in self.input_list:
                self._process_single_file(file_path, output_file)
        finally:
            output_file.close()

    def process(self):
        if self.output_is_dir:
            self._output_to_dir()
        else:
            self._output_to_file()


def _get_newline(file_path, enc):
    newline = None

    with io.open(file_path, 'r', encoding=enc) as f:
        f.readline()
        newline = f.newlines

    return newline


def split_line(line,
               delimiters=default_delimeter,
               quote_dict=default_quote_dict,
               check_quote=True):
    """Split a line into lines of sentences.

    Returns:
        The resulted string
    """
    result = ""
    newline_preventers = delimiters | {'\n'}
    qc = _QuoteChecker(quote_dict)

    line = line.rstrip('\n')
    length = len(line)

    for i, char in enumerate(line):
        # Always append original char to the result.
        result = ''.join((result, char))

        if check_quote:
            if qc.is_outside_quote(char, i):
                pass
            else:
                continue

        # Additionaly, append a newline after a sentence delimeter.
        if char in delimiters:
            if ((i <= length - 2 and line[i+1] not in newline_preventers)
                    or i == length - 1):
                result = ''.join((result, '\n'))

    # re-parse if entire line is enclosed.
    if (check_quote
            and qc.first_append_index == 0
            and qc.first_pop_index == length - 1):
        reparsed = split_line(result[1:-1],
                              delimiters,
                              quote_dict,
                              check_quote)
        # rstrip to avoid \n before the last quotation mark.
        reparsed = reparsed.rstrip('\n')
        result = ''.join((result[0],
                          reparsed,
                          result[-1]))

    if result[-1] != '\n':
        result = ''.join((result, '\n'))

    return result
