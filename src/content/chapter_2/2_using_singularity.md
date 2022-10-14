# Interact with images

Now that the `.sif` file has been **pulled**, it is possible to interact with it via multiple ways.

## Shell

The `shell` command allows you to spawn a new bash **within your container** and interact with it as though it were a small virtual machine.

```
[bencretois@login-1.SAGA ~]$ singularity shell 91126800_ml_and_associated_tech_main.sif
Singularity>
```

The change in prompt indicates that you have entered the container. Once inside of a Singularity container, you are the same user as you are on the host system **except that you have root access, meaning that you can install packages and other software in your container**.

Note that with **singularity**, when you are inside of a Singularity container, you are the same user as you are on the host system.

```
Singularity> whoami
bencretois
```

## Executing commands

The `exec` command allows you to execute a custom command within a container by specifying the image file. For instance, if I want to train a Machine Learning model using the `.sif` image we could write:

```
singularity exec \
                91126800_ml_and_associated_tech_main.sif \
                python main_scripts/train_model.py
```

## Specifying bind paths

If the data we want to process / use to train a machine learning model are stored in a different folder (for instance our `.sif` file is in `cluster/projects/nn8055k` but the data is in `cluster/projects/nn8054k`) we need to expose `cluster/projects/nn8054k` or in other words, make it available to the container. The flag `--bind` fill that purpose. 

We would run the container as follow:

```
singularity exec \
                --bind /cluster/projects/nn8054k \
                91126800_ml_and_associated_tech_main.sif \
                python main_scripts/train_model.py
```

## Exposing GPUs

When training or using a machine learning model it will usually be preferable to use a GPU(s) for accelerating the processed. The container being an "isolated" environment, it is required to specify that we want to expose GPUs to our container. This can simply be done by adding the flag `--nv`. For example:

```
singularity exec \
                --nv \
                91126800_ml_and_associated_tech_main.sif \
                python main_scripts/train_model.py
```