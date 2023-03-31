#!/bin/bash
app_folder=$(dirname $(dirname $(realpath $0)))
python3.10 $app_folder/main.py
