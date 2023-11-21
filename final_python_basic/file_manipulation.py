## Python Command Line Interface (CLI) Tool for File Manipulation

## importing libraries and modules:
import argparse
import os # scandir(), getcwd(), chdir(), makedirs(), rmdir(), remove()
import sys # argv, exit()
import datetime # used in create_log()
import json # used in create_log() and output_logs()

## Global variable to catch whether command is successfully terminated or not
error = "" # a null string
## Global variable to save default current directory in the program
current_dir_default = os.getcwd()  # used in get_current_dir()
## Global variables for file directories:
directory_file = os.path.join(current_dir_default, "current_dir.txt")
log_file = os.path.join(current_dir_default, "log_file.json")

##-----------------------------Functions-----------------------------
## Setup the argparse parser
def setup():
    parser = argparse.ArgumentParser(description="Python Command Line Interface (CLI) Tool for File Manipulation", 
                                     epilog="Thanks for using CLI application for File Manipulation")

    parser.add_argument("PATH", action="store", type=str, nargs="?", default=".", 
                        help="a directory (Default: Current directory)")
    parser.add_argument("--ls", action="store_true",
                        help="Return a list of all files and directories in the `PATH`. (Defult value for `PATH`: ./)")
    parser.add_argument("--cd", action="store_true",
                        help="Change the working directory to `PATH`.")
    parser.add_argument("--mkdir", action="store", metavar="PATH",
                        help="Create a new directory at `PATH`.")
    parser.add_argument("--rmdir", action="store", metavar="PATH",
                        help="Remove the directory at `PATH` if it is empty.")   
    parser.add_argument("--rm", action="store", metavar="FILE | DIRECTORY", 
                        help="Remove the file specified by `FILE`. Remove the directory at `DIRECTORY` and its contents recursively (with -r).")
    parser.add_argument("-r", action="store_true", 
                        help="Is used with --rm `DIRECTORY`")
    parser.add_argument("--cp", action="store", nargs=2, metavar=("SOURCE", "DESTINATION"), 
                       help="Copy a file or directory from `SOURCE` to `DESTINATION`.")
    parser.add_argument("--mv", action="store", nargs=2, metavar=("SOURCE", "DESTINATION"),
                        help="Move a file or directory from `SOURCE` to `DESTINATION`.")
    parser.add_argument("--find", action="store", nargs=2, metavar=("PATH", "PATTERN"),
                        help="Search for files or directories matching `PATTERN` starting from `PATH`.")
    parser.add_argument("--cat", action="store", metavar="FILE", 
                        help="Output the contents of the file `FILE`.")
    ## Aditional commands:
    parser.add_argument("--show-logs", action="store_true", 
                        help="Output the logs.")
    parser.add_argument("--cwd", action="store_true",
                        help="Show the current working directory.")
    parser.add_argument("--exit", action="store_true",
                        help= "Simulate closing command-line interface: Reset CWD")

    return parser

## update Current Directory which is saved in a txt file `current_dir.txt`:
def set_current_dir(dir):
    global error
    try:
        with open(directory_file, "w") as file: # if the file exists, replaces it
            file.write(dir)
    except OSError as e:
        raise e  # raise an exception for caller function


## Read current directory which is saved in a txt file `current_dir.txt`:
def get_current_dir():
    global error
    ## read current directory from the file. create a file and set current directory if the file does not exist
    try:
        with open(directory_file, "r") as file: # if the file exists, replaces it
            current_dir = file.read()
            return current_dir
    except FileNotFoundError as e:
        ## Create File for the first time:
        try:
            set_current_dir(current_dir_default)
            return current_dir_default
        except OSError as e:
            raise e  # raise an exception for caller function
    except OSError as e:
        raise e  # raise an exception for caller function


## Change the working directory to `path`:
def change_directory(path):
    global error
    try:
        ## we used scandir() instead of isfile() and isdir() to get exceptions:
        ## we used `with` to automaticly close the iterator and free acquired resources:
        with os.scandir(path) as entries: # returns an iterator points to all the entries in the path
            pass # the `path` is a valid directory
        
        ## at this point, `path` is valid
        os.chdir(path) 
        dir = os.getcwd() # getcwd() raise an FileNotFoundError
        set_current_dir(dir) # update current directory
    except OSError as e:
        raise e

