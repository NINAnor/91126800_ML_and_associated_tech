# Job script basics

To run a job on the cluster involves creating a shell script called a **job script**. The job script is a plain-text file containing any number of commands, including your main computational task.

## Anatomy of a job script

A job script consists of a couple of parts, in this order:

- The first line, which is typically `#!/bin/bash` (the Slurm script does not have to be written in Bash, see below)
- Parameters to the queue system (specified using the tag `#SBATCH`)
- Commands to set up the execution environment
- The actual commands you want to be run

Note that lines starting with a `#` are ignored as comments, except lines that start with `#SBATCH` and the **shebang** (i.e. `#!/bin/bash`), which are not executed, but contain special instructions to the queue system. There can be as many `#SBATCH` as you want. Moreover, the `#SBATCH` lines must precede any commands in the script.

### SBATCH parameters

Which parameters are allowed or required depends the job type and cluster, but two parameters must be present in (almost) any job:

- **--account**: specifies the project the job will run in. Required by all jobs.
- **--time**: specifies how long a job should be allowed to run. If it has not finished within that time, it will be cancelled.

Other parameters that you will use on HPCs such as `SAGA`, `Betzy` or `Fram` include:

- **ntasks**: specifies the number of tasks to run on a node
- **cpus-per-task**: allocate a specific number of CPUs to each task
- **--mem-per-cpu**: allocate a specific amount of memory per CPU and per task
- **--partition**: 

And more rarely (if you have a very expensive task to run):

- **--nodes**: number of nodes required
- **--ntasks-per-node**: number of processes or tasks to run on a single node

### Module load

The **module system** is a concept available on most supercomputers, simplifying the use of different software (versions) in a precise and controlled manner. In most cases, an HPC has far more software installed than the average user will ever use and it would not been computationally efficient to have them loaded by default.

Note that with the use of container, you do not need the module system as all the different softwares should be built in your image. See [Chapter 2](./chapter_2/0_introduction_containers.md).

To get a list of available packages you can use:

```
module avail
```

To load a module into your environment to start using an application you can use:

```
module load package
```

For instance, if you want to load `Pytorch v. 1.4.0` with `python 3.7.4` use:

```
PyTorch/1.4.0-fosscuda-2019b-Python-3.7.4
```

## Example 1:

```bash
#SBATCH --account=nnXXX
#SBATCH --job-name=Run_ML_model
#SBATCH --nodes=2
#SBATCH --time=1:0:0
#SBATCH --mem-per-cpu=4G
#SBATCH --ntasks=8 --cpus-per-task=10 --ntasks-per-node=4
```

This job will get 2 nodes, and run 4 processes (tasks) on each of them, each process is getting 10 cpus with 4GB of memory. The wall-time is 1 hours so each task will be able to compute for a maximum of 1 hour.


## Example 3, a generic script:

```bash

#!/bin/bash

# Job name:
#SBATCH --job-name=YourJobname
#
# Project:
#SBATCH --account=nnXXXXk
#
# Wall time limit:
#SBATCH --time=DD-HH:MM:SS
#
# Other parameters:
#SBATCH ...

## Set up job environment:
set -o errexit  # Exit the script on any error
set -o nounset  # Treat any unset variables as an error

module --quiet purge  # Reset the modules to the system default
module load SomeProgram/SomeVersion
module list

## Do some work:
YourCommands



```