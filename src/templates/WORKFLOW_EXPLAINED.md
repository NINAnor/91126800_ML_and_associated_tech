# Case study 1: cats and dogs classification

In this case study we are training a deep neural network (ResNet 18) to classify pictures of cats and dogs. We will not go through the scripts for training the model themselves but rather the workflow allowing us to train a model. First, we will dissect the `Dockerfile`, then 

## 1 - Setup your environment: the Dockerfile

When beginning a new ML project the first sensible thing to do is to build the **Dockerfile**. This way we have an "environment" that we can export elsewhere, allowing complete reproducibility of our analysis. Let's analyse the Dockerfile of this specific case study line by line.

- First we install python version 3.8 in our container so we can use up to date python libraries 

```
FROM python:3.8
```

- Avoid the system asking questions / dialogs during the `apt-get` install

```
ARG DEBIAN_FRONTEND=noninteractive
```

- Update `apt-get` to have up to date packages

```
RUN \
    apt-get update && \
    rm -rf /var/lib/apt/lists/*
```

- Install the package manager `poetry`. Note that you can install your preferred package manager such as `conda` in this step.

```
RUN pip3 install poetry 
```

- Set the working directory of the container

```
WORKDIR /app
```

- The next three lines are specific to `poetry`. Basically we copy both the `pyproject.toml` (file containing the packages we use for our analysis) and `poetry.lock` (file containing all the dependancies). Then we remove the creation of the virutal environment so that `python` in our container uses all our package without opening a virtual environment. Finally we install our packages.

```
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
```

- Copy all the files of the folder where we open the container

```
COPY . ./
```

- Set the python path to the working directory. This way the `main_scripts` can access the scripts in the other folders (for instance the `utils` scripts).

```
ENV PYTHONPATH "${PYTHONPATH}:/app/"
```

## 2 - Creating the docker image

The `Dockerfile` being defined we can now create our image (i.e. the "environment" in which we will run the training script). For open a terminal, move to the folder where your `Dockerfile` is located and write the following command (change `case_study_1` to the name of your folder):

`docker run -t case_study_1:latest -f Dockerfile .`

The command should output the following:

```
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

## 3 - Training the model locally (your computer or the VDI)

First of all, we should try to make sure that our scripts work well on the VDI before spending computational resources on SIGMA2. To develop and improve our scripts we can leverage the power of `Docker` by using the created image in two ways. 

First, we can start a `Jupyter` instance inside the docker container so you can develop in a more interactive environments while having all the python libraries you need. For this you can use the script `docker_start_jupyter` in `ml-sats/bash_utils`.

The script 

```
#!/bin/bash

cd ~/Code/deepexperiments

docker run \
    -p 8889:8889 \
    --rm -it \
    -v $PWD:/app \
    -v $HOME/Data:/Data \
    case_study_1:latest \
    poetry run jupyter lab \
    --port=8889 --no-browser --ip=0.0.0.0 --allow-root
~                                                        
```

You can also use the docker image to run the training script on any computers using the script `case_study_1/bash_scripts/train_model.sh`. Note that you need to change the folders that are exposed (for the meaning of exposed folder refer to the document XXX)

```
#!/bin/bash

# e: stop on error
# u : raises error if variable undefined
# -o pipefail: trigger error when command in the pipe fail
set -euo pipefail

cd $HOME/Code/case_study_1

DATA_PATH=/Data/train
OUT_DIR=/Data/

docker run --rm -v $HOME/Data:/Data -v $PWD:/app case_study_1:latest \
    python -u /app/main_scripts/train_model.py \
                --data_path $DATA_PATH \
                --save_path $OUT_DIR/model.pt \
                --save_es $OUT_DIR/model.pt \
                --batch_size 128 \
                --lr 0.001 \
                --num_epoch 10
```

We are finally ready to train the model. Since this is a test and the main model will be trained on SIGMA2 we run the model only for a few epoch to be sure the code does not contain any bug. Running the script (`./bash_scripts/train_model.sh`) should output the following:

```
benjamin.cretois@nixml086424q01:~/Code/ml-sats/case_study_1$ ./bash_scripts/train_model.sh 
./bash_scripts/train_model.sh: line 3: cd: /home/benjamin.cretois/Code/case_study_1: No such file or directory
/usr/local/lib/python3.8/site-packages/torch/nn/functional.py:718: UserWarning: Named tensors and all their associated APIs are an experimental feature and subject to change. Please do not use them for anything important until they are released as stable. (Triggered internally at  /pytorch/c10/core/TensorImpl.h:1156.)
  return torch.max_pool2d(input, kernel_size, stride, padding, dilation, ceil_mode)
