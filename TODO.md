TODO
====

- [ ] Progress stucks when input has only one or zero line.
- [ ] _perhaps_ re-solve UI response problem via multi-threading?
- [x] Solve the UI Blocking problem.

## Pre-process Checks
- [ ] Directory output mode: Check existance, Warn before overwrite  
      (app.process) if `ts._output_is_dir`
      and files in `ts.get_output_list()` exist
      proceed after confirming overwrite, otherwise return.
- [x] Check empty
- [x] raise error in `_get_quote_dict`: QuoteUnevenError

## Qt

- [x] class ErroBox(QMessageBox)
- [x] Subclass QProgressDialog.

## buncuts.app

- [x] `on_btnBrowseInput_clicked()`:  
      Restrict the selectable files to *.txt files.

## buncuts.utils

- [ ] _delayed_ Perhaps also check whether the splitted sentences are enclosed.
- [ ] _delayed_ Also implent a simple quote checking method  
      that only does one-level check?
- [ ] _delayed_ implement the echo and limit option.
