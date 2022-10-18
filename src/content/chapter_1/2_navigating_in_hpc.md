# Navigating in Sigma2's HPC server

## Basic bash commands

Communication between you and the HPC server is usually done through an interface named a `bash` and no **Graphical User Interface (GUI)** is provided

Here is how the bash looks like

```
[bencretois@login-5.SAGA ~]$ 
```

Communicating with a bash requires learning a particular programming language, **bash scripting**. Below we provide a list of selected commands that will allow you to navigate in HPC server:


### Change directory

**Command:**

* `cd + path to the directory` 

**Output:**

```
[bencretois@login-5.SAGA ~]$ cd deepexperiments/
[bencretois@login-5.SAGA ~/deepexperiments]$
```

### Get to the previous directory

**Command:**

* `cd ..` -> get to the previous directory

**Output:**

```
[bencretois@login-5.SAGA ~/deepexperiments]$ cd ..
[bencretois@login-5.SAGA ~]$
```

### List the content of a directory

**Command:**

* `ls` + name of a directory - Note that `ls` by default list the files of your current directory 

**Output:**

```
[bencretois@login-5.SAGA ~/deepexperiments]$ ls

bash_cheatsheet.md   Dockerfile             list_ignore.txt  poetry.lock     runs            sync.sh
bayesianfy.ipynb     docker_run_jupyter.sh  models           pyproject.toml  scripts         utils
deepexperiments.sif  jobs
```

### get the path of your current directory

**Command:**

* `pwd` 

**Output:**

```
[bencretois@login-5.SAGA ~]$ pwd
/cluster/home/bencretois
```

### Create a new folder

**Command:**


* `mkdir` + name of the folder you want to create

**Output:**
 
```
[bencretois@login-5.SAGA ~]$ mkdir new_folder
[bencretois@login-5.SAGA ~]$ ls
deepexperiments new_folder
```

### Learning more bash commands

*Bash command** are very well documented on Internet and if you wish to learn more you can begin [here](https://www.educative.io/blog/bash-shell-command-cheat-sheet).


## Bash commands specific to Sigma2's HPC

There are also some useful commands specific to your Sigma2 account:


### List your projects

**Command:**

`projects` -> list your projects

**Output:**

```
[bencretois@login-5.SAGA ~]$ projects
nn5019k
```

### Look at used space and allocated quota for your projects

**Command:**

`dusage` -> . Note that **space used** is what you are currently using and **quota** is the limit. 

**Output:**

```
[bencretois@login-5.SAGA ~]$ dusage

dusage v0.1.4
                          path    backup    space used     quota    files      quota
------------------------------  --------  ------------  --------  -------  ---------
                      /cluster        no       5.6 GiB         -   38 819          -
      /cluster/home/bencretois       yes       4.6 GiB  20.0 GiB    1 311    100 000
/cluster/work/users/bencretois        no       0.0 KiB         -        0          -
     /cluster/projects/nn5019k       yes     938.2 MiB   1.0 TiB   37 508  1 000 000

```
