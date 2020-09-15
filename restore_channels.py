# restore_channels.py
# Restore channels subscription in destination account from simple text file
import argparse
from telethon.tl.functions.channels import JoinChannelRequest
from open_session import open_session


def restore_channels(client, session_name):
    filename = session_name+'_channel_list'
    with open(filename, 'r') as file_object:
        for line in file_object:
            print("Join @"+line.rstrip())
            chan_entity = client.get_entity(line.rstrip())
            dialog = client(JoinChannelRequest(chan_entity))


def main():
    print("Restore channels subscription in account from backup file")
    parser = argparse.ArgumentParser()
    parser.add_argument("session_name")
    args = parser.parse_args()
    client = open_session(args.session_name)
    print("---- processing ----")
    restore_channels(client, args.session_name)


if __name__ == "__main__":
    main()
