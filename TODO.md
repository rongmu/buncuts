TODO
====

- [ ] Consider using inno setup to install your app  
      - http://www.jrsoftware.org/isinfo.php

## Qt

- [ ] Implement progress indicator. eg. ProgressBar.
      (QFuture depends on C++, is not supported in Python)  
      http://qt-project.org/wiki/Progress-bar

## buncuts.utils

- [ ] Allow user to specify output line ending format in API.
      In GUI, no option for this, just keep the original format.  
      Also, check `file.newlines` out.
  - [ ] `process_single_file()`:  
        Translate line endings in the file to `\n`
        before passing it to `split_chunk()`.  
        Also, translate the newline back to the format the original file uses,
        before writing to the output.
- [ ] Strip the quotation marks of lines that are
      totally enclosed in quotation.
  - [ ] `split_chunk()`:  
        Return a list of lines instead of a string.
        Tuple and count no longer needed.
  - [ ] `process_single_file()`:  
        Check if the line is enclosed in quotation.
        If it's true, strip the first and last quotation marks,
        pass the line again to the `split_chunk()`with `check_quote=False`.
- [x] Allow user to specify the input/output encodings

### process_single_file()

- [ ] _delayed_ implement the echo and limit option.
- [x] skip empty lines.

### split_chunk()

- [ ] Should use a FILO to avoid multiple embeded quotations.
