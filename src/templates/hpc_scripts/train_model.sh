#!/bin/bash

#SBATCH --account=nn5019k --job-name=cat_dog_model
#SBATCH --partition=accel --gpus=1
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=4G

cd /cluster/home/bencretois/ml-sats/case_study_1

for LR in 0.01 0.001 0.0001
do
singularity exec --bind /cluster/projects/nn5019k:/Data \
    --nv case_study_1.sif \
    python -u main_scripts/train_model.py \
                --data_path /Data/kaggle_cats_dogs/train \
                --save_path /Data/saved_models/model.pt \
                --save_es /Data/saved_models/model_es.pt \
                --batch_size 128 \
                --lr $LR \
                --num_epoch 10
done

