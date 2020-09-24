# mute_channels.py
# Mute all channels until 2038/01/01
import argparse
import datetime
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerNotifySettings, PeerNotifySettings
from open_session import open_session


def channel_is_muted(client, channel):
    chan = client(GetFullChannelRequest(channel))
    mute_until = chan.full_chat.notify_settings.mute_until
    if mute_until is None:
        return False
    else:
        return mute_until > datetime.datetime.now(tz=datetime.timezone.utc)


def mute_channels(client):
    for dialog in client.iter_dialogs():
        if dialog.is_channel:  # Process channels only
            if channel_is_muted(client, dialog):
                print(dialog.title+" channel is already muted")
                continue

            result = client(UpdateNotifySettingsRequest(
                peer=dialog,
                settings=InputPeerNotifySettings(
                    show_previews=False,
                    mute_until=datetime.datetime(2038, 1, 1),
                    sound=None
                    )
                ))

            if result:
                print(dialog.title+" channel is muted until 2038/01/01 !")
            else:
                print(dialog.title+" channel is skipped !")


def main():
    print("Backup list of channels subscription from account")
    parser = argparse.ArgumentParser()
    parser.add_argument("session_name")
    args = parser.parse_args()
    client = open_session(args.session_name)
    print("---- processing ----")
    mute_channels(client)


if __name__ == "__main__":
    main()
