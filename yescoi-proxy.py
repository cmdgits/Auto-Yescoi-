import requests
import time
from colorama import Fore, Style, init
import json
import random

init(autoreset=True)

def print_welcome_message():
    print(r"""
          
█▀▀ █▀▄▀█ █▀▄ █▀▀ █ ▀█▀ █▀
█▄▄ █░▀░█ █▄▀ █▄█ █ ░█░ ▄█
          """)
    print(Fore.GREEN + Style.BRIGHT + "YesCoin (Gold) BOT")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://github.com/cmdgits/Auto-Yescoi-")


# Load tokens from file
def load_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

# Load proxies from file
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

available_colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

# Define headers
def get_headers(token):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.yescoin.gold',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.yescoin.gold/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

# Use proxy for requests
def get_random_proxy(proxies):
    proxy = random.choice(proxies)
    return {
        'http': proxy,
        'https': proxy,
    }

def collect_coin(token, amount, proxies):
    url = 'https://api.yescoin.gold/game/collectCoin'
    headers = get_headers(token)
    data = json.dumps(amount)
    proxy = get_random_proxy(proxies)

    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxy)
        response.raise_for_status()
        result = response.json()

        if result['code'] == 0:
            return result
        else:
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as e:
        print(f"Error collecting coins: {e}")
        return None

def fetch_account_info(token, proxies):
    url = 'https://api.yescoin.gold/account/getAccountInfo'
    headers = get_headers(token)
    proxy = get_random_proxy(proxies)

    try:
        response = requests.get(url, headers=headers, proxies=proxy)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching account info: {e}")

# Similar modifications for other API calls to include proxy handling

# Example: Fetching game info
def fetch_game_info(token, proxies):
    url = 'https://api.yescoin.gold/game/getGameInfo'
    headers = get_headers(token)
    proxy = get_random_proxy(proxies)

    try:
        response = requests.get(url, headers=headers, proxies=proxy)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching game info: {e}")

# Example main function using tokens and proxies
def main():
    print_welcome_message()
    tokens = load_tokens('tokens.txt')
    proxies = load_proxies('proxy.txt')

    for token in tokens:
        print(f"Processing token: {token}")
        account_info = fetch_account_info(token, proxies)
        if account_info:
            print(f"Account info: {account_info}")
        else:
            print("Failed to fetch account info")

        # Collect coins example
        game_info = fetch_game_info(token, proxies)
        if game_info:
            amount = game_info['data']['coinPoolLeftCount'] // game_info['data']['singleCoinValue']
            collect_coin(token, amount, proxies)

        time.sleep(2)  # Delay between requests

if __name__ == "__main__":
    main()

