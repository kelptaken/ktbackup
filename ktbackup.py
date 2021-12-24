# Local Backup Tool
# by @kelptaken --- 24.12.21

### --- PREPARING --- ###

global isHaloAvailable
global source
global destination

import os
import sys
import shutil
import socket
import getpass
import datetime
import traceback
import filecmp
import platform
import pathlib
import time
import json

"""
jfile = open('Dest/Amebus/ktbackup.json', 'r')  
bebra = jfile.read()                            
bebruskins = json.loads(bebra)                         For my nasty purposes :)
print(bebruskins["ameba"])
exit()
"""
try:
    from halo import Halo
    isHaloAvailable = True
    backupSpinnerAnim = {
    'interval': 300,
    'frames': ['[-----]', '[#----]', '[-#---]', '[--#--]', '[---#-]', '[----#]']
}
    backupSpinner = Halo(text='Backing up...', spinner=backupSpinnerAnim)
    restoreSpinner = Halo(text='Restoring', spinner=backupSpinnerAnim)
except BaseException:
    isHaloAvailable = False

# Variables
try:
    source = sys.argv[1]
    destination = sys.argv[2]
    name = sys.argv[3]
    username = getpass.getuser()
    hostname = socket.gethostname()
    o_system = platform.system()
    datapath = f'{destination}/{name}/Data'
    bkpath = f'{destination}/{name}'
except IndexError:
    print('! No arguments passed.')
    print('- Usage:')
    print('autobackup.py <source> <destination> <backupname {auto}>')
    exit()

# Functions ---

# Compare two folder destination. Proudly copied from Stack Overflow (https://stackoverflow.com/questions/4187564/recursively-compare-two-directories-to-ensure-they-have-the-same-files-and-subdi)
def compare(dir1, dir2):
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if len(dirs_cmp.left_only)>0 or len(dirs_cmp.right_only)>0 or \
        len(dirs_cmp.funny_files)>0:
        return False
    (_, mismatch, errors) =  filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)
    if len(mismatch)>0 or len(errors)>0:
        return False
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not compare(new_dir1, new_dir2):
            return False
    return True


# Check that the source and destination are fine
def runChecks(source, destination):
    # Check if source exists
    if os.path.exists(source) == True:
        print('- Source exists.')
    elif os.path.exists(source) == False:
        exit('! Backup source does not exist. Exiting.')
    else:
        exit('! Caught "else" statement while checking existence of source. Exiting.')
    
    # Check if destination exists
    if os.path.exists(destination) == True:
        print('- Destination exists.')
    elif os.path.exists(destination) == False:
        print('- Destination does not exist, creating folder.')
        os.mkdir(destination)
    else:
        exit('! Caught "else" statement while checking existence of destination. Exiting.')

    # Check if source = directory
    if os.path.isfile(source) == True:
        exit('! Source is a file. It should be a directory. Exiting.')
    elif os.path.isfile(source) == False:
        print('- Source is a directory.')
    else:
        exit('! Caught "else" statement while checking source type. Exiting.')

    # Check if destination = directory
    if os.path.isfile(destination) == True:
        exit('! Destination is a file. It should be a directory. Exiting.')
    elif os.path.isfile(destination) == False:
        print('- Destination is a directory.')
    else:
        exit('! Caught "else" statement while checking source type. Exiting.')

    # Check if source = destination. I don't know how this code works, I literally wrote it while sleeping
    if compare(source, destination) == True:
        if len(os.listdir(source)) == 0:
            print('- Source is empty.')
            if len(os.listdir(destination)) == 0:
                print('- Destination is empty.')
        else:
            if source != destination:
                try:
                    print('! Content in source and destination is the same, deleting destination')
                    shutil.rmtree(destination)
                    os.mkdir(destination)
                except PermissionError:
                    exit('! Unable to delete destination (Permission denied). Exiting.')
            exit("! Source and destination can't be the same directory. Exiting.")
    elif compare(source, destination) == False:
        print('- Source and destination are different.')
    else:
        exit('! Caught "else" statement while comparing source and destination.')
    
    print('- All checks passed.')


# Get raw size of folder
def get_size(folder: str) -> int:
    return sum(p.stat().st_size for p in pathlib.Path(folder).rglob('*'))


# Convert raw size to human-readable
def filesize(size: int) -> str:
     for unit in ("B", "K", "M", "G", "T"):
         if size < 1024:
             break
         size /= 1024
     return f"{size:.1f}{unit}"


# Create backup folder structure
def createStructure(source, destination):
    print('- Creating directory structure...')
    os.makedirs(datapath)
    jsonFileContent = {
        'name': str(name),
        'creator': f'{username}@{hostname}/{o_system}',
        'size': f'{filesize(get_size(source))}',
        'date': str(datetime.date.today())
        }
    jsonFile = open(f'{bkpath}/ktbackup.json', 'w')
    json.dump(jsonFileContent, jsonFile)



# Backup
def backup(source, destination, name, username, hostname):
    print('\n' + name)
    print('======')
    print(f'Creator: {username}@{hostname}/{o_system}')
    print(f'Size: {filesize(get_size(source))}')
    print(f'Date: {datetime.date.today()}')

    createStructure(source, destination)

    if isHaloAvailable == True:
        backupSpinner.start()
        shutil.copytree(source, datapath, dirs_exist_ok=True)
        backupSpinner.stop_and_persist()
        print('Done!')
    
    elif isHaloAvailable == False:
        print('/ Backing up...')
        shutil.copytree(source, datapath, dirs_exist_ok=True)
        print('Done!')
    else:
        print('! Caught "else" statement while checking Halo availability. Not using Halo.')
        print('/ Backing up...')
        shutil.copytree(source, datapath, dirs_exist_ok=True)
        print('Done!')


# Restore
def restore(source, destination):
    print('- Checking backup...')
    if os.path.exists(f'{source}/ktbackup.json'):
        print('- ktbacakup.json exists')
    else:
        exit('! ktbackup.json does not exist. Exiting.')

    if os.path.exists(f'{source}/Data'):
        print('- Data exists')
    else:
        exit('! Data does not exist. Exiting.')

    if os.path.exists(destination):
        print('- Destination exists')
    else:
        print('- Destination does not exist, creating a folder')
        os.mkdir(destination)

    if os.path.isfile(destination):
        exit('! Destination cannot be a file. Exiting.')
    else:
        print('- Destination is a folder.')

    print('- Fetching backup data...')

    jsonFile = open(f'{source}/ktbackup.json')
    jsonFIleR = jsonFile.read()
    jsonData = json.loads(jsonFIleR)

    name = jsonData["name"]
    creator = jsonData["creator"]
    size = jsonData["size"]
    date = jsonData["date"]

    print('\n' + name)
    print('======')
    print(f'Creator: {creator}')
    print(f'Size: {size}')
    print(f'Date: {date}')

    restoreSpinner.start()
    shutil.copytree(f'{source}/Data', destination, dirs_exist_ok=True)
    restoreSpinner.stop_and_persist()
    print('Done!')


print(f'- KTBackup vALPHA-0.1 on {username}@{hostname}/{o_system}')
if sys.argv[1] != '--restore':
    runChecks(source, destination)
    backup(source, destination, name, username, hostname)
else:
    print('- Entering restore mode.')
    source = sys.argv[2]
    destination = sys.argv[3]
    restore(source, destination)
