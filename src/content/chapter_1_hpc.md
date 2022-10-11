# High Performance Clusters (HPC)

## 1. Description of SIGMA2 and how to apply for an account

### 1.1. What is SIGMA2?

Sigma2 is a **non-profit** company that provides services for high-performance computing and data storage to individuals and groups involved in research and education at all Norwegian universities and colleges, and other publicly funded organizations and projects (such as NINA). Their activities are financed by the **Research Council of Norway (RCN)** and the **Sigma2 consortium partners**, which are the universities in Oslo, Bergen, Trondheim and Tromsø. This collaboration goes by the name **NRIS – Norwegian research infrastructure services**. 

Sigma2 owns four High Performance Computing (HPC) servers that have different capabilities: `Betsy`, `Saga`, `Fram` and `LUMI`. Generally, at NINA we do not conduct extremely intensive computational tasks (compared to an AI lab for instance) and if we want access to one or multiple GPUs it is reasonable to apply for an access to `Saga`.

To apply for access to one of Sigma2 HPC please refer to [this page](https://www.sigma2.no/apply-e-infrastructure-resources). You will need to fill out a form describing your project, your experience with HPC and your computational needs (amount of CPU / GPU memory and storage your project will need).

For some help regarding the application process contact [Benjamin Cretois](mailto:benjamin.cretois@nina.no), [Kjetil Grun](mailto:kjetil.grun@nina.no) or [Francesco Frassinelli](mailto:francesco.frassinelli@nina.no).

### 1.2. The role of Sigma2 in the ML workflow

While most of the scripting for building efficient machine learning pipeline and algorithms is be done locally (on your own NINA laptop or on the Linux Virtual Desktop made available by Datahjelp, VDI), Sigma2 supercomputers can help being more efficient at training / using the machine learning models.

Machine learning algorithms and particularly deep learning algorithms are much faster trained wth Graphical Processing Units (GPUs) as GPUs are very efficient at parallelizing processes. Sigma2's computers have multiple GPUs available that we can "borrow" for our computation tasks - this is specified in a **job** script as we will see later. Sigma2 makes it possible to train multiple ML models at the same time for instance, making it possible to fine tune specific parameters and variables relatively quickly.

Sigma2 should thus be used when our scripts related to machine learning already work on the VDI (or on your local computer) and you would like to fine-tune your model's parameters or ultimately to train your machine learning model on the entire dataset you have.

### 1.3. Getting started with Sigma2

After a successful application to an account on Sigma2 you will be able to access the HPC facility you applied for (in our case it is `saga`). You can log in using the command `ssh` in Windows PowerShell or on a linux terminal: 

```bash
$ ssh username@saga.sigma2.no
```

Note that if you have access to another HPC facility, you have to replace `saga` in the command describe above.


## 2. Basic commands on Sigma2

### 2.1 Beginner bash

Once you are logged in the HPC you should only see a dry, unwelcoming interface named a `shell`. Navigating on a computer through a shell can be quite combersome as it works through commands only, there is no real visual apart from the displayed text!

```
# Here is how the shell looks like
[bencretois@login-5.SAGA ~]$ 
```

To navigate in the HPC you will need to learn some `shell scripting`. Here is a quick list of command that will allow you to navigate in a Sigma2 supercomputer:


* `cd + path to the directory` -> change director

```
[bencretois@login-5.SAGA ~]$ cd deepexperiments/
[bencretois@login-5.SAGA ~/deepexperiments]$
```

* `ls` list the folder (i.e. the directory) in which you are

```
[bencretois@login-5.SAGA ~/deepexperiments]$ ls
bash_cheatsheet.md   Dockerfile             list_ignore.txt  poetry.lock     runs            sync.sh
bayesianfy.ipynb     docker_run_jupyter.sh  models           pyproject.toml  scripts         utils
deepexperiments.sif  jobs
```

* `cd ..` -> get to the previous directory

```
[bencretois@login-5.SAGA ~/deepexperiments]$ cd ..
[bencretois@login-5.SAGA ~]$
```

* `pwd` -> get the path of the current directory

```
[bencretois@login-5.SAGA ~]$ pwd
/cluster/home/bencretois
```

* `mkdir name_folder` -> create a folder named `name_folder`
 
```
[bencretois@login-5.SAGA ~]$ mkdir new_folder
[bencretois@login-5.SAGA ~]$ ls
deepexperiments new_folder
```


### 2.2. Bash commands specific to Sigma2

There are also some useful commands specific to your Sigma2 account:

`projects` -> list your projects

```
[bencretois@login-5.SAGA ~]$ projects
nn5019k
```

`dusage` -> look at the space used in your project folders. Note that **space used** is what you are currently using and **quota** is the limit. 

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





### 3 Running scripts on Sigma2

### 3.1. Anatomy of a job script

To run a job on a SIGMA2 server we need to create a shell script called a job script. The job script is a plain-text file containing any number of commands, including your main computational task


### 3.2. Description of job scripts

## Using docker on SIGMA2

1. Introduction to docker
1. Build your custom docker image
1. Introduction to singularity
1. Run your script in a docker container
 
## Machine learning workflow
 
1. Structuring the ML project

First of all, we need to differentiate the **development space** & the **data space**. Usually, HPCs allocate a large amount of disk storage capacity in a specific place (i.e. `/cluster/projects/` for SAGA) and a smaller amount of disk storage capacity to store the scripts used to run an analysis (i.e. `/cluster/home/`)

For instance, for this specific project (nn5019k) we have 20GB of space in `/cluster/home/bencretois` and 1TB in `/cluster/projects/nn5019k` as displayed with the command `dusage` below:

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