## Output a list of all files and directories in the `path`:
def list_directory_content(path):
    global error
    try:
        ## we used `with`` to automaticly close the iterator and free acquired resources:
        with os.scandir(path=path) as entries: # returns an iterator points to all the entries in the path
            for entry in entries:
                print(entry.name)
    except OSError as e:
        raise e # raise an exception for caller function


## Create a new directory at `path`:
def make_directory(path):
    global error
    try:
        os.makedirs(path) # Creates multiple directories, including intermediate directories (similar to running mkdir -p in Bash)
    except OSError as e: # Catching Error: FileExistsError, ...
        raise e # raise an exception for caller function


## Remove the directory at `path` if it is empty:
def remove_empty_directory(path):
    global error
    # avoid an error (The process cannot access the file because it is being used by another process) by rmdir(CURRENT_DIRECTORY)
    # Solution: change directory before calling rmdir("."):
    if path == "." or path == "./":
        path = get_current_dir() ## get full path bfore changing directory
    if path ==  get_current_dir():
        try:
            change_directory("..") ## avoid Error
        except OSError as e:
            raise e # raise an exception for caller function  
    try:
        os.rmdir(path) # If the `path` isn’t empty, an OSError is raised
    except OSError as e:
        raise e # raise an exception for caller function


## Remove the file specified by `file`:
def remove_file(file):
    global error
    try:
        os.remove(file) # remove() raise an OSError
    except OSError as e:
        raise e # raise an exception for caller function


## Remove the directory at `directory` and its contents recursively:
def remove_directory(directory):
    ## implementation from scratch:
    global error
    ## we used scandir() instead of isfile() and isdir() to get exceptions:
    try:
        ## we used `with` to automaticly close the iterator and free acquired resources:
        with os.scandir(directory) as entries: # returns an iterator points to all the entries in the path
            pass # the directory is a valid one 
    except OSError as e:
        print(e.strerror)
        print("Error in remove_directory")
        error = "Error: " + e.strerror
        return False
    
    path_subs_files = list(os.walk(directory))[0] # os.walk does not throw exceptions
    path = path_subs_files[0] # a string
    sub_dirs = path_subs_files[1] # a list of subdirs
    files = path_subs_files[2] # a list of files in path

    for subdir in sub_dirs:
        res = remove_directory(os.path.join(path, subdir)) # Recursive calling
        if not res:
            return False # Terminate all recursive functions
    ## There is no sub-directory in the path: remove all files in the path
    for file in files:
        try:
            remove_file(os.path.join(path, file))
        except OSError as e:
            print(e.strerror)
            error = "Error: " + e.strerror
            return False
    ## There is no sub-directory nor files in the path
    try:
        remove_empty_directory(path)
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror
        return False
    return True


## Copy Just one file from source to destination.
## source and destination are file  
def copy_file(source, destination):
    global error
    try:
        file_read = open(source, "rb") # for txt and binary files
        ## read file at source:
        data = file_read.read()
        file_read.close()
        ## Open file to write:
        file_write = open(destination, "wb") # for txt and binary files
        ## write data to destination file:
        file_write.write(data)
        file_write.close()
    except OSError as e:
        raise e # raise an exception for caller function


## A recursive function to copy or move the `source` (a directory with files and sub-directories) to `destination`
def copy_move_directory(source, destination, flag):
    ## implementation from scratch:
    global error
    ## we used scandir() instead of isfile() and isdir() to get exceptions:
    try:
        ## we used `with` to automaticly close the iterator and free acquired resources:
        with os.scandir(source) as entries: # returns an iterator points to all the entries in the path
            pass # the directory is a valid one 
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror
        return False
    
    path_subs_files = (list(os.walk(source)))[0] # a 3-tuple (path, sub_dirs, files)
    dir = path_subs_files[0]
    dir_basename = os.path.basename(dir)
    sub_dirs = path_subs_files[1] # a list of sub-directories
    files = path_subs_files[2] # a list of files
    new_dir = os.path.join(destination, dir_basename)

    # make directory in destination:
    try:
        make_directory(new_dir)
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror
        return False
    ## Copy/Move file from source to destination:    
    for file in files:
        try:
            copy_file(os.path.join(dir, file), os.path.join(new_dir, file))
        except OSError as e:
            print(e.strerror)
            error = "Error: " + e.strerror
            return False
        ## Remove file at source if the task is move:
        if flag == 'move':
            try:
                remove_file(os.path.join(dir, file))
            except OSError as e:
                print(e.strerror)
                error = "Error: " + e.strerror
                return False
    ## Recursive Calling for all sub-directories:
    for sub_dir in sub_dirs:
        res = copy_move_directory(os.path.join(dir, sub_dir), os.path.join(destination, dir_basename), flag) # Recursive calling
        if not res:
            return False # terminate all recursive functions
    ## There is no sub-directory nor files in the `dir` to move:
    if flag == 'move':
        try:
            remove_empty_directory(dir)
        except OSError as e:
            print(e.strerror)
            error = "Error: " + e.strerror
            return False
    return True 


