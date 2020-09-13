# open_session.py
# Open session file if exist and start Telegram client
import argparse
import json
from telethon import TelegramClient, sync


def open_session(session_name):
    config_filename = 'api.json'
    try:
        with open(config_filename, 'r') as f:
            api = json.load(f)
    except FileNotFoundError:
        input("Enter api_id")
        api = {
            'api_id' : input("Enter api_id") ,
            'api_hash' : input("Enter api_hash")
            }
        with open(config_filename, 'w') as f:
            json.dump(api, f)

    print(f"Connect to {session_name} session")
    client = TelegramClient(session_name, api['api_id'], api['api_hash'])
    client.start()
    print(f"Session {session_name} opened\n")
    print(f"Account is @{client.get_me().username}\n")
    return client


def main():
    print("Open session file if exist and start Telegram client")
    parser = argparse.ArgumentParser()
    parser.add_argument("session_name")
    args = parser.parse_args()
    client = open_session(args.session_name)


if __name__ == "__main__":
    main()
