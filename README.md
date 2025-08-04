# BW-Industrial-Prj
## Excel Trend Checker

This tool analyzes trends in financial data from two sheets in an Excel file, compares them, and writes any differences to a new summary sheet.

## How to Use
### Step 01: Create new folder data under project root folder.
### Step 02: Copy your Excel report file into `data/` folder.
### Step 03: Create virtual environment then active to use.
```bash
Create virtual environment
$ python -m venv venv

Active to use
$ venv\Scripts\activate
```
### Step 04: Install dependencies:
Run below command to install dependencies
```bash
pip install -r requirements.txt
```

### Step 05: Run application
Run below command to run application
```bash
$ python main.py
```