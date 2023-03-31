#!/bin/bash
script_folder=$(dirname $(realpath $0))
app_folder=$(dirname $(dirname $(realpath $0)))
web_dir="$app_folder/node_api/web_server/public"

python3.10 $script_folder/web_server.py --dir $web_dir
