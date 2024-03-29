# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Minimal script for generating an image using pre-trained StyleGAN generator."""

import os
import pickle
import sys
import argparse

sys.path.append('./stylegan')

import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import config

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument('--init-rand', '-r', default=5, type=int)
    p.add_argument('--output', '-o', default='example.png')
    args = p.parse_args()
    return args

def main():
    args = get_args()
    # Initialize TensorFlow.
    tflib.init_tf()

    # Load pre-trained network.
    orig_url = 'https://drive.google.com/file/d/1H2RNWlES9F-iU9o8s8wRT5JqKDZVfmEq/view?usp=sharing'
    url = 'https://drive.google.com/uc?id=1H2RNWlES9F-iU9o8s8wRT5JqKDZVfmEq' # network-snapshot-005685.pkl
    with dnnlib.util.open_url(url, cache_dir=config.cache_dir) as f:
        _G, _D, Gs = pickle.load(f)
        # _G = Instantaneous snapshot of the generator. Mainly useful for resuming a previous training run.
        # _D = Instantaneous snapshot of the discriminator. Mainly useful for resuming a previous training run.
        # Gs = Long-term average of the generator. Yields higher-quality results than the instantaneous snapshot.

    # Print network details.
    Gs.print_layers()

    # Pick latent vector.
    rnd = np.random.RandomState(args.init_rand)
    latents = rnd.randn(1, Gs.input_shape[1])

    # Generate image.
    fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
    images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True, output_transform=fmt)

    # Save image.
    os.makedirs(config.result_dir, exist_ok=True)
    png_filename = os.path.join(config.result_dir, args.output)
    PIL.Image.fromarray(images[0], 'RGB').save(png_filename)

if __name__ == "__main__":
    main()
