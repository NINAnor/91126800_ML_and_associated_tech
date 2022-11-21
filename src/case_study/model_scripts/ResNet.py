import torch 
import torch.nn as nn
import torch.nn.functional as F

class ResBlock(nn.Module):
    def __init__(self, num_layers, in_channels, out_channels, identity_downsample=None, stride=1):
        # the assert statement is used to continue the execute if the given condition evaluates to True. 
        # If the assert condition evaluates to False, then it raises the AssertionError exception with the specified error message.
        assert num_layers in [18, 34, 50, 101, 152], "should be a a valid architecture"

        super(ResBlock, self).__init__()

        # In the ResNet > 34, the number of channels in the 3rd convolution is 4 times the number
        # of channels of the second one.
        self.num_layers = num_layers
        if self.num_layers > 34:
            self.expansion = 4
        else:
            self.expansion = 1

        # ResNet50, 101, and 152 include additional layer of 1x1 kernels
        # See the forward function
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)
        self.bn1 = nn.BatchNorm2d(out_channels)
        
        if self.num_layers > 34:
            self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        else:
            # for ResNet18 and 34, connect input directly to (3x3) kernel (skip first (1x1))
            self.conv2 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)

        self.bn2 = nn.BatchNorm2d(out_channels)
        self.conv3 = nn.Conv2d(out_channels, out_channels * self.expansion, kernel_size=1, stride=1, padding=0)
        self.bn3 = nn.BatchNorm2d(out_channels * self.expansion)

        # RELU function
        self.relu = nn.ReLU()

        # conv layer that we will do to the identity mapping so it has the same shape as the other layers
        self.identity_downsample = identity_downsample

    def forward(self, x):

        identity = x

        if self.num_layers > 34:
            x = self.conv1(x)
            x = self.bn1(x)
            x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.conv3(x)
        x = self.bn3(x)

        # We use the layer if we need to change the shape
        if self.identity_downsample is not None:
            identity = self.identity_downsample(identity)

        x += identity
        x = self.relu(x)
        return x

class ResNet(nn.Module):
    def __init__(self, num_layers, image_channels, num_classes, block):

        assert num_layers in [18, 34, 50, 101, 152], f'ResNet{num_layers}: Unknown architecture! Number of layers has ' \
                                                     f'to be 18, 34, 50, 101, or 152 '
        super(ResNet, self).__init__()

        if num_layers < 50:
            self.expansion = 1
        else:
            self.expansion = 4

        if num_layers == 18:
            layers = [2, 2, 2, 2]
        elif num_layers == 34 or num_layers == 50:
            layers = [3, 4, 6, 3]
        elif num_layers == 101:
            layers = [3, 4, 23, 3]
        else:
            layers = [3, 8, 36, 3]

        # For ALL ResNet, the first layer is a convolution of stride 7 with 64 output channels
        self.in_channels = 64
        self.conv1 = nn.Conv2d(image_channels, 64, kernel_size=7, stride=2, padding=3)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()

        # This first layer is followed by a maxpool of stride 2 and kernel of 3
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # ResNetLayers
        self.layer1 = self.make_layers(num_layers, block, layers[0], intermediate_channels=64, stride=1)
        self.layer2 = self.make_layers(num_layers, block, layers[1], intermediate_channels=128, stride=2)
        self.layer3 = self.make_layers(num_layers, block, layers[2], intermediate_channels=256, stride=2)
        self.layer4 = self.make_layers(num_layers, block, layers[3], intermediate_channels=512, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(512 * self.expansion, 1000)
        self.fc2 = nn.Linear(1000, 512)
        self.fc_out = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.reshape(x.shape[0], -1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc_out(x)
        return x

    def make_layers(self, num_layers, block, num_residual_blocks, intermediate_channels, stride):

        layers = []

        # In the paper the identity downsample is a conv layer
        identity_downsample = nn.Sequential(nn.Conv2d(self.in_channels, intermediate_channels*self.expansion, kernel_size=1, stride=stride),
                                            nn.BatchNorm2d(intermediate_channels*self.expansion))

        # This is the layer that changes the number of channels
        # If we look at the first ResNet layer, it's going to change 64 to 256
        # The downsample is ONLY for the first block, then it's just a normal identity 
        # mapping
        layers.append(block(num_layers, self.in_channels, intermediate_channels, identity_downsample, stride))

        # Then we need to update in_channels!
        self.in_channels = intermediate_channels * self.expansion # 256

        for i in range(num_residual_blocks - 1):
            layers.append(block(num_layers, self.in_channels, intermediate_channels)) # At the end of the first block
            # we will have 256 channels (in_channels here) and out_channels will be 64. 

        return nn.Sequential(*layers)
