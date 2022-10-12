# Container technology

A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. [^1]

Containers are a solution to the problem of how to get software to run reliably when moved from one computing environment to another. For example, containers can be used to export the training of a ML model from your local machine to a HPC server without the strain of installing all the dependancies necessary to run the training. Think of a container as a shipping container for software — it holds important content like files and programs so that an application can be delivered efficiently from producer to consumer.

To create and use *containers* the use of a *container platform* is necessary. **Docker** is the most popular but others exist such as [podman](https://podman.io/) for instance. On the other hand, **Docker** and similar have some limitations which makes it difficult to use on HPC clusters and more powerful platform such as [Singularity](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html) are necessary.

## Docker



## Singularity





[^1]: Definition from [docker.com](https://www.docker.com/resources/what-container/)