from blum_automation import automation
from colorama import Fore, Style
from time import sleep

def main():
    automation()
    print(Style.BRIGHT + Fore.LIGHTWHITE_EX + "\nThe automation has been completed successfully!")
    sleep(3)

if __name__ == '__main__':
    main()