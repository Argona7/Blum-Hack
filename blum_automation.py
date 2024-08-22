# cython: language_level=3

import os
import json
import time
import requests
from ctypes import windll
from random import randint
from colorama import Fore, Style
from text import print_name, clear_console

windll.kernel32.SetConsoleTitleW("Blum Hacking by Argona")


failed_request = {
    "claim farm": True,
    "start farm": True,
    "get game id": True
}

# start farm , claim farm , get game id

def get_farming_time(additional_seconds: float, thousandths: bool):
    if thousandths:
        start = int(int(time.time() * 1000) + additional_seconds * 1000)
        end = start + 28800000  # adding 8 hours, because farming lasts 8 hours.
        return (start, end)
    else:
        start = int(time.time()) + additional_seconds
        return start


def get_refresh_token(tokens_file_path: str):
    if os.path.exists(tokens_file_path):
        # Если файл существует, читаем его содержимое
        with open(tokens_file_path, 'r', encoding='utf-8') as file:
            tokens = {}
            data = json.load(file)
            if not data["accounts"]:
                print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Необходимо добавить аккаунты!")
                time.sleep(1)
                return False

            accounts_names = data["accounts"].keys()
            for i in accounts_names:
                account = data["accounts"][i]
                if (not account["refreshed"]) or (not account["timestamp"]) or (
                        (account["timestamp"] + 3600) < get_farming_time(0, False)):
                    if not account["refresh_token"]:
                        continue
                    tokens[account["refresh_token"]] = [i, "refresh"]
                else:
                    tokens[account["access_token"]] = [i, "access"]

            return (tokens, list(accounts_names))

    else:
        data = {
            "accounts": {}
        }
        with open(tokens_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + f"Файл не найден. Создан новый файл по пути: {tokens_file_path}")
            print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Необходимо добавить аккаунты!")
            time.sleep(1)
            return False


def get_access_tokens(refresh_token: str, account_name: str, tokens_file_path: str, max_attempts: int):
    url = "https://gateway.blum.codes/v1/auth/refresh"
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "accept": "application/json, text/plain, */*",
        "origin": "https://telegram.blum.codes"
    }
    data = {"refresh": refresh_token}

    for attempt in range(max_attempts):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            timestamp = get_farming_time(0, False)
            data = response.json()
            if os.path.exists(tokens_file_path):
                with open(tokens_file_path, 'r', encoding='utf-8') as file:
                    data_file = json.load(file)

                data_file["accounts"][account_name]["refresh_token"] = data["refresh"]
                data_file["accounts"][account_name]["access_token"] = data["access"]
                data_file["accounts"][account_name]["timestamp"] = timestamp

                with open(tokens_file_path, 'w', encoding='utf-8') as file:
                    json.dump(data_file, file, ensure_ascii=False, indent=4)

                print(Fore.LIGHTGREEN_EX + f"Refresh token updated!")
                return data["access"]
            else:
                print(Fore.LIGHTWHITE_EX + Style.BRIGHT + f"File {tokens_file_path} was not found.")
                print(Fore.LIGHTWHITE_EX + Style.BRIGHT + f"Record refresh token manually: {data['refresh']}\ntimestamp: {timestamp}")
                time.sleep(1)
                return True
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(3)

    print(Fore.LIGHTRED_EX + "Failed to get an access token!")
    return False


# {
#     "availableBalance": str,
#     "playPasses": int,
#     "isFastFarmingEnabled": bool,
#     "timestamp": int,
#     "farming": {
#         "startTime": int (timestamp),
#         "endTime": int (timestamp),
#         "earningsRate": str (0.0022),
#         "balance": str (farming balance status)
#     }
# }
def get_account_info(headers: dict, max_attempts: int):
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to obtain an account balance......")
    url = "https://game-domain.blum.codes/api/v1/user/balance"

    for attempts in range(max_attempts):
        response = requests.get(url, headers=headers)
        data = response.json()
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            time.sleep(1)
            return data
        else:
            print(data)
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(3)

    print(Fore.LIGHTRED_EX + "Failed to get an account balance!")
    return False


def get_daily_reward(headers: dict, max_attempts: int):
    print(Fore.YELLOW + Style.BRIGHT + "Attempting a daily reward......")
    url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-180"

    params = {
        "offset": -180
    }
    for attempt in range(max_attempts):
        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            time.sleep(1)
            return True
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(3)

    return False


def farming_claim(headers: dict, account_info: dict, max_attempts: int):
    print(Fore.YELLOW + Style.BRIGHT + "Attempting a farming reward......")

    url = "https://game-domain.blum.codes/api/v1/farming/claim"
    data = {
        "availableBalance": account_info["availableBalance"],
        "playPasses": account_info["playPasses"],
        "isFastFarmingEnabled": account_info["isFastFarmingEnabled"],
        "timestamp": get_farming_time(0.5, True)[0]
    }
    for attempt in range(max_attempts):
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            time.sleep(1)
            return True
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(3)

    failed_request["claim farm"] = False
    print(Fore.LIGHTRED_EX + "Failed to get an reward!")
    return False


