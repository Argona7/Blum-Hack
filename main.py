import json
import requests
from blum_automation import automation
from colorama import Fore, Style
from time import sleep

def main():
    try:
        automation()
        print(Style.BRIGHT + Fore.LIGHTWHITE_EX + "\nThe automation has been completed successfully!")
        sleep(3)
    except Exception as e:
        print(e)
        input()

if __name__ == '__main__':
    main()