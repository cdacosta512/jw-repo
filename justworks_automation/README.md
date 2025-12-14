# Local Tax Update Script

This script fills in missing local tax amounts in a CSV file using data from an XML file.
You do NOT need to edit the script.

--

## Requirements

### Python must be installed

Before running the script, make sure Python is installed.

To check:
    python --version

If Python is not installed, download and install it from:
    https://www.python.org

Use the default install options.

--

## Files You Need

Place all of the following files in the same folder:

- update_local_tax.py
- Your CSV file (example: input.csv)
- Your XML file (example: input.xml)

--

## How to Run the Script

1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to the folder with the files
3. Run:

    python update_local_tax.py input.csv input.xml

Replace input.csv and input.xml with your actual file names.

--

## What Happens

- The script reads the CSV and XML files
- It fills in blank local tax amounts in the CSV
- A new file is created automatically

--

## Output File

- The output file will be named:
  input-UPDATED.csv
- The original CSV file is not changed

--

## Notes

- Only blank tax values are filled in
- Existing values are left untouched
- Rows that do not match are skipped