def farming_start(headers: dict, max_attempts: int):
    print(Fore.YELLOW + Style.BRIGHT + "Attempting to start farming......")
    url = "https://game-domain.blum.codes/api/v1/farming/start"
    for attempt in range(max_attempts):
        timestamp = get_farming_time(1, True)
        data = {
            "startTime": timestamp[0],
            "endTime": timestamp[1],
            "earningsRate": "0.0022",
            "balance": "0"
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            time.sleep(1)
            return True
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(3)

    failed_request["start farm"] = False
    print(Fore.LIGHTRED_EX + "Failed to start farming!")
    return False


def farm(account_info: dict, headers: dict):
    global failed_request
    if account_info['farming']['endTime'] <= get_farming_time(0, True)[0]:
        if farming_claim(headers, account_info, 3):
            if farming_start(headers, 3):
                return
            else:
                time.sleep(2)
                return

        else:
            time.sleep(2)
            return

    else:
        print(Fore.LIGHTRED_EX + "Farming is already in progress!")
        return


def friends_claim_points(headers: dict, max_attempts: int):
    global failed_request

    print(Fore.YELLOW + Style.BRIGHT + "Trying to get points for friends......")
    url = "https://gateway.blum.codes/v1/friends/claim"

    for attempt in range(max_attempts):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if response.json()["code"] == 12:
                print(Fore.LIGHTBLACK_EX + "Points for friends already received or not available!")
                time.sleep(1)
                return
            print(Fore.LIGHTGREEN_EX + "Successful!")
            return
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(3)

    print(Fore.LIGHTRED_EX + "Failed to get points for friends!")
    time.sleep(2)
    return False


def get_game_id(headers: dict, game_id: str, max_attempts: int):
    if not game_id:
        game_id = f"{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}c{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}-b{randint(1, 9)}e{randint(1, 9)}-{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}f-a{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}-a{randint(1, 9)}e{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}f{randint(1, 9)}b{randint(1, 9)}a"
    print(Fore.YELLOW + Style.BRIGHT + "Trying to get a game id......")
    # create a random game id
    url = "https://game-domain.blum.codes/api/v1/game/play"
    data = {
        "gameId": game_id
    }
    for attempt in range(max_attempts):
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            return response.json()['gameId']
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(3)

    failed_request["get game id"] = False
    print(Fore.LIGHTRED_EX + "Failed to get game id!")
    return False


def game_claim_points(headers, game_id, max_attempts: int):
    print(Fore.YELLOW + Style.BRIGHT + "Trying to claim points......")
    points = randint(230, 250)
    url = "https://game-domain.blum.codes/api/v1/game/claim"
    data = {
        "gameId": game_id,
        "points": points
    }
    for attempt in range(max_attempts):
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(Fore.LIGHTGREEN_EX + "Successful!")
            print(Style.BRIGHT + Fore.LIGHTWHITE_EX + f"{response.text} : {points} points")
            time.sleep(1)
            return
        else:
            print(Fore.LIGHTBLACK_EX + f"Error: status code {response.status_code}")
            print(Fore.LIGHTBLACK_EX + "Attempting to reconnect")
            time.sleep(0.4)

    print(Fore.LIGHTRED_EX + "Failed to earn points!")
    return


def game(account_info: dict, headers: dict):
    global failed_request
    playPasses = account_info["playPasses"]
    if playPasses == 0:
        return False
    game_id = ""
    for _ in range(playPasses):
        game_id = get_game_id(headers, game_id, 3)
        if game_id:
            time.sleep(30.5)
            game_claim_points(headers, game_id, 3)
        else:
            time.sleep(2)
            return True

    return True


def automation():
    try:
        user_folder = os.path.expanduser("~")
        tokens_file_path = os.path.join(user_folder, "refresh_tokens.json")

        print_name()
        clear_console()
        time.sleep(1)

        data = get_refresh_token(tokens_file_path)
        if not data:
            return

        tokens = data[0]
        tokens_names = list(tokens.keys())
        account_names = data[1]

        print(Style.BRIGHT + Fore.LIGHTWHITE_EX  + f"Available accounts: {' '.join(account_names)}")
        time.sleep(1)
        StrExcludedAccounts = input(Fore.LIGHTCYAN_EX  + "Which accounts to exclude from the automation list?: ")
        ExcludeAccounts = StrExcludedAccounts.split()

        for i in range(len(tokens_names)):
            name = tokens[tokens_names[i]][0]
            if name in ExcludeAccounts:
                continue
            clear_console()
            print(Fore.BLUE + Style.BRIGHT + f"The account begins: {name}\n")
            if tokens[tokens_names[i]][1] == "refresh":
                access_token = get_access_tokens(tokens_names[i], name, tokens_file_path, 4)
            else:
                access_token = tokens_names[i]

            if not access_token:
                print(Fore.LIGHTRED_EX + f"Failed to get access account token {name} . Try again later!")
                continue

            headers = {
                "Authorization": f"Bearer {access_token}",
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
                "accept": "application/json, text/plain, */*",
                "origin": "https://telegram.blum.codes"
            }

            if not get_daily_reward(headers, 2):
                print(Fore.LIGHTMAGENTA_EX + "The daily reward has already been received!")
            account_info: dict = get_account_info(headers, 3)
            if not account_info:
                continue
            time.sleep(1)
            farm(account_info, headers)
            status = game(account_info, headers)
            if not status:
                print(Fore.LIGHTMAGENTA_EX + "The number of tickets is 0!")

            friends_claim_points(headers, 1)
            if not failed_request["claim farm"]:
                account_info = get_account_info(headers, 3)
                farm(account_info, headers)
            elif not failed_request["start farm"]:
                farming_start(headers, 3)
            elif not failed_request["get game id"]:
                get_account_info(headers, 3)
                game(account_info, headers)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
        return

