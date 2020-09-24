# leave_channels.py
# Leave channels, stored in *_channel_list file, from session account
import argparse
from telethon.tl.functions.channels import LeaveChannelRequest
from open_session import open_session


def leave_channels(client, session_name):
    filename = session_name+'_channel_list'
    with open(filename, 'r') as file_object:
        for line in file_object:
            print("Leaving @"+line.rstrip())
            chan_entity = client.get_entity(line.rstrip())
            client(LeaveChannelRequest(chan_entity))


def main():
    print("Leave channels from session account")
    parser = argparse.ArgumentParser()
    parser.add_argument("session_name")
    args = parser.parse_args()
    client = open_session(args.session_name)
    print("---- processing ----")
    leave_channels(client, args.session_name)


if __name__ == "__main__":
    main()
