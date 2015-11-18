#!/usr/bin/env python
import os
import hashlib

folder_info = []

def getfolderinfo(folder, root_uri, folder_ROOT):

    if not os.path.exists(folder):
        print("Path does not exist!")
        return folder_info

    if os.path.isfile(folder):
        print("This is a file!")
        return folder_info
        
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        
        if os.path.isfile(itempath):
            file_sha = hashfile(itempath)
            file_size = os.path.getsize(itempath)
            folder_info.append(
                {
                    "sha": file_sha,
                    "size": file_size,
                    "uri": root_uri+itempath[len(folder_ROOT):]})
        elif os.path.isdir(itempath):
            getfolderinfo(itempath, root_uri, folder_ROOT)
    return folder_info


def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

#a = getfolderinfo('/home/shaw/Develop/snlab/simple-tracker/client', 'http://192.168.1.1')
#print(a)
