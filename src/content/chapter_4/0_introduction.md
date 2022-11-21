# Case study: training a cat / dog classifier

In this section we will demonstrate how to train a cat and dog classifier using supercomputers and in particular SIGMA2.

## Data 

The case study is entirely reproducible and you can run it yourself provided you have an account on SIGMA2. 

The data to run this case study can be found on [Kaggle](https://www.kaggle.com/competitions/dogs-vs-cats/data?select=train.zip), a subsidiary of Google that allow users to find and publish data sets, explore and build models in a web-based data-science environment, work with other data scientists and machine learning engineers, and enter competitions to solve data science challenges. The training dataset is composed of 25,000 images of dogs and cats and weight approximatively about 500MB.a 

## Code 

All the scripts are found in the GitHub repository of this book, under `case_study`. The folder contains three subfolders:

- **bash_scripts**: contains all the bash scripts which are not to be ran on HPC.
- **hpc_scripts**: contains all the bash scripts to be run on HPC.
- **model_scripts**: All the python scripts necessary to train the model.

The folder also contains a `Dockerfile` which will be used for creating `docker container`.
