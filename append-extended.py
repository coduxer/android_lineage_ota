#!/usr/bin/env python3
# Copyright 2021 Erfan Abdi
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import argparse
import os

import hashlib

def sha1sum(file_path):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha1 = hashlib.sha1()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()

def file_size_in_bytes(file_path):
    file_stats = os.stat(file_path)
    return file_stats.st_size


def add_new_ota(new_ota, json_file):
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            data = {"response": []}
            f.write(json.dumps(data, indent=4))
            
    with open(json_file, 'r+') as file:
        file_data = json.load(file)
        file_data["response"].insert(0, new_ota)
        file.seek(0)
        json.dump(file_data, file, indent=4)

    print("Done")
    
def create_new_ota(file_path, url, json_file):
    import re
    import os
    from datetime import datetime
    file_name = os.path.basename(file_path)
    file_props = re.match(r'(.+)-(.+)-(.+)-(.+)-(.+).zip', file_name)
    file_date = datetime.strptime(file_props.group(3), '%Y%m%d')
    #import ipdb; ipdb.set_trace()
    new_ota = {
                "datetime": int(file_date.timestamp()),
                "filename": file_name,
                "id": sha1sum(file_path),
                "romtype": file_props.group(4),
                "size": file_size_in_bytes(file_path),
                "url": url,
                "version": file_props.group(2)
            }
    add_new_ota(new_ota, json_file)
    print("Done")


if __name__ =='__main__':
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='OTA JSON Data appender')

    # Required positional argument
    parser.add_argument('ROM_FILE_PATH')
    parser.add_argument('ROM_FILE_URL')
    parser.add_argument('JSON_FILE')
    args = parser.parse_args()

    create_new_ota(args.ROM_FILE_PATH, args.ROM_FILE_URL, args.JSON_FILE)
