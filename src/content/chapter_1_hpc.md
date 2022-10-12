## 1. An introduction to HPC

### 1.1. What is HPC and why using it?

**High performance computing** (HPC) generally refers to processing complex calculations at high speeds across multiple servers in parallel. Those groups of servers are known as clusters and are composed of **hundreds or even thousands of compute servers** that have been connected through a network. 

With the increased use of technologies like the Internet of Things (IoT), artificial intelligence (AI), and machine learning (ML), organizations are producing huge quantities of data, and they need to be able to process and use that data more quickly in real-time. To power the analysis of such large dataset it is often more practical / mandatory to make use of supercomputing. Supercomputing enables fast processing of data and training of complex algorithms such as neural networks for image and sound recognition.

### 1.2. What is Uninett Sigma2?

Sigma2 is a **non-profit** company that provides services for high-performance computing and data storage to individuals and groups involved in research and education at all Norwegian universities and colleges, and other publicly funded organizations and projects (such as NINA). Their activities are financed by the **Research Council of Norway (RCN)** and the **Sigma2 consortium partners**, which are the universities in Oslo, Bergen, Trondheim and Tromsø. This collaboration goes by the name **NRIS – Norwegian research infrastructure services**. 

Sigma2 owns **four High Performance Computing (HPC) servers** that have different configurations: `Betsy`, `Saga`, `Fram` and `LUMI`. Generally, if a project requires access to one or more **Graphics processing units** (GPUs) it is reasonable to apply for an access to `Saga`.

To apply for access to one of Sigma2 HPC please refer to [this page](https://www.sigma2.no/apply-e-infrastructure-resources). You will need to fill out a form describing your project, your experience with HPC and your computational needs (amount of CPU / GPU memory and storage your project will need).

For help regarding the application process contact [Benjamin Cretois](mailto:benjamin.cretois@nina.no), [Kjetil Grun](mailto:kjetil.grun@nina.no) or [Francesco Frassinelli](mailto:francesco.frassinelli@nina.no).


### 1.3. Getting started with Sigma2

After a successful application to an account on Sigma2 you will be given your **username** and will be able to log on the HPC terminal.

To access the HPC server you applied for (in our case it is `saga`). You can log in using the command `ssh` in **Windows PowerShell** or on a **linux terminal**: 

```bash
$ ssh username@saga.sigma2.no
```

The first time you log in, you will be asked to set your **password** which will have to be used at any subsequent connection to the HPC server.


## 2. Navigating in Sigma2's HPC server

### 2.1 bash crash course

Communication between you and the HPC server is usually done through an interface named a `bash` and no **Graphical User Interface (GUI)** is provided

Here is how the bash looks like

```
[bencretois@login-5.SAGA ~]$ 
```

Communicating with a bash requires learning a particular programming language, **bash scripting**. Below we provide a list of selected commands that will allow you to navigate in HPC server:


#### Change directory

**Command:**

* `cd + path to the directory` 

**Output:**

```
[bencretois@login-5.SAGA ~]$ cd deepexperiments/
[bencretois@login-5.SAGA ~/deepexperiments]$
```

#### Get to the previous directory

**Command:**

* `cd ..` -> get to the previous directory

**Output:**

```
[bencretois@login-5.SAGA ~/deepexperiments]$ cd ..
[bencretois@login-5.SAGA ~]$
```

#### List the content of a directory

**Command:**

* `ls` + name of a directory - Note that `ls` by default list the files of your current directory 

**Output:**

```
[bencretois@login-5.SAGA ~/deepexperiments]$ ls

bash_cheatsheet.md   Dockerfile             list_ignore.txt  poetry.lock     runs            sync.sh
bayesianfy.ipynb     docker_run_jupyter.sh  models           pyproject.toml  scripts         utils
deepexperiments.sif  jobs
```

#### get the path of your current directory

**Command:**

* `pwd` 

**Output:**

```
[bencretois@login-5.SAGA ~]$ pwd
/cluster/home/bencretois
```

#### Create a new folder

**Command:**


* `mkdir` + name of the folder you want to create

**Output:**
 
```
[bencretois@login-5.SAGA ~]$ mkdir new_folder
[bencretois@login-5.SAGA ~]$ ls
deepexperiments new_folder
```

#### Learning more bash commands

*Bash command** are very well documented on Internet and if you wish to learn more you can begin [here](https://www.educative.io/blog/bash-shell-command-cheat-sheet).


### 2.2. Bash commands specific to Sigma2's HPC

There are also some useful commands specific to your Sigma2 account:


#### List your projects

**Command:**

`projects` -> list your projects

**Output:**

```
[bencretois@login-5.SAGA ~]$ projects
nn5019k
```

#### Look at used space and allocated quota for your projects

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








