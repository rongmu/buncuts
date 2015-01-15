TODO
====

- [ ] Consider using inno setup to install your app  
      - http://www.jrsoftware.org/isinfo.php

## Qt

- [ ] Implement progress indicator. eg. ProgressBar.
      (QFuture depends on C++, is not supported in Python)  
      http://qt-project.org/wiki/Progress-bar

## buncuts.utils

- [ ] _delayed_ Perhaps also check whether the splitted sentences are enclosed.
- [ ] Also implent a simple quote checking method that only do one-level check?
- [x] Split lines that are totally enclosed in quotation.
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