Epoch: 0, Training loss: 0.6700030667766644, Validation loss: 0.6518245041370392
Validation loss decreased (inf --> 0.651825).  Saving model ...
Epoch: 1, Training loss: 0.6335798464003642, Validation loss: 0.6232574313879014
Validation loss decreased (0.651825 --> 0.623257).  Saving model ...
Epoch: 2, Training loss: 0.5948401207377196, Validation loss: 0.5763850644230842
Validation loss decreased (0.623257 --> 0.576385).  Saving model ...
Epoch: 3, Training loss: 0.553090987691454, Validation loss: 0.5323234401643276
Validation loss decreased (0.576385 --> 0.532323).  Saving model ...
Epoch: 4, Training loss: 0.5246088358627004, Validation loss: 0.5051904194056988
Validation loss decreased (0.532323 --> 0.505190).  Saving model ...
Epoch: 5, Training loss: 0.48994877194143405, Validation loss: 0.4672641947865486
Validation loss decreased (0.505190 --> 0.467264).  Saving model ...
Epoch: 6, Training loss: 0.4647162993242786, Validation loss: 0.45798871740698816
Validation loss decreased (0.467264 --> 0.457989).  Saving model ...
Epoch: 7, Training loss: 0.4354040877074952, Validation loss: 0.42637150436639787
Validation loss decreased (0.457989 --> 0.426372).  Saving model ...
Epoch: 8, Training loss: 0.4093162176335693, Validation loss: 0.41202530562877654
Validation loss decreased (0.426372 --> 0.412025).  Saving model ...
Epoch: 9, Training loss: 0.3919389988206754, Validation loss: 0.39200695902109145
Validation loss decreased (0.412025 --> 0.392007).  Saving model ...
Finished Training
```



## 4 - Pushing the image to the Gitlab repository

On SIGMA2 we cannot use our docker image immediately as it has been created on our local computer. As explained [here]() SIGMA2 uses `singularity` which is another software for handling images.

First we need to push our docker image to `GitLab` (we use `Gitlab` instead of `GitHub` as it is easier to handle docker images on `Gitlab`). This has to be done in 3 steps:

- First, be sure you are logged in the Gitlab registry:

```
docker login registry.gitlab.com
```

- Then we need to rename the docker image with regard to the `Gitlab` repository where it will be stored. For instance, the image we build `case_study_1:latest` will be stored in `registry.gitlab.com/nina-data/ml-sats/`, thus we need to rename the image as `registry.gitlab.com/nina-data/ml-sats/case_study_1:latest`:

```
docker tag case_study_1:latest registry.gitlab.com/nina-data/ml-sats/case_study_1:latest
```

- Then we can push the image to the `Gitlab` repository:

```
docker push registry.gitlab.com/bencretois/ml-sats/case_study_1:latest
```

# 5 - Training the model on SIGMA2

We first need to pull the image we stored on the Gitlab repository in our folder in SIGMA2. `singularity` uses `.sif` file so when we pull the image we need to relabel the image as a `.sif` file:

```
singularity pull --name case_study_1.sif docker://registry.gitlab.com/bencretois/ml-sats/case_study_1
```

Now that `case_study_1.sif` has been created in our folder we can train the model on SIGMA2 using the script `case_study_1/hpc_scripts/train_model.sh`. The script contains a few lines worth noticing:

- First the `shebang`, to tell the interpreter that this is a `bash` script

```
#!/bin/bash
```

- The SIGMA2 specific lines. Here we tell the HPC server that for running our script we need 1 GPU for a maximum of 24 hours. We also ask for a CPU with 4GB of memory.

```
#SBATCH --account=nn5019k --job-name=cat_dog_model
#SBATCH --partition=accel --gpus=1
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=4G
```

- We change our current directory to the directory where our scripts are located

```
cd $HOME/ml-sats/case_study_1
```

- Since we have 24 hours of GPU we run our script with three different learning rates. In this specific case the script will be ran 3 times in a consecutive fashion: once the script using the learning rate of 0.01 is finished, the script will be ran with a learning rate of 0.001. We will learn about parallelizing on SIGMA2 in case_study_2.

```
for LR in 0.01 0.001 0.0001
do
```

- Finally we set up the docker container for running the script `train_model.py` and specify all the relevant parameters. With singularity, by default only the working directory is exposed (in our case `$HOME/ml-sats`) so we need manually expose the folder where the the data is stored and where we want the model to be stored with the command `--bind`. Then with `python` we ask the docker container to use `python` to run the script `train_model.py`. The option `-u` is useful to display the printed text in the `.out` file.

```
singularity exec --bind /cluster/projects/nn5019k:/Data \
    --nv case_study_1.sif \
    python -u main_scripts/train_model.py \
                --data_path /Data/kaggle_cats_dogs/train \
                --save_path /Data/saved_models/model.pt \
                --save_es /Data/saved_models/model_es.pt \
                --batch_size 128 \
                --lr $LR \
                --num_epoch 100
done
```

- Now we can start the model training by submitting our script as a job with the command:

```
sbatch train_model.sh
```

# 6 (optional) - Importing the trained model locally

If we want to use our trained model on our own computer we can import the model using the command `scp`:

```
scp bencretois@sage.sigma2.no:/cluster/projects/nn5019k/saved_models/model.pt $HOME/Code/ml-sats/case_study_1
```