def copy_file_directory(source, destination):
    ## implementation from scratch:
    global error
    if source == "." or source == "./":
        source = get_current_dir() # get full path, so we can use os.path.basename(source))
    
    if os.path.isdir(source): # returns True if source is an existing directory
        if os.path.isdir(os.path.join(destination, os.path.basename(source))):
            print("The directory already exists in destination.")
            error = "Error: The directory already exists in destination."
            return
        res = copy_move_directory(source, destination, flag= 'copy') # Copy all files in the directory
        if not res:
            print("Copy operation failed.")

    elif os.path.isfile(source): # returns True if source is an existing file
        if os.path.isfile(os.path.join(destination, os.path.basename(source))):
            print("The file already exists at destination.")
            error = "Error: The file already exists at destination."
            return
        if os.path.isfile(destination):
            print("Destination must be a directory not a file.")
            error = "Error: Destination must be a directory not a file."
            return
        ## Copy file from source to destination:
        try: 
            copy_file(source, os.path.join(destination, os.path.basename(source)))
        except OSError as e:
            print(e.strerror)
            error = "Error: " + e.strerror
            print("Copy operation failed.")
    else:
        print("The system cannot find the source specified.") 
        error = "Error: The system cannot find the source specified."
        print("Copy operation failed.")


## Move a file or directory from `source` to `destination`:
def move_file_directory(source, destination):
    ## implementation from scratch:
    global error

    if source == "." or source == "./":
        source = get_current_dir() # get full path, so we can use os.path.basename(source))

    if os.path.isdir(source): # returns True if source is an existing directory
        if os.path.isdir(os.path.join(destination, os.path.basename(source))):
            print("The directory already exists in destination.")
            error = "Error: The directory already exists in destination."
            return
        res = copy_move_directory(source, destination, flag= 'move') # Move all files in the directory
        if not res:
            print("Move operation failed.")

    elif os.path.isfile(source): # returns True if source is an existing file
        if os.path.isfile(os.path.join(destination, os.path.basename(source))):
            print("The file already exists at destination.")
            error = "Error: The file already exists at destination."
            return
        if os.path.isfile(destination):
            print("Destination must be a directory not a file.")
            error = "Error: Destination must be a directory not a file."
            return
        
        try: 
            ## Copy file from source to destination:
            copy_file(source, os.path.join(destination, os.path.basename(source)))
            ## Remove file at source:
            remove_file(source)
        except OSError as e:
            print(e.strerror)
            error = "Error: " + e.strerror
            print("Move operation failed.")
    else:
        print("The system cannot find the source specified.") 
        error = "Error: The system cannot find the source specified."
        print("Move operation failed.")


