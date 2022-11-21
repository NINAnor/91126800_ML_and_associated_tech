# Training model on SIGMA2

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