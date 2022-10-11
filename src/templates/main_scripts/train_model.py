# Libraries
import argparse
import torch
import datetime
import glob
import numpy as np
import random
import torch.optim as optim
import torch.nn as nn
import albumentations as A
import os

from PIL import Image
from torch.utils.data import DataLoader
from model_scripts.ResNet import ResNet
from model_scripts.ResNet import ResBlock

from utils.loader import ImgLoader
from utils.earlystopping import EarlyStopping

class trainingApp():

    def __init__(self, data_path, save_path, save_es, batch_size, lr, num_epochs):

        self.data_path = data_path
        self.save_path = save_path
        self.save_es = save_es
        self.batch_size = batch_size
        self.lr = lr
        self.num_epochs = num_epochs

        # related to system
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

        # Transform
        self.transform = self.initTransform()

        # early stopping
        self.patience = 7

        # Cuda
        self.is_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.is_cuda else "cpu")

        # Related to model
        self.model = self.initModel()
        self.optimizer = self.initOptimizer()
        self.criterion = nn.CrossEntropyLoss()

    def initModel(self):

        model = ResNet(num_layers=18, num_classes=2, image_channels=3, block=ResBlock)
        model.to(self.device)
        return model

    def initOptimizer(self):

        return optim.SGD(self.model.parameters(), lr=self.lr, momentum=0.9)

    def initTransform(self):

        transform = A.Compose(
            [
                A.SmallestMaxSize(max_size=260),
                A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=15, p=0.5),
                A.RandomCrop(height=224, width=224),
                A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.5),
                A.RandomBrightnessContrast(p=0.5),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ]
        )

        return transform

    def trainingLoop(self):

        # Prepare the dataset
        list_images = glob.glob(self.data_path + "/*.jpg")

        # Make a training and testing set
        train_images = random.sample(list_images, int(len(list_images) * 0.8))
        test_images = [item for item in list_images if item not in train_images]

        trainset = ImgLoader(train_images, transform=self.transform)
        testset = ImgLoader(test_images, transform=self.transform)

        trainLoader = DataLoader(trainset,
                                batch_size = self.batch_size, 
                                shuffle=True,
                                pin_memory=self.is_cuda)

        testLoader = DataLoader(testset,
                                batch_size = self.batch_size, 
                                shuffle=True,
                                pin_memory=self.is_cuda)

        # early stopping call
        early_stopping = EarlyStopping(patience=self.patience, path=self.save_es, verbose=True)

        # Train the network
        for epoch in range(self.num_epochs):  # loop over the dataset multiple times

            training_loss = 0.0
            val_loss = 0.0
            nb_train_batch = 0
            nb_val_batch = 0

            for i, data in enumerate(trainLoader, 0):
                # get the inputs; data is a list of [inputs, labels]
                imgs, labels = data
                imgs = imgs.permute(0,3,1,2)

                # Imgs and labels to GPU if possible
                imgs = imgs.to(self.device)
                labels = labels.to(self.device)

                # zero the parameter gradients
                self.optimizer.zero_grad()

                # forward + backward + optimize
                outputs = self.model(imgs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                training_loss += loss.item()
                nb_train_batch += 1

            with torch.no_grad():
                for i, data in enumerate(testLoader,0):
                    imgs, labels = data
                    imgs = imgs.permute(0,3,1,2)

                    # Imgs and labels to GPU if possible
                    imgs = imgs.to(self.device)
                    labels = labels.to(self.device)

                    # forward + backward + optimize
                    outputs = self.model(imgs)
                    loss = self.criterion(outputs, labels)

                    val_loss += loss.item()
                    nb_val_batch += 1

            t_loss = training_loss / nb_train_batch
            v_loss = val_loss / nb_val_batch

            print("Epoch: {}, Training loss: {}, Validation loss: {}".format(epoch, training_loss / nb_train_batch, val_loss / nb_val_batch))

            # Add the mean loss of the val for the epoch
            early_stopping(v_loss, self.model)

            if early_stopping.early_stop:
                print("Early stopping")
                break

        # Save the model
        print('Finished Training')
        torch.save(self.model.state_dict(), self.save_path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--data_path",
                        help="Path to the folder containing the data (train and test set will be sampled)",
                        required=True,
                        type=str
    )

    parser.add_argument("--save_path",
                        help="Number of epochs to train the model on",
                        required=True,
                        type=str
    )

    parser.add_argument("--save_es",
                        help="Path to early stopping checkpoints",
                        required=True,
                        type=str
    )

    parser.add_argument("--batch_size",
                        help="Batch size",
                        required=True,
                        type=int
    )

    parser.add_argument("--lr",
                        help="Learning rate",
                        required=True,
                        type=float
    )

    parser.add_argument("--num_epochs",
                        help="Number of epochs to train the model on",
                        required=True,
                        type=int
    )

    cli_args = parser.parse_args()

    trainingApp(cli_args.data_path, 
    cli_args.save_path, 
    cli_args.save_es, 
    cli_args.batch_size, 
    cli_args.lr, 
    cli_args.num_epochs).trainingLoop()
