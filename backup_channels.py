# backup_channels.py
# Backup list of channels subscription fromn account to simple text file
import argparse
from open_session import open_session


def backup_channels(client, session_name):
    filename = session_name+'_channel_list'
    with open(filename, 'w') as file_object:
        for dialog in client.iter_dialogs():
            if dialog.is_channel:  # Process channels only
                if dialog.entity.username is None:
                    print(dialog.title+" channel with no username!\n")
                else:
                    file_object.write(dialog.entity.username+"\n")


def main():
    print("Backup list of channels subscription from account")
    parser = argparse.ArgumentParser()
    parser.add_argument("session_name")
    args = parser.parse_args()
    client = open_session(args.session_name)
    print("---- processing ----")
    backup_channels(client, args.session_name)


if __name__ == "__main__":
    main()
