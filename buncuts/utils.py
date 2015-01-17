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
    """Split a line into lines of sentences and return the resulted string."""
    result_list = []
    newline_preventers = delimiters | {'\n'}
    qc = _QuoteChecker(quote_dict)

    line = line.rstrip('\n')
    length = len(line)

    for i, char in enumerate(line):
        # Always append original char to the result.
        result_list.append(char)

        if check_quote:
            if qc.is_outside_quote(char, i):
                pass
            else:
                continue

        # Additionaly, append a newline after a sentence delimeter.
        if char in delimiters:
            if ((i <= length - 2 and line[i+1] not in newline_preventers)
                    or i == length - 1):
                result_list.append('\n')

    result = ''.join(result_list)

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


class _QuoteChecker(object):
    """Quote checker.

    The instance is expected to be used in an iteration,
    to check whether a character is inside a (nested) quotation
    in a sequence of text.
    """
    def __init__(self, quote_dict):
        self._quote_dict = quote_dict
        self._quotes_remained = []
        self.first_append_index = None
        self.first_pop_index = None

    def is_outside_quote(self, char, i):
        """Return True if the char is outside a quotation, False if not."""
        if char in self._quote_dict:
            close_quote = self._quote_dict[char]
            self._quotes_remained.append(close_quote)

            if self.first_append_index is None:
                self.first_append_index = i

        elif (len(self._quotes_remained) != 0
                and char == self._quotes_remained[-1]):
            self._quotes_remained.pop()

        if len(self._quotes_remained) == 0:
            if self.first_pop_index is None:
                self.first_pop_index = i
            return True
        else:
            return False


class TextSplitter(object):
    def __init__(self,
                 input_list,
                 output_path,
                 output_is_dir=False,
                 output_append=False,
                 input_enc=default_input_enc,
                 output_enc=default_output_enc,
                 output_newline=None,
                 delimiters=default_delimeter,
                 check_quote=True,
                 quote_dict=default_quote_dict):
        """ Text Splitter.

        Notes on Arguments:
            input_list: A list of paths of input files.
            delimiters: A set of sentence delimiters.
        """
        self._input_list = input_list
        self._input_enc = input_enc

        self._output_path = output_path
        self._output_enc = output_enc
        self._output_newline = output_newline
        self._output_is_dir = output_is_dir
        if output_append:
            self._write_mode = 'a'
        else:
            self._write_mode = 'w'

        self._delimiters = delimiters
        self._quote_dict = quote_dict
        self._check_quote = check_quote

    def __unicode__(self):
        if self._output_newline is None:
            output_newline = "Same as input"
        else:
            if self._output_newline == '\r\n':
                output_newline = "CRLF"
            elif self._output_newline == '\n':
                output_newline = "LF"

        delim_list = list(self._delimiters)
        delim_list.sort()
        delimiters = ''.join(delim_list)

        quote_list = [ "{open_}{close}".format(open_=k, close=v)
                      for k, v in self._quote_dict.iteritems() ]
        quotes = ';'.join(quote_list)

        summary = ("Summary {repr_}\n"
                   "-------\n"
                   "Input List: {input_list}\n"
                   "Output Path: {output_path}\n"
                   "Is Output a Directory? {output_is_dir}\n"
                   "Output Write Mode: {write_mode}\n"
                   "Input Encoding: {input_enc}\n"
                   "Output Encoding: {output_enc}\n"
                   "Output Newline Format: {output_newline}\n"
                   "Sentence Delimiters: {delimiters}\n"
                   "Check Quotation? {check_quote}\n"
                   "Quotations: {quotes}\n"
                   ).format(repr_=repr(self),
                            input_list=";".join(self._input_list),
                            output_path=self._output_path,
                            output_is_dir=self._output_is_dir,
                            write_mode=self._write_mode,
                            input_enc=self._input_enc,
                            output_enc=self._output_enc,
                            output_newline=output_newline,
                            delimiters=delimiters,
                            check_quote=self._check_quote,
                            quotes=quotes)

        return summary

    def _process_single_file(self, input_path, output_file):
        input_file = io.open(input_path,
                             mode='r',
                             encoding=self._input_enc)
        try:
            for line in input_file:
                if self._progress is not None:
                    if self._progress.wasCanceled():
                        break
                    self._count += 1
                    self._progress.setValue(self._count)

                line = re.sub(r"^[ 　]+|[ 　\n]+$", "", line)

                if line == '':
                    continue

                line_splitted = split_line(line,
                                           self._delimiters,
                                           self._quote_dict,
                                           self._check_quote)
                output_file.write(line_splitted)
        finally:
            input_file.close()

    def _output_to_dir(self):
        for file_path in self._input_list:
            if self._progress is not None and self._progress.wasCanceled():
                break

            if self._output_newline is None:
                output_newline = _get_newline(file_path,
                                              self._input_enc)
            else:
                output_newline = self._output_newline

            output_path = os.path.join(self._output_path,
                                       os.path.basename(file_path))
            output_file = io.open(output_path,
                                  mode=self._write_mode,
                                  encoding=self._output_enc,
                                  newline=output_newline)

            try:
                self._process_single_file(file_path, output_file)
            finally:
                output_file.close()

    def _output_to_file(self):
        if self._output_newline is None:
            output_newline = _get_newline(self._input_list[0],
                                          self._input_enc)
        else:
            output_newline = self._output_newline

        output_file = io.open(self._output_path,
                              mode=self._write_mode,
                              encoding=self._output_enc,
                              newline=output_newline)

        try:
            for file_path in self._input_list:
                if self._progress is not None and self._progress.wasCanceled():
                    break

                self._process_single_file(file_path, output_file)
        finally:
            output_file.close()

    def total_lines(self):
        num_lines = sum(1 for f in self._input_list for line in open(f))
        return num_lines

    def process(self, progress=None):
        if progress is not None:
            self._progress = progress
            self._count = 0

        if self._output_is_dir:
            self._output_to_dir()
        else:
            self._output_to_file()
