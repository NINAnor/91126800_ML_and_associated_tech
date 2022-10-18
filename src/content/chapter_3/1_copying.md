# Copying files over to an HPC cluster

It is possible to copy / transfer files using simple **bash** commands. `scp` is used to simply **copy** data over while `rsync` is used to **synchronise** folders.

## `scp`: Copying files

The first command  is `scp` which allows you to copy files from your machine to the HPC machines. For instance you want to copy the script `train_model.py` from the **template** folder over to `saga` in the project folder **nn8055k**, we would write (using your relevant username and HPC):

```
$ scp train_model.py bencretois@saga.sigma2.no:/cluster/projects/nn8055k/
```

With `scp` it is also possible to **copy a folder** over to the HPC machine, you will need to add the flag `-r` for this. For instance, if I want to copy the entire `template` folder over to `saga` I can write:

```
$ scp -r template bencretois@saga.sigma2.no:/cluter/projects/nn8055k
```

## `rsync`: Synchronizing a local repository with a remote repository

Instead of copying all files from your local to remote folder you can synchronze the two folders with `rsync`. Synchronizing has the advantage of being more flexible than `scp` and has some optimisations to make the transfer of files faster. Moreoever `rsync` has a plethora of command line options, allowing the user to fine tune its behavior. It supports complex filter rules, runs in batch mode, daemon mode, etc. 

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

With `list_ignore.txt` looking like:

```
folder1
file1.txt
folder2
```