## A Dynamic Programming algorithm to find matching with wildcard patterns (`*`, `?`):
def isMatch(string, pattern):
    m, n = len(string), len(pattern)
    ## Initialize a 2D DP (Dynamic Programming) table:
    dp = []
    for _ in range(m+1):
        dp.append([False]*(n+1)) 
        
    dp[0][0] = True # Empty pattern and empty string
    ## Filling the first row of the DP table: empty string:
    for j in range(1, n + 1):
        if pattern[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
    ## Filling the DP table using bottom-up dynamic programming:
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[j - 1] == '*':
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[j - 1] == '?' or pattern[j - 1] == string[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
 
    return dp[m][n]


## Search for files or directories matching `pattern` starting from `path`:
def search(path, pattern):
    global error
    ## we used scandir() instead of isfile() and isdir() to get exceptions:
    try:
        ## we used `with` to automaticly close the iterator and free acquired resources:
        with os.scandir(path) as entries: # returns an iterator points to all the entries in the path
            pass # the directory is a valid one 
    except OSError as e:
        raise e
    
    paths = list(os.walk(path)) # os.walk does not throw exceptions
    for path, _, files in paths: # paths is a list of 3-tuples [(path, subdirs, files), ...]
        if isMatch(os.path.basename(path), pattern):
            print(path) # a matching
        for file in files:
            if isMatch(file, pattern):
                print(os.path.join(path, file)) # a matching


## Output the contents of the file `file`:
def concatenate(file):
    global error
    try:
        file_read = open(file, "r")
        ## read file at `file`:
        data = file_read.read()
        print(data)
        file_read.close()
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror


## Update JSON log-file
def create_log():
    global error
    command_line = " ".join(sys.argv)
    ## Current date and time is unique so can be used as a key
    ## We convert datetime to str because keys must be str, int, float, bool or None, not datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    outcome = error if error else "Success"
    now_log = {
        "command": command_line,
        "outcome": outcome
    }

    if os.path.isfile(log_file):
        ## Read JSON log-file:
        try:
            with open(log_file, "r") as file_read:
                log_data = json.load(file_read)
        except OSError as e:
            print(e.strerror)
            error = "Error: " + e.strerror
            return
    else: # the first time to create a log
        log_data = {} # an empty dictionary
    
    ## Add new log to the dictionary:
    log_data[now] = now_log
    ## Serializing json
    json_object = json.dumps(log_data, indent=4)
    ## Update JSON log-file:
    try:
        with open(log_file, "w") as file_wirte:
            file_wirte.write(json_object)
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror


## Show logs in a human-readable format:
def output_logs():
    if os.path.isfile(log_file):
        ## Read JSON log-file:
        try:
            with open(log_file, "r") as file_read:
                log_data = json.load(file_read)
                for date, value in log_data.items():
                    print(f"date: {date} Command: {value['command']}\nOutcome: {value['outcome']}\n")
        except OSError as e:
            print(e.strerror)
            error = "Error: " + e.strerror
    else: # There is no log_file
        print("No log has been created yet!")

##-----------------------------Main-----------------------------
parser = setup()
try:
    args = parser.parse_args()
except SystemExit as e: # argparse handles and prints an error then calls sys.exit() which throws a SystemExit exception
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        pass # argparse raise an SystemExit after printing the help message. This should not be considered as an Error
    else:
        error = "Error handled by argparse module"
    create_log() # Create a log before exiting program
    sys.exit(2)

## Change Current Directory:
try:
    os.chdir(get_current_dir())
except OSError as e:
    error = "Error: " + e.strerror
    create_log() # Create a log before exiting program
    print("Cannot change current directory")
    sys.exit(2)

## We used if elif to handle just one command at the same time:
if args.ls: 
    try:
        list_directory_content(args.PATH)
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror
elif args.cd:
    try:
        change_directory(args.PATH)
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror
elif args.mkdir:
    try:
        make_directory(args.mkdir)
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror
elif args.rmdir:
    try:
        remove_empty_directory(args.rmdir)
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror
elif args.rm:
    if args.r:
        res = remove_directory(args.rm) # remove a directory and return True if it was successfully done
        if not res:
            print("Remove operation failed.")
    else:
        try:
            remove_file(args.rm)
        except OSError as e:
            print(e.strerror)
            error = "Error: " + e.strerror
elif args.cp: # args.cp: a list of two string: [`source`, `destination`]
    copy_file_directory(args.cp[0], args.cp[1])  #  copy_file_directory() handles errors itself
elif args.mv: # args.mv: a list of two string: [`source`, `destination`]
    move_file_directory(args.mv[0], args.mv[1]) # move_file_directory() handles errors itself
elif args.find: # args.find: a list of two string: [`path`, `pattern`]
    try:
        search(args.find[0], args.find[1])
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror 
elif args.cat: 
    concatenate(args.cat) # concatenate() handles exceptions itself 
elif args.show_logs:
    output_logs() # output_logs() handles exceptions itself 
elif args.cwd:
    try:
        print(get_current_dir())
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror 
elif args.exit: # Simulate command-line window closing
    try:
        set_current_dir(current_dir_default)
    except OSError as e:
        print(e.strerror)
        error = "Error: " + e.strerror 

# Create a log:
create_log() # create_log() handles exceptions itself 
