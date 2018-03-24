#!/bin/bash

CHATID=""
TOKEN=""
TIME="10"
URL="https://api.telegram.org/bot$TOKEN/sendMessage"
TEXT="$1"

curl -s --max-time $TIME -d "chat_id=$CHATID&disable_web_page_preview=1&text=$TEXT" $URL >/dev/null
