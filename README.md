# KTBackup ALPHA
Local backup made easy, with Python and shutil

## Features
- One-command backup and restore
- Minimalistic (only using stdlib)
- Convenient directory structure

## Usage
#### Backup
```ktbackup.py <source> <destination> <backup name>```

A new folder with your backup name will be created in destination.
This folder will have two objects: `ktbackup.json` and `Data` folder.
`ktbackup.json` will contain information about your backup: name, creator (your computer username, hostname, and OS), creation date and size. This will be used when restoring.
`Data` will contain your source folder content.

#### Restore
```ktbackup.py --restore <source> <destination>```

Source is your backup folder (where Data and ktbackup.json are located).
**Destination will NOT contain Data and ktbackup.json, just your backup data.**

The script will read `ktbackup.json` and restore your files to destination.

*P. S. if Halo module is installed on your system (```pip install halo```), backing up and restoring will have a cool animation!*

## To do
- Add remote hosts support
