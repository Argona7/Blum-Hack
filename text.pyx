# cython: language_level=3

import os
import cython
from sys import stdout
from time import sleep
import ctypes
from colorama import Fore, Style, init


ctypes.windll.kernel32.SetConsoleTitleW("Blum Hacking by Argona")

init(autoreset=True)


cpdef void clear_console():

    if os.name == 'nt':
        os.system('cls')
  
    else:
        os.system('clear')

@cython.cfunc
def set_console_size(int columns=150, int lines=40):
    """Функция для установки размера консоли через ctypes"""
    cdef object kernel32 = ctypes.WinDLL('kernel32')
    cdef object handle = kernel32.GetStdHandle(-11)
    cdef object buffer_size = ctypes.wintypes._COORD(columns, lines)
    cdef object window_size = ctypes.wintypes._SMALL_RECT(0, 0, columns - 1, lines - 1)
    kernel32.SetConsoleScreenBufferSize(handle, buffer_size)
    kernel32.SetConsoleWindowInfo(handle, ctypes.c_long(True), ctypes.byref(window_size))

@cython.cfunc
@cython.locals(default_columns=cython.int, default_lines=cython.int)
def get_terminal_size(int default_columns=150, int default_lines=40) -> tuple:
    """Получение размера консоли с установкой значений по умолчанию в случае ошибки"""
    cdef int columns, lines
    try:
        columns, lines = os.get_terminal_size()
    except OSError:
        columns, lines = default_columns, default_lines
    return columns, lines

@cython.cfunc
def print_text_with_effect(text: cython.str, color: cython.str=Fore.RED, float speed=0.02):
   
    lines = text.strip('\n').splitlines()

  
    columns, total_lines = get_terminal_size()

   
    cdef int max_length = max(len(line) for line in lines)

    
    cdef int vertical_padding = (total_lines - len(lines)) // 2
    cdef int horizontal_padding = (columns - max_length) // 2

  
    cdef int i
    for i in range(max_length):
        stdout.write("\033[H\033[J") 
        for _ in range(vertical_padding):
            print()
        for line in lines:
            print(' ' * horizontal_padding + color + line[:i] + Style.RESET_ALL)
        stdout.flush()
        sleep(speed)


    sleep(1)


    for i in range(max_length, -1, -1):
        stdout.write("\033[H\033[J") 
        for _ in range(vertical_padding):
            print() 
        for line in lines:
            print(' ' * horizontal_padding + color + line[:i] + Style.RESET_ALL)
        stdout.flush()
        sleep(speed)


cpdef void print_name():
    set_console_size(columns=150, lines=40)

    text = """
  ('-.      _  .-')                                  .-') _     ('-.            ('-. .-.    ('-.                 .-. .-')   
  ( OO ).-. ( \( -O )                                ( OO ) )   ( OO ).-.       ( OO )  /   ( OO ).-.             \  ( OO )  
  / . --. /  ,------.    ,----.      .-'),-----. ,--./ ,--,'    / . --. /       ,--. ,--.   / . --. /    .-----.  ,--. ,--.  
  | \-.  \   |   /`. '  '  .-./-')  ( OO'  .-.  '|   \ |  |\    | \-.  \        |  | |  |   | \-.  \    '  .--./  |  .'   /  
.-'-'  |  |  |  /  | |  |  |_( O- ) /   |  | |  ||    \|  | ) .-'-'  |  |       |   .|  | .-'-'  |  |   |  |('-.  |      /,  
 \| |_.'  |  |  |_.' |  |  | .--, \ \_) |  |\|  ||  .     |/   \| |_.'  |       |       |  \| |_.'  |  /_) |OO  ) |     ' _) 
  |  .-.  |  |  .  '.' (|  | '. (_/   \ |  | |  ||  |\    |     |  .-.  |       |  .-.  |   |  .-.  |  ||  |`-'|  |  .   \   
  |  | |  |  |  |\  \   |  '--'  |     `'  '-'  '|  | \   |     |  | |  |       |  | |  |   |  | |  | (_'  '--'\  |  |\   \  
  `--' `--'  `--' '--'   `------'        `-----' `--'  `--'     `--' `--'       `--' `--'   `--' `--'    `-----'  `--' '--'  
    """

    print_text_with_effect(text)
