# telemigration.py
# Transferring channels subscription to another account
import time
from telethon import functions, types, errors
from telethon.tl.functions.channels import JoinChannelRequest
from open_session import open_session
from backup_channels import backup_channels

# Delay between requests for join
join_channel_request_delay = 20

print("Connect to source account")
source_client = open_session("source")
print("Connect to destination account")
destination_client = open_session("destination")

# Backup list of channels subscription fromn destination account to file
backup_channels(destination_client, "destination")
# Load backup file into list for skipping channels already joining
with open('destination_chanell_list') as file_object:
    existing_channels = file_object.readlines()
    existing_channels = [x.strip() for x in existing_channels]

print("---- processing channels ----")
for dialog in source_client.iter_dialogs():
    if dialog.is_channel:  # Process channels only
        if dialog.entity.username is None:
            print("Skip private channel: "+dialog.title)
        elif dialog.entity.username in existing_channels:
            print("Skip existing channel @"+dialog.entity.username.ljust(32) +
                  " -- "+dialog.title)
        else:
            try:
                print("Join @"+dialog.entity.username.ljust(32) +
                      " -- "+dialog.title)
                chan_entity = destination_client.get_entity(
                    dialog.entity.username
                    )
                destination_client(JoinChannelRequest(chan_entity))
                time.sleep(join_channel_request_delay)
            except errors.FloodWaitError as e:
                print('Must wait', e.seconds, 'seconds before last join')
                time.sleep(e.seconds+join_channel_request_delay)
                print("Join @"+dialog.entity.username.ljust(32)+" -- " +
                      dialog.title)
                chan_entity = destination_client.get_entity(
                    dialog.entity.username
                    )
                destination_client(JoinChannelRequest(chan_entity))
            except errors.ChannelPrivateError:
                print(f"The channel @{dialog.entity.username} specified is "
                      "private and you lack permission to access it. Another "
                      "reason may be that you were banned from it")

print("---- processing chat folders ----")
chat_folders = source_client(functions.messages.GetDialogFiltersRequest())
for chat_folder in chat_folders:
    res = destination_client(functions.messages.UpdateDialogFilterRequest(
        id=chat_folder.id,
        filter=chat_folder
        ))
