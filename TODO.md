TODO
====

- [ ] Progress stucks when input has only one or zero line.
- [x] Solve the UI Blocking problem.

## Pre-process Checks
- [ ] Output should not be empty. Otherwise will output to pwd.
      Also should validate output path.
- [ ] raise error in `_get_quote_dict`

## Qt

- [ ] class ErroBox(QMessageBox)
- [x] Subclass QProgressDialog.

## buncuts.utils

- [ ] _delayed_ Perhaps also check whether the splitted sentences are enclosed.
- [ ] _delayed_ Also implent a simple quote checking method  
      that only does one-level check?

### process_single_file()

- [ ] _delayed_ implement the echo and limit option.

## buncuts.app

- [ ] `on_btnBrowseInput_clicked()`:  
      Restrict the selectable files to *.txt files.
