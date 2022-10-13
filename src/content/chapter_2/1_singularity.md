# Singularity

Singularity is a **container platform**. It allows you to create and run containers that package up pieces of software in a way that is portable and reproducible. You can build a container using Singularity on your laptop, and then run it on many of the largest HPC clusters in the world, local university or company clusters, a single server, in the cloud, or on a workstation down the hall. 

## Singularity Image Format file

**Singularity** uses **Singularity Image Format** (`.sif`) files to run containers. `sif` files can be built through two processes:

- Downloading pre-built images
- Building images from scratch

Building images from scratch require **root access** and since we do not have **root access** at NINA we need to rely on downloading pre-built images to build our `.sif` files.

## Downloading pre-built images as `.sif` files

It is possible to download images from the public image registries using **Singularity** using `singularity pull`. For instance, you can pull the [latest official python image from docker hub](https://hub.docker.com/_/python) on saga using the command:

```
singularity pull docker://python
```

The `docker://` uri is used to reference Docker images served from a registry. In this case `pull` does not just download an image file. Docker images are stored in layers, so `pull` combines those layers into a usable **Singularity file**.

I make sure that the images has been pulled:

```
[bencretois@login-1.SAGA ~]$ ls
python_latest.sif
```

## Downloading your own custom image

In most case you will want to use **an image that you built** so that the depencies required to run your custom software are already specified and installed. Since we do not have **root access** at NINA we follow the following workflow:

1. Specify a `Dockerfile`
2. Build the docker image
3. Push the docker image in a registry
4. Pull the image as a `.sif` file from a HPC cluster

Below we describe and provide an example for each step.

### 1. Specify a `Dockerfile`

We first write a `Dockerfile` containing all we need to run our software. In this case, we want to train a cat and dog picture classifier and we need to write the `Dockerfile` accordingly.

```
FROM python:3.8

ARG DEBIAN_FRONTEND=noninteractive

RUN pip3 install poetry 

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . ./

ENV PYTHONPATH "${PYTHONPATH}:/app/"
```

In this `Dockerfile` we first use the official image for python.3.8. 

Then we install [poetry](https://python-poetry.org/) (which is the python package manager) using `pip`. We recommand **poetry** over **anaconda** as we ran into some problems running **anaconda** with Docker. 

We set the working directory of the container as `/app`

We copy both `pyproject.toml` and `poetry.lock` in the container so that `poetry` knows which packages to install

We install the packages necessary to run our machine learning experiment

And finally we specify the `PYTHONPATH` so that scripts that are in certain folders can read the scripts which are stored in other folders.



### 2. Build the docker image

Building the docker image implies that `docker` is installed on your system. At NINA it is possible to install [Docker Desktop](https://www.docker.com/products/docker-desktop/) to use Docker on the remote server. Please contact Datahjelp which can assist you setting up either **Docker Desktop** or the **VDI** .

Once you have access to `docker` you can build your custom image using the command:

`docker build -t ml_image -f Dockerfile .`

`-t` stands for "tag", which is the name you want to give to the image.

`-f` stands for "file" and takes the `Dockerfile` as input.


### 3. Push the docker image in a registry




### 4. Pull the image as a `.sif` file from a HPC cluster

To pull the image that is stored on Gitlab, Docker hub or GitHub registry simply run:

```
singularity pull docker://ml_image
```