# Templates

## 3. Running scripts on Sigma2

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
