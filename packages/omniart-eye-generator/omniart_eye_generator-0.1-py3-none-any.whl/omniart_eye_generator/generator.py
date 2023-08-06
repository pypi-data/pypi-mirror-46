import torch
import torch.nn as nn

latent_space_size = 100
label_count = 8
generator_feature_maps = 64
channels = 3


class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(latent_space_size + label_count, generator_feature_maps * 16, 4, 1, 0, bias=False),
            nn.BatchNorm2d(generator_feature_maps * 16),
            nn.ReLU(True),
            nn.Dropout(0.2),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(generator_feature_maps * 16, generator_feature_maps * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(generator_feature_maps * 8),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d(generator_feature_maps * 8, generator_feature_maps * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(generator_feature_maps * 4),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d(generator_feature_maps * 4, generator_feature_maps * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(generator_feature_maps * 2),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d(generator_feature_maps * 2, generator_feature_maps, 4, 2, 1, bias=False),
            nn.BatchNorm2d(generator_feature_maps),
            nn.ReLU(True),
            # state size. (ngf) x 64 x 64
            nn.ConvTranspose2d(generator_feature_maps, channels, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. (nc) x 128 x 128
        )

    def forward(self, noise, labels):

        batch_size = noise.size(0)
        noise = noise.squeeze()

        if noise.dim() == 1:
            noise = noise.unsqueeze(0)

        x = torch.cat([noise, labels], 1)
        x = x.view(batch_size, -1, 1, 1)

        x = self.main(x)
        return x
