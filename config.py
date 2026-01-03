import os
import json


#####################################
######### General

BOT_TOKEN: str = str(os.getenv("BOT_TOKEN"))

#####################################
######### Messages

with open('message.json', 'r') as f:
    _msgs = json.load(f)

WELCOME_MSG: str = _msgs["welcome"]
UNRECOGNIZED_LINK: str = _msgs["unrecognized_link"]
DOWNLOADING_START: str = _msgs["downloading_start"]
FILE_NOT_FOUND: str = _msgs["file_not_found"]
EMPTY_FILE: str = _msgs["empty_file"]
ERROR_DOWNLOADING: str = _msgs["error_downloading"]