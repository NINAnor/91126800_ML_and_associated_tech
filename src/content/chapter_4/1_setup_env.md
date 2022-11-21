# Setting up the environment

## Virtual environments versus containers

Two choices are offered to set up the environment: **virtual environments** and **containers**. We will demonstrate how we can train the cat / dog classifier using both methods.

## Conda setup

WORK IN PROGRESS

## Container setup

On the other hand it might be a good idea to set up a container. Because we have not **root** access on SIGMA2's HPC we have to build a Singularity container by first having a Docker container which is specified using a **Dockerfile**. Let's analyse the Dockerfile of this specific case study line by line:

- First we install python version 3.8 in our container so we can use up to date python libraries 

```bash
FROM python:3.8
```

- Avoid the system asking questions / dialogs during the `apt-get` install

```bash
ARG DEBIAN_FRONTEND=noninteractive
```

- Update `apt-get` to have up to date packages

```bash
RUN \
    apt-get update && \
    rm -rf /var/lib/apt/lists/*
```

- Install the package manager `poetry`. Note that you can install your preferred package manager such as `conda` in this step.

```bash
RUN pip3 install poetry 
```

- Set the working directory of the container

```bash
WORKDIR /app
```

- The next three lines are specific to `poetry`. Basically we copy both the `pyproject.toml` (file containing the packages we use for our analysis) and `poetry.lock` (file containing all the dependancies). Then we remove the creation of the virutal environment so that `python` in our container uses all our package without opening a virtual environment. Finally we install our packages.

```bash
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
```

- Copy all the files of the folder where we open the container

```bash
COPY . ./
```

- Set the python path to the working directory. This way the `main_scripts` can access the scripts in the other folders (for instance the `utils` scripts).

```bash
ENV PYTHONPATH "${PYTHONPATH}:/app/"
```

## 2 - Creating the docker image

The `Dockerfile` being defined we can now create our image (i.e. the "environment" in which we will run the training script). For open a terminal, move to the folder where your `Dockerfile` is located and write the following command (change `case_study_1` to the name of your folder):

`docker run -t case_study_1:latest -f Dockerfile .`

The command should output the following:

```bash
Sending build context to Docker daemon  244.7kB
Step 1/10 : FROM python:3.8
 ---> 271c1bcd4489
Step 2/10 : ARG DEBIAN_FRONTEND=noninteractive
 ---> Using cache
 ---> 0965e91032c6
Step 3/10 : RUN     apt-get update &&     rm -rf /var/lib/apt/lists/*
 ---> Using cache
 ---> 02fa21122354
Step 4/10 : RUN pip3 install poetry
 ---> Using cache
 ---> 33bbd2c53863
Step 5/10 : WORKDIR /app
 ---> Using cache
 ---> 7720e687da9c
Step 6/10 : COPY pyproject.toml poetry.lock ./
 ---> Using cache
 ---> 345244b7ba43
Step 7/10 : RUN poetry config virtualenvs.create false
 ---> Using cache
 ---> 47271847855f
Step 8/10 : RUN poetry install --no-root
 ---> Using cache
 ---> 67e487ef8ae6
Step 9/10 : COPY . ./
 ---> c7656f1447fa
Step 10/10 : ENV PYTHONPATH "${PYTHONPATH}:/app/"
 ---> Running in 9f82e9b70fc5
Removing intermediate container 9f82e9b70fc5
 ---> b08815df7070
Successfully built b08815df7070
Successfully tagged case_study_1:latest
```

Indicating that the image has been successfully created.
