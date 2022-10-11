# File management on Sigma2

### 2.3. Copy files over to Sigma2

**A very important command** is `scp` which allows you to copy files from your machine to the HPC machines. For instance you want to copy the script `train_model.py` over to `saga` in the folder `deepexperiments`, the command would be (using your relevant username and HPC):

```
$ scp train_model.py bencretois@saga.sigma2.no:/deepexperiments/
```

With `scp` it is also possible to copy a folder over to the HPC machine, you will need to add the flag `-r` for this. For instance, if I want to copy the entire `deepexperiments` folder over to `saga` I can write:

```
$ scp -r train_model.py bencretois@saga.sigma2.no:/deepexperiments/
```

### 2.4. Synchronizing your local repository with your remote repository

Instead of copying all files from your local to remote folder you can synchronze the two folders with `rsync`

```
$ rsync -e ssh -avz ./local_repo user@server:/remote_repo
```

`-a` is the archive option, i.e. syncs directories recursively while keeping permissions, symbolic links, ownership, and group settings. 

`-v` being the verbose option and prints the progress and status of the rsync command.

`-z` compressing files during the transfer - speed up the sync.

`-e` is used to specify the remote shell to use, `ssh` in our case.

It is also possible to use the option `--exclude` to exclude some file from synchronisation:

```
$ rsync -e ssh -avz --exclude "file.txt" ./local_repo user@server:/remote_repo
```

However, in some cases there are files that we do not want to send to the remote repository. In these cases with can generate and `.txt` file containing a list of files to exclude.

```
$ rsync -e ssh -avz --exclude-from{"list_ignore.txt"} ./local_repo user@server:/remote_repo
```

With `list_ignore.txt`:

```
folder1
file1.txt
folder2
```



```
def doConnection(connection_string):

    myfs = fs.open_fs(connection_string)
    return myfs
```



```
def walk_audio(filesystem, input_path):
    # Get all files in directory with os.walk
    walker = filesystem.walk(input_path, filter=['*.wav', '*.flac', '*.mp3', '*.ogg', '*.m4a', '*.WAV', '*.MP3'])
    for path, dirs, flist in walker:
        for f in flist:
            yield fs.path.combine(path, f.name)
```


```
def parseInputFiles(filesystem, input_path):

    files = []

    for index, audiofile in enumerate(walk_audio(filesystem, input_path)):
        files.append(audiofile)
            
    print('Found {} files for training'.format(len(files)))

    return files
```
