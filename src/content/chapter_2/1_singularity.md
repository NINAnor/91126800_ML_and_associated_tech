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

It is possible to push your custom image directly in the **GitLab** or **GitHub** registry. 

#### Pushing the image on GitLab registry

Pushing the image on the **Gitlab** registry requires less manual configuration and we give an example on how to do it below.

Provided that you have a GitLab account and a GitLab project (in our example the project is called `ml_image`) for your specific task, the image should be rename as:

```
registry.gitlab.com/nina-data/ml_image:latest
```

We rename the image to provide an url to the registry where the image should be stored. Once the image has been pushed, you can check `GitLab project -> Container registry`


#### Pushing the image on GitHub registry

In your project repository create a folder `.github/workflows` and create a file `publish_image.yml` containing the following code:

```
name: Create and publish a Docker image

on:
  push:
    branches: main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push-image:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Log in to the Container registry
        uses: docker/login-action@f054a8b539a109f9f41c372932f1ae047eff08c9
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@98669ae865ea3cffbcbaa878cf57c20bbf1c6c38
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push Docker image
        uses: docker/build-push-action@ad44023a93711e3deb337508980b4b5e9bcdc5dc
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

Once the folder and file have been created simply **push** the `.github` to the project's GitHub repository and **GitHub Actions** will take care of building and hosting the image.

Note that you will find the image in `Packages` (right sidebar of GitHub) and that you will need to make your image **public** before being able to pull it on **Sigma2**.


### 4. Pull the image as a `.sif` file from a HPC cluster

To pull the image that is stored on Gitlab, Docker hub or GitHub registry simply run:

```
singularity pull docker://registry/name_of_your_image
```

For instance, to pull the image from this repository (which is hosted on GitHub):

```
 singularity pull docker://ghcr.io/ninanor/91126800_ml_and_associated_tech:main
```