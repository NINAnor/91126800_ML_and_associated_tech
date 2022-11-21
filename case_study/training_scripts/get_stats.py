import argparse
import torch
import json
import glob
import os
import albumentations as A

from sklearn.metrics import auc, roc_curve

from torch.utils.data import DataLoader
from models.classicResNet import ResNet
from models.classicResNet import ResBlock
from utils.loader import ImgLoader


class GetStatModel():

    def __init__(self, data_path, model_path, to_save_json, batch_size):

        self.data_path = data_path
        self.model_path = model_path
        self.to_save_json = to_save_json
        self.batch_size = batch_size

        # Transform
        self.transform = self.initTransform()

        # Cuda
        self.is_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.is_cuda else "cpu")

        # model
        self.model = self.initModel()
        
        # related to metrics
        self.METRICS_SIZE = 3
        self.LABELS_NDX = 0
        self.PROBA_NDX = 1
        self.PREDICTED_NDX = 2

    def initModel(self):

        model = ResNet(num_layers=18, num_classes=2, image_channels=3, block=ResBlock)
        model.load_state_dict(torch.load(self.model_path))
        model.to(self.device)
        model.eval()
        
        return model

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

    def initDL(self):

        list_images = glob.glob(self.data_path + "/*.jpg")
        testset = ImgLoader(list_images, transform=self.transform)

        testLoader = DataLoader(testset,
                        batch_size = self.batch_size, 
                        shuffle=True,
                        pin_memory=self.is_cuda)

        return testLoader

    def do_preds(self, testLoader):

        metrics_mat = torch.zeros(self.METRICS_SIZE, len(testLoader.dataset), device=self.device)

        with torch.no_grad():
            for batch_ndx, tuple_ndx in enumerate(testLoader,0):

                # Get index for test_metrics
                start_ndx = batch_ndx * self.batch_size
                end_ndx = start_ndx + self.batch_size

                # Get images and labels to CPU or GPU
                imgs, labels = tuple_ndx
                imgs = imgs.permute(0,3,1,2)
                imgs = imgs.to(self.device)
                labels = labels.to(self.device)

                # Do the prediction
                outputs = self.model(imgs)

                # Get the predicted label (the category with the highest probability)
                _, predicted = torch.max(outputs, dim=1)

                # Fill up test_metrics for this batch
                metrics_mat[self.LABELS_NDX, start_ndx:end_ndx] = labels
                #metrics_mat[self.PROBA_NDX, start_ndx:end_ndx] = outputs
                metrics_mat[self.PREDICTED_NDX, start_ndx:end_ndx] = predicted

        return metrics_mat.to('cpu')

    def main(self):

        testLoader = self.initDL()
        metrics_mat = self.do_preds(testLoader)

        # Get accuracy
        correct = torch.eq(metrics_mat[self.LABELS_NDX], metrics_mat[self.PREDICTED_NDX]).sum()
        accuracy = correct / len(metrics_mat[self.LABELS_NDX])
        print(accuracy)
        
        # Write to a json compatible file
        stats = {'accuracy' : accuracy.item(),
                'model': 'ResNet50'}

        # Return value in a json file
        with open(self.to_save_json, 'w') as outfile:
            json.dumps(stats)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--data_path",
                        help="Path to the test dataset",
                        required=True,
                        type=str
    )

    parser.add_argument("--model_path",
                        help="Path to the model",
                        required=True,
                        type=str
    )

    parser.add_argument("--to_save_json",
                        help="Path to save the json file",
                        required=True,
                        type=str
    )

    parser.add_argument("--batch_size",
                        help="Batch size",
                        required=True,
                        type=int
    )

    cli_args = parser.parse_args()

    GetStatModel(cli_args.data_path,
                cli_args.model_path,
                cli_args.to_save_json,
                cli_args.batch_size).main()


