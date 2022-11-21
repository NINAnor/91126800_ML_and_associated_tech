# Training model locally

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