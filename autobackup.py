# Local Backup Tool
# by @kelptaken --- 24.12.21

### --- PREPARING --- ###

global isHaloAvailable

import os, sys, shutil, socket, getpass, datetime, traceback, filecmp, platform
try:
    from halo import Halo
    isHaloAvailable = True
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
        print('- Source does not exist, creating folder.')
        os.mkdir(source)
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

    # Check if source = destination
    if compare(source, destination) == True:
        if len(os.listdir(source)) == 0:
            print('- Source is empty.')
            if len(os.listdir(destination)) == 0:
                print('- Destination is empty.')
        else:
            exit("! Source and destination can't be the same directory. Exiting.")
    elif compare(source, destination) == False:
        print('- Source and destination are different.')
    else:
        exit('! Caught "else" statement while comparing source and destination.')
    
    print('- All checks passed.')


# Backup
def backup(source, destination, name, username, hostname):
   print('\n' + name)
   print('======')
   print()


print(f'- KTBackup vALPHA-0.1 on {username}@{hostname}/{o_system}')
runChecks(source, destination)
backup(source, destination, name, username, hostname)