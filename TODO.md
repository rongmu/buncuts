TODO
====

- [ ] Deal with line ending format problem,  
      this time it should be Windows first.
- [ ] Consider using inno setup to install your app  
      - http://www.jrsoftware.org/isinfo.php
- [x] Allow user to specify the input/output encodings

## Qt

- [ ] Implement progress indicator. eg. ProgressBar.
      (QFuture depends on C++, is not supported in Python)  
      http://qt-project.org/wiki/Progress-bar

## buncuts.utils
### split_into_sentences()

- skip empty line.
- implement the echo and limit option.
- implement chunk_size option.

### chunk_splitter()

- Should use a FILO to avoid multiple embeded quotations.
