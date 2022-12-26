import os
import sys
import requests
import subprocess

# Specify path
base_dir_path = '../yolov7/'
pt_path = base_dir_path + 'yolov7.pt'

isExist = os.path.exists(base_dir_path)
isDir = os.path.isdir(base_dir_path)

yoloDirectoryOk = isExist and isDir
if not yoloDirectoryOk:
    sys.exit()

print(base_dir_path, "found")


# download checkpoint
checkptExist = os.path.exists(pt_path)
if not checkptExist:
    print("download checkpoint...")
    pt_url = 'https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt'
    r = requests.get(pt_url, allow_redirects=True)
    open(pt_path, 'wb').write(r.content)
else:
    print(pt_path, "found")


print("install required packaged")
subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "-r", base_dir_path+"requirements.txt"])
