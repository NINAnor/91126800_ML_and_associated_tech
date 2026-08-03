# Setting up the environment

## Virtual environments versus containers

Two choices are offered to set up the environment: **virtual environments** and **containers**. We will demonstrate how we can train the cat / dog classifier using both methods.

## Conda setup

WORK IN PROGRESS

## Container setup

On the other hand it might be a good idea to set up a container. Because we have not **root** access on SIGMA2's HPC we have to build a Singularity container by first having a Docker container which is specified using a **Dockerfile**. Let's analyse the Dockerfile of this specific case study line by line:

- We base our container on the official `uv` image which ships with python 3.12 so we can use up to date python libraries

```bash
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
```

- Copy the dependency files rather than resolving them again, which makes the install reproducible

```bash
ENV UV_LINK_MODE=copy

WORKDIR /app
```

- The next lines are specific to `uv`. We copy both the `pyproject.toml` (file containing the packages we use for our analysis) and `uv.lock` (file containing all the resolved dependencies) into the container. Then we install the packages while caching the downloaded wheels so that rebuilds are fast. The `--no-install-project` flag means we only install the dependencies at this stage, not the project itself.

```bash
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
```

- Copy all the files of the folder where we open the container

```bash
ADD . /app
```

- Now that the source files are in place, install the project itself so the `uv` environment contains everything we need

```bash
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen
```

- Set the python path to the working directory. This way the scripts can access the scripts in the other folders (for instance the `model_scripts` scripts).

```bash
ENV PYTHONPATH="/app"
```

## 2 - Creating the docker image

The `Dockerfile` being defined we can now create our image (i.e. the "environment" in which we will run the training script). Open a terminal, move to the folder where your `Dockerfile` is located and write the following command (change `case_study_1` to the name of your folder):

`docker build -t case_study_1:latest .`

The command should output the following:

```bash
Sending build context to Docker daemon  244.7kB
Step 1/7 : FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
 ---> 271c1bcd4489
Step 2/7 : ENV UV_LINK_MODE=copy
 ---> Using cache
 ---> 0965e91032c6
Step 3/7 : WORKDIR /app
 ---> Using cache
 ---> 7720e687da9c
Step 4/7 : RUN --mount=type=cache,target=/root/.cache/uv --mount=type=bind,source=uv.lock,target=uv.lock --mount=type=bind,source=pyproject.toml,target=pyproject.toml uv sync --frozen --no-install-project
 ---> Using cache
 ---> 47271847855f
Step 5/7 : ADD . /app
 ---> c7656f1447fa
Step 6/7 : RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen
 ---> Using cache
 ---> 67e487ef8ae6
Step 7/7 : ENV PYTHONPATH="/app"
 ---> Running in 9f82e9b70fc5
Removing intermediate container 9f82e9b70fc5
 ---> b08815df7070
Successfully built b08815df7070
Successfully tagged case_study_1:latest
```

Indicating that the image has been successfully created.
