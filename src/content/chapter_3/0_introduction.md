# File management on HPC clusters

In addition to training a machine learning model we usually want to process our data on an HPC cluster to benefit the computational resources. For example, if we want to train a complex machine learning model we want the HPC cluster to first process our data so we get **tensors** so they can be used as inputs for the model. **Using the data requires being able to access them**.

There are two ways of making the data available to the HPC cluster:

1. Copying the data over to the HPC cluster
2. Using a **filesystem** to make remote data available to the HPC cluster

## Copying the data over to the HPC cluster

Both methods have their advantages and drawbacks. While copying data over to the HPC cluster is conceptually simpler as it doesn't require the use of any specific library, the method will be limited by the size of the dataset. By default, if you apply for an account on one of Sigma2's HPC clusters you will be allocated **1 TB** of storage that can be extended up to **10TB**. Moreover, copying multiple TB of data can be a **long process**.

## Using a **filesystem** to make remote data available to the HPC cluster

On the other hand, using **filesystems** allows you to use data stored in a remote server (e.g. cloud storage, private servers ...) in the HPC cluster and abstract the need of having storage memory in the HPC cluster. **Filesystems** nevertheless require slight change in your code.




