# File Manipulation CLI

This is a python Command Line Interface (CLI) Tool for File Manipulation.

## Setup
- Ensure Python 3.8 or higher is installed on your system.


## Usage

Run the `file_manipulation.py` script using Python with the desired arguments:

```bash
python file_manipulation.py -h, --help 
python file_manipulation.py --ls [PATH]
python file_manipulation.py --cd [PATH]
python file_manipulation.py --mkdir PATH
python file_manipulation.py --rmdir PATH
python file_manipulation.py --rm FILE
python file_manipulation.py --rm DIRECTORY -r
python file_manipulation.py --cp SOURCE DESTINATION
python file_manipulation.py --mv SOURCE DESTINATION
python file_manipulation.py --find PATH PATTERN
python file_manipulation.py --cat FILE
python file_manipulation.py --show-logs
python file_manipulation.py --cwd
python file_manipulation.py --exit

```

### Arguments

- `-h`, `--help`: Show the help message.
- `--ls [PATH]`: Return a list of all files and directories in the `PATH`. (Defult value for `PATH`: ./)
- `--cd [PATH]`: Change the working directory to `PATH`.
- `--mkdir PATH`: Create a new directory at `PATH`.
- `--rmdir PATH`: Remove the directory at `PATH` if it is empty.
- `--rm FILE`: Remove the file specified by `FILE`.
- `--rm DIRECTORY -r`: Remove the directory at `DIRECTORY` and its contents recursively (with -r).
- `--cp SOURCE DESTINATION`: Copy a file or directory from `SOURCE` to `DESTINATION`.
- `--mv SOURCE DESTINATION`: Move a file or directory from `SOURCE` to `DESTINATION`.
- `--find PATH PATTERN`: Search for files or directories matching `PATTERN` starting from `PATH`.
- `--show-logs`: Show the logs.
- `--cwd`: Show the current working directory (CWD).
- `--exit`:  Simulate closing command-line interface: Reset CWD.

#### More about PATTERN in `--find PATH PATTERN`
The pattern can include the characters ‘?’ and ‘\*’ 
* ‘?’ – matches any single character 
* ‘\*’ – Matches any sequence of characters (including the empty sequence)\
for example PATTERN= ‘\*.txt’ means all files or folders that end with ‘.txt’ (like text files)

## Logs
Logs of the executed commands are stored in `log_file.json` in the following format:

```json

{
    "2023-11-17 18:03:41": {
        "command": "final.py --cat t.txt",
        "outcome": "Success"
    },
    "2023-11-17 18:05:00": {
        "command": "final.py --ls ./dummypath",
        "outcome": "Error: The system cannot find the path specified"
    },
    "2023-11-17 18:25:29": {
        "command": "final.py --show-logs",
        "outcome": "Success"
    },
    // ... other logs
}

```


---
Thanks for using CLI application for File Manipulation