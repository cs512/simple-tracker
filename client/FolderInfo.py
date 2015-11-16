#!/usr/bin/env python
import os
import hashlib

folder_info = {}
    
def getFolderInfo(folder):

    if not os.path.exists(folder):
        print("Path does not exist!")
        return folder_info

    if os.path.isfile(folder):
        print("This is a file!")
        return folder_info
        
    print(os.listdir(folder))
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        
        if os.path.isfile(itempath):
            file_sha = hashfile(itempath)
            file_size = os.path.getsize(itempath)
            folder_info.setdefault(itempath, {"sha":file_sha, "size":file_size, "src":"10.0.0.1"});
        elif os.path.isdir(itempath):
            getFolderInfo(itempath)
    return folder_info

def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

