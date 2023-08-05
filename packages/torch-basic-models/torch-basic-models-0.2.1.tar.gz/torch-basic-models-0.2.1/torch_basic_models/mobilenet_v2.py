import json
from pathlib import Path
from typing import Type

import box
import jsonschema
import torch.nn as nn
from mobile_block import MobileBlock

from .batch_norm_2d import load_default_batch_norm_2d
from .configs import MobileNetV2Config
from .layers import Classifier, Squeeze, GlobalPooling, InplaceReLU6


@box.register(tag='model')
class MobileNetV2(nn.Module):
    with open(str(Path(__file__).parent / 'schema' / 'mobilenet_v2_config.json')) as f:
        schema = json.load(f)

    def __init__(self, config: MobileNetV2Config):
        super().__init__()
        t = config.expansion_ratio
        input_size = config.input_size
        width_multiple = config.width_multiple
        batch_norm_2d: Type[nn.BatchNorm2d] = load_default_batch_norm_2d()
        stride_list = config.stride_list

        # building first layer
        in_channels = int(32 * width_multiple)
        blocks = [
            self.conv_bn_relu(3, in_channels, kernel=3, stride=stride_list[0], batch_norm_2d=batch_norm_2d)
        ]
        input_size //= 2

        # building inverted residual blocks
        block_settings = [
            # t, c, n, s
            [1, 16, 1, 1],
            [t, 24, 2, stride_list[1]],
            [t, 32, 3, stride_list[2]],
            [t, 64, 4, stride_list[3]],
            [t, 96, 3, 1],
            [t, 160, 3, stride_list[4]],
            [t, 320, 1, 1],
        ]
        for expansion, channels, times, first_stride in block_settings:
            out_channels = int(channels * width_multiple)

            for i in range(times):
                stride = first_stride if i == 0 else 1
                block = MobileBlock(
                    input_size=input_size,
                    in_channels=in_channels,
                    out_channels=out_channels,
                    stride=stride,
                    expansion=expansion,
                    kernel=3,
                    groups=1,
                    batch_norm_2d=batch_norm_2d,
                    relu=InplaceReLU6,
                    residual=True)
                blocks.append(block)

                in_channels = out_channels
                input_size //= stride

        last_channels = int(1280 * max(width_multiple, 1.0))
        blocks.append(self.conv_bn_relu(in_channels, last_channels, kernel=1, stride=1, batch_norm_2d=batch_norm_2d))
        blocks.append(GlobalPooling())
        blocks.append(Squeeze())
        blocks.append(Classifier(last_channels, config.feature_dim, dropout=config.dropout_ratio))

        self.blocks = nn.Sequential(*blocks)
        self._initialize_weights(batch_norm_2d=batch_norm_2d)

    def forward(self, x):
        return self.blocks(x)

    @staticmethod
    def conv_bn_relu(in_channels: int, out_channels: int, kernel: int, stride: int,
                     batch_norm_2d: Type[nn.BatchNorm2d]):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel, stride=stride, padding=kernel // 2, bias=False),
            batch_norm_2d(out_channels),
            InplaceReLU6()
        )

    def _initialize_weights(self, batch_norm_2d: Type[nn.BatchNorm2d]):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()  # pragma: no cover
            elif isinstance(m, batch_norm_2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                m.weight.data.normal_(0, 0.001)
                m.bias.data.zero_()

    @classmethod
    def factory(cls, config: dict = None):
        jsonschema.validate(config or {}, cls.schema)
        return cls(config=MobileNetV2Config(values=config))
