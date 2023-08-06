import json
from pathlib import Path
from typing import Type

import box
import jsonschema
from torch import nn
from torch.nn import functional

from .batch_norm_2d import load_default_batch_norm_2d
from .configs import ResNetConfig
from .layers import Classifier, Squeeze, GlobalPooling


class Bottleneck(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int, batch_norm_2d: Type[nn.BatchNorm2d]):
        super().__init__()

        mid_channels = out_channels // 4
        self.blocks = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=1, bias=False),
            batch_norm_2d(mid_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid_channels, mid_channels, kernel_size=3, stride=stride, padding=1, bias=False),
            batch_norm_2d(mid_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid_channels, out_channels, kernel_size=1, bias=False),
            batch_norm_2d(out_channels),
        )

        if stride == 1 and in_channels == out_channels:
            self.shortcut = nn.Sequential()
        else:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                batch_norm_2d(out_channels),
            )

    def forward(self, x):
        out = self.blocks(x) + self.shortcut(x)
        out = functional.relu(out, inplace=True)
        return out


@box.register(tag='model')
class ResNet(nn.Module):
    with open(str(Path(__file__).parent / 'schema' / 'resnet_config.json')) as f:
        schema = json.load(f)

    def __init__(self, config: ResNetConfig):
        super().__init__()
        batch_norm_2d: Type[nn.BatchNorm2d] = load_default_batch_norm_2d()

        in_channels = 64
        blocks = [
            nn.Conv2d(in_channels=3, out_channels=in_channels, kernel_size=7, stride=2, padding=3, bias=False),
            batch_norm_2d(in_channels),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        ]

        stride_list = [1, 2, 2, 2]
        channels_list = [256, 512, 1024, 2048]
        for layers, out_channels, first_stride in zip(config.layers_list, channels_list, stride_list):
            for i in range(layers):
                stride = first_stride if i == 0 else 1
                blocks.append(Bottleneck(in_channels, out_channels, stride=stride, batch_norm_2d=batch_norm_2d))
                in_channels = out_channels
        blocks.append(GlobalPooling())
        blocks.append(Squeeze())
        blocks.append(Classifier(in_channels, config.feature_dim, dropout=config.dropout_ratio))

        self.blocks = nn.Sequential(*blocks)
        self._initialize_weights(batch_norm_2d=batch_norm_2d)

    def _initialize_weights(self, batch_norm_2d):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight.data)
            elif isinstance(m, batch_norm_2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, x):
        return self.blocks(x)

    @classmethod
    def factory(cls, config: dict = None):
        jsonschema.validate(config or {}, cls.schema)
        return cls(config=ResNetConfig(values=config))
