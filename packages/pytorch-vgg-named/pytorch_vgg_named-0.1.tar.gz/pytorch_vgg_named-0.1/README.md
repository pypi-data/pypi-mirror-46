# Named VGG Feature Extractors

The networks provided here are the same as in `torchvision.models.vgg`, but
they are built differently, so that you can extract lists of features in a
single call like this: 

```python3
r11, r31, r51 = net.forward(targets=['relu1_1', 'relu3_1', 'relu5_1'])
```

This is mostly useful for applications in Neural Style Transfer, where we often
want to query sets of features from a network.

## License

The files in this project are derived from the [pytorch](https://github.com/pytorch/pytorch/) repository and are published under the same BSD-style license.
