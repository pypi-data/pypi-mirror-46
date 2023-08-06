import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from collections import OrderedDict
import torchvision.models.vgg as tvgg

from .sequential_extractor import SequentialExtractor

__all__ = [
    'VGG', 'vgg11', 'vgg11_bn', 'vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn',
    'vgg19_bn', 'vgg19', 'vgg19_normalized', 'VGG19_NORM_WEIGHTS'
]

VGG19_NORM_WEIGHTS = 'http://pascal.inrialpes.fr/data2/archetypal_style/vgg19_normalized_pytorch/vgg_conv_bethgelabs-35ec6ced.pth'

class Flatten(nn.Module):
  def forward(self, x):
    return x.view(x.size(0), -1)


def VGG(features, classifier,
        final_size=7, init_weights=True, **kwargs):
    seq = (features + 
           [('AdaPool', nn.AdaptiveAvgPool2d((final_size, final_size))),
            ('flatten', Flatten())] + 
           classifier)
    if init_weights:
      _initialize_weights(seq)
    return SequentialExtractor(OrderedDict(seq))

def _initialize_weights(modules):
    for _, m in modules:
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, 0, 0.01)
            nn.init.constant_(m.bias, 0)


def make_layers(cfg, batch_norm=False, relu_inplace=True):
    layers = []
    in_channels = 3
    b = 1
    l = 1
    for v in cfg:
        if v == 'M':
            layers += [(f'pool{b}', nn.MaxPool2d(kernel_size=2, stride=2))]
            b += 1
            l = 1
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [(f'conv{b}_{l}',conv2d), 
                           (f'bn{b}_{l}', nn.BatchNorm2d(v)),
                           (f'relu{b}_{l}', nn.ReLU(inplace=relu_inplace))]
            else:
                layers += [(f'conv{b}_{l}',conv2d), 
                           (f'relu{b}_{l}', nn.ReLU(inplace=relu_inplace))]
            in_channels = v
            l += 1
    return layers


def make_classifier(final_channels, final_size=7,
                    num_classes=1000, relu_inplace=True,
                    start_fc=6, num_fc=2, hidden=4096, **kwargs):
  fc_layers = list()
  dim_features = final_channels * final_size * final_size
  for i in range(start_fc, start_fc+num_fc):
    fc_layers += [(f'fc{i}', nn.Linear(dim_features, hidden)),
                  (f'relu_fc{i}', nn.ReLU(relu_inplace)),
                  (f'drop_fc{i}', nn.Dropout())]
    dim_features = hidden
  fc_layers += [(f'fc{start_fc+num_fc}', nn.Linear(dim_features, num_classes))]
  return fc_layers

cfg = {
  'A': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
  'B': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
  'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
  'E': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
  'E_3x3': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M', 512, 512]
}


def vgg11(pretrained=False, **kwargs):
    """VGG 11-layer model (configuration "A")

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    if pretrained:
        kwargs['init_weights'] = False
    features = make_layers(cfg['A'], batch_norm=False)
    classifier = make_classifier(final_channels=512, **kwargs)
    model = VGG(features, classifier, **kwargs)

    if pretrained:
        model.load_state_dict(load_unnamed_model(model, tvgg.vgg11(True)))
    return model


def vgg11_bn(pretrained=False, **kwargs):
    """VGG 11-layer model (configuration "A") with batch normalization

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    if pretrained:
        kwargs['init_weights'] = False
    features = make_layers(cfg['A'], batch_norm=True)
    classifier = make_classifier(final_channels=512, **kwargs)
    model = VGG(features, classifier, **kwargs)
    if pretrained:
        model.load_state_dict(load_unnamed_model(model, tvgg.vgg11_bn(True)))
    return model


def vgg13(pretrained=False, **kwargs):
    """VGG 13-layer model (configuration "B")

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    if pretrained:
        kwargs['init_weights'] = False
    features = make_layers(cfg['B'], batch_norm=False)
    classifier = make_classifier(final_channels=512, **kwargs)
    model = VGG(features, classifier, **kwargs)
    if pretrained:
        model.load_state_dict(load_unnamed_model(model, tvgg.vgg13(True)))
    return model


def vgg13_bn(pretrained=False, **kwargs):
    """VGG 13-layer model (configuration "B") with batch normalization

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    if pretrained:
        kwargs['init_weights'] = False
    features = make_layers(cfg['B'], batch_norm=True)
    classifier = make_classifier(final_channels=512, **kwargs)
    model = VGG(features, classifier, **kwargs)
    if pretrained:
        model.load_state_dict(load_unnamed_model(model, tvgg.vgg13_bn(True)))
    return model


def vgg16(pretrained=False, **kwargs):
    """VGG 16-layer model (configuration "D")

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    if pretrained:
        kwargs['init_weights'] = False
    features = make_layers(cfg['D'], batch_norm=False)
    classifier = make_classifier(final_channels=512, **kwargs)
    model = VGG(features, classifier, **kwargs)
    if pretrained:
        model.load_state_dict(load_unnamed_model(model, tvgg.vgg16(True)))
    return model


def vgg16_bn(pretrained=False, **kwargs):
    """VGG 16-layer model (configuration "D") with batch normalization

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    if pretrained:
        kwargs['init_weights'] = False
    features = make_layers(cfg['D'], batch_norm=True)
    classifier = make_classifier(final_channels=512, **kwargs)
    model = VGG(features, classifier, **kwargs)
    if pretrained:
        model.load_state_dict(load_unnamed_model(model, tvgg.vgg16_bn(True)))
    return model


def vgg19(pretrained=False, **kwargs):
    """VGG 19-layer model (configuration "E")

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    if pretrained:
        kwargs['init_weights'] = False
    features = make_layers(cfg['E'], batch_norm=False)
    classifier = make_classifier(final_channels=512, **kwargs)
    model = VGG(features, classifier, **kwargs)
    if pretrained:
        model.load_state_dict(load_unnamed_model(model, tvgg.vgg19(True)))
    return model


def vgg19_bn(pretrained=False, **kwargs):
    """VGG 19-layer model (configuration 'E') with batch normalization

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    if pretrained:
        kwargs['init_weights'] = False
    features = make_layers(cfg['E'], batch_norm=True)
    classifier = make_classifier(final_channels=512, **kwargs)
    model = VGG(features, classifier, **kwargs)
    if pretrained:
        model.load_state_dict(load_unnamed_model(model, tvgg.vgg19_bn(True)))
    return model


def vgg19_normalized():
  model = vgg19()
  model.prune('relu5_4')
  model.load_state_dict(torch.utils.model_zoo.load_url(VGG19_NORM_WEIGHTS))
  return model


def load_unnamed_model(net, net_old):
  assert len(net.state_dict()) == len(net_old.state_dict()), \
    (len(net.state_dict()), len(net_old.state_dict()))
  old_state = net_old.state_dict()
  new_state = {k_new: w_old
               for (k_new, w_old)
               in zip(net.state_dict().keys(), old_state.values())}
  return new_state
