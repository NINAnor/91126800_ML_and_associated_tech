import albumentations as A
import numpy as np
import torch


from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder
from PIL import Image

class ImgLoader(Dataset):
    def __init__(self, files, transform=None, filepath=False):
        self.files = files 
        self.transform = transform
        self.samples = []
        self.class_encode = LabelEncoder()
        self._init_dataset()
        self.filepath = filepath

    def __getLabels__(self):
        return self.class_encode.classes_

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):

        # Process the image
        img_path, label = self.samples[idx]
        pil_img = Image.open(img_path)
        img = np.array(pil_img)

        # Transform the image
        if self.transform is not None:
            img = self.transform(image=img)["image"]

        #img = img.transpose(2,0,1)

        # Process the labels
        label_encoded = self.one_hot_sample(label)
        label_class = torch.argmax(label_encoded)

        if self.filepath:
            return (img, label_class, img_path)
        else:
            return (img, label_class)

    def _init_dataset(self):

        labels = []

        for file in self.files:
            # Get the label of the image:
            label = file.split("/")[-1].split(".")[0]
            # Add the label to the folder recording the labels
            labels.append(label)
            # Append image path + label
            self.samples.append((file, label))

        self.class_encode.fit(list(labels))

    def to_one_hot(self, codec, values):
        value_idxs = codec.transform(values)
        return torch.eye(len(codec.classes_))[value_idxs]

    def one_hot_sample(self, label):
        t_label = self.to_one_hot(self.class_encode, [label])
        return t_label