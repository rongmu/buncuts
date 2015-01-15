TODO
====

- [ ] Consider using inno setup to install your app  
      - http://www.jrsoftware.org/isinfo.php

## Qt

- [ ] Implement progress indicator. eg. ProgressBar.
      (QFuture depends on C++, is not supported in Python)  
      http://qt-project.org/wiki/Progress-bar

## buncuts.utils

- [ ] Strip the quotation marks of lines that are
      totally enclosed in quotation.
  - [ ] `split_line()`:  
        Before the return, see if the processed string is inside quotation.
        If so, strip the outermost quotation marks and
        `return split_line(result)`.
        Return a list of lines instead of a string.
        Tuple and count no longer needed.
  - [ ] `process_single_file()`:  
        Check if the line is enclosed in quotation.
        If it's true, strip the first and last quotation marks,
        pass the line again to the `split_chunk()`with `check_quote=False`.
- [ ] Also implent a simple quote checking method that only do one-level check?
- [x] Should use a FILO to avoid multiple embeded quotations.
- [x] Allow user to specify output line ending format in API.
      In GUI, no option for this, just keep the original format.  
- [x] Allow user to specify the input/output encodings

### process_single_file()

- [ ] _delayed_ implement the echo and limit option.
- [x] skip empty lines.

## buncuts.app

- [ ] `on_btnBrowseInput_clicked()`:  
      Restrict the selectable files to *.txt files.
