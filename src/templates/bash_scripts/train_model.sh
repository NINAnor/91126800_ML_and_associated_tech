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