# What is Uninett Sigma2?

Sigma2 is a **non-profit** company that provides services for high-performance computing and data storage to individuals and groups involved in research and education at all Norwegian universities and colleges, and other publicly funded organizations and projects (such as NINA). Their activities are financed by the **Research Council of Norway (RCN)** and the **Sigma2 consortium partners**, which are the universities in Oslo, Bergen, Trondheim and Tromsø. This collaboration goes by the name **NRIS – Norwegian research infrastructure services**. 

Sigma2 owns **four High Performance Computing (HPC) servers** that have different configurations: `Betsy`, `Saga`, `Fram` and `LUMI`. Generally, if a project requires access to one or more **Graphics processing units** (GPUs) it is reasonable to apply for an access to `Saga`.

To apply for access to one of Sigma2 HPC please refer to [this page](https://www.sigma2.no/apply-e-infrastructure-resources). You will need to fill out a form describing your project, your experience with HPC and your computational needs (amount of CPU / GPU memory and storage your project will need).

For help regarding the application process contact [Benjamin Cretois](mailto:benjamin.cretois@nina.no), [Kjetil Grun](mailto:kjetil.grun@nina.no) or [Francesco Frassinelli](mailto:francesco.frassinelli@nina.no).


# Getting started with Sigma2

After a successful application to an account on Sigma2 you will be given your **username** and will be able to log on the HPC terminal.

To access the HPC server you applied for (in our case it is `saga`). You can log in using the command `ssh` in **Windows PowerShell** or on a **linux terminal**: 

```bash
$ ssh username@saga.sigma2.no
```

The first time you log in, you will be asked to set your **password** which will have to be used at any subsequent connection to the HPC server.
