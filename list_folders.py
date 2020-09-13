# list_folders.py
# List chat folders (filters) from account
import argparse
from telethon import functions
from open_session import open_session


def list_folders(client, session_name):
    chat_folders = client(functions.messages.GetDialogFiltersRequest())
    for chat_folder in chat_folders:
        print(chat_folder.stringify())


def main():
    print("# List chat folders (filters) from account")
    parser = argparse.ArgumentParser()
    parser.add_argument("session_name")
    args = parser.parse_args()
    client = open_session(args.session_name)
    list_folders(client, args.session_name)


if __name__ == "__main__":
    main()
