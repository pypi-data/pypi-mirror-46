# Named VGG Feature Extractors

The networks provided here are the same (as in, the same weights and
everything) as in `torchvision.models.vgg`, but they are built differently, so
that you can extract lists of features in a single call like this: 

```python3
r11, r31, r51 = net.forward(targets=['relu1_1', 'relu3_1', 'relu5_1'])
```

This is mostly useful for applications in Neural Style Transfer, where we often
want to query sets of features from a network.
For this purpose, there is also a function `vgg19_normalized` which loads the
weights provided by Leon Gatys in his own implementation
[on github](https://github.com/leongatys/PytorchNeuralStyleTransfer).

## Installation

```console
pip install pytorch-vgg-named
```

## Usage

Use this like the regular `torchvision.models.vgg` module:

```python3
#! /urs/bin/env python3

import vgg_named
net = vgg_named.vgg19(pretrained=True).eval()
print(net)
# SequentialExtractor(
#   (conv1_1): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
#   (relu1_1): ReLU(inplace)
#   (conv1_2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
#   (relu1_2): ReLU(inplace)
#   (pool1): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
#   (conv2_1): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
#   (relu2_1): ReLU(inplace)
#   (conv2_2): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
#   (relu2_2): ReLU(inplace)
#   (pool2): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
#   [...]
#   (conv5_4): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
#   (relu5_4): ReLU(inplace)
#   (pool5): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
#   (AdaPool): AdaptiveAvgPool2d(output_size=(7, 7))
#   (flatten): Flatten()
#   (fc6): Linear(in_features=25088, out_features=4096, bias=True)
#   (relu_fc6): ReLU(inplace)
#   (drop_fc6): Dropout(p=0.5)
#   (fc7): Linear(in_features=4096, out_features=4096, bias=True)
#   (relu_fc7): ReLU(inplace)
#   (drop_fc7): Dropout(p=0.5)
#   (fc8): Linear(in_features=4096, out_features=1000, bias=True)
# )

# create a small batch of inputs
import torch
images = torch.randn(4, 3, 224, 224)

with torch.no_grad():
  # call like a regular vgg network
  fc8 = net.forward(images)

  # extract one specific set of features
  c42 = net.forward(images, targets='conv4_2')
  print(f'c42.shape = {c42.shape}')
  # c42.shape = torch.Size([4, 512, 28, 28])

  # extract a list of features. Note that the elements do not have to be in any
  # particular order. Duplicates are allowed too.
  r31, c31, po5, fc6 = net.forward(images, targets=['relu3_1', 'conv3_1', 'pool5', 'fc6'])
  print(f'r31.shape = {r31.shape}\n'
        f'c31.shape = {c31.shape}\n'
        f'po5.shape = {po5.shape}\n'
        f'fc6.shape = {fc6.shape}')
  # r31.shape = torch.Size([4, 256, 56, 56])
  # c31.shape = torch.Size([4, 256, 56, 56])
  # po5.shape = torch.Size([4, 512, 7, 7])
  # fc6.shape = torch.Size([4, 4096])

  # if you only need the first few layers and want to shave some MB of the GPU
  # memory, you can prune the network:
  net.prune('conv2_1')
  print(net)
  # SequentialExtractor(
  #   (conv1_1): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  #   (relu1_1): ReLU(inplace)
  #   (conv1_2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  #   (relu1_2): ReLU(inplace)
  #   (pool1): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  #   (conv2_1): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  # )
```

**For the normalized model only**, the preprocessing should be done like this:

```python
import torchvision.transforms as tvt
prep = tvt.Compose([tvt.ToTensor(),
                    # turn to BGR
                    tvt.Lambda(lambda x: x[torch.LongTensor([2,1,0])]), 
                    #subtract imagenet mean
                    tvt.Normalize(mean=[0.40760392, 0.45795686, 0.48501961],
                                  std=[1,1,1]),
                    # scale to expected input range
                    tvt.Lambda(lambda x: x.mul_(255))])
```

And postprocessing accordingly:

```python
postp = tvt.Compose([tvt.Lambda(lambda x: x/255), # don't use in-place
                      # add imagenet mean
                      tvt.Normalize(mean=[-0.40760392, -0.45795686, -0.48501961],
                                    std=[1,1,1]),
                      # turn to RGB
                      tvt.Lambda(lambda x: x[torch.LongTensor([2,1,0])]),
                      tvt.Lambda(lambda x: torch.clamp(x, 0, 1)),
                      tvt.ToPILImage()])
```

**For the standard VGG models, use the canonical pytorch normalization!**

## License

The files in this project are derived from the [pytorch](https://github.com/pytorch/pytorch/) repository and are published under the same BSD-style license.
