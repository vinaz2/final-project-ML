"""
This script goes along my blog post:
'Keras Cats Dogs Tutorial' (https://jkjung-avt.github.io/keras-tutorial/)
"""


import os
import sys
import glob
import argparse

import numpy as np
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    return args


def get_files(path):
    if os.path.isdir(path):
        files = glob.glob(os.path.join(path, '*'))
    elif path.find('*') > 0:
        files = glob.glob(path)
    else:
        files = [path]

    files = [f for f in files if f.lower().endswith(('jpg', 'jpeg', 'png'))]

    if not len(files):
        sys.exit('No images found by the given path!')

    return files


if __name__ == '__main__':
    args = parse_args()
    files = get_files(args.path)

    # Update this to three classes
    cls_list = ['cats', 'dogs', 'snakes']

    # Load your updated trained model (3-class model)
    net = load_model('model-resnet50-final3.h5')

    # Loop through all files and make predictions
    for f in files:
        img = image.load_img(f, target_size=(224, 224))
        if img is None:
            continue
        x = image.img_to_array(img)
        x = preprocess_input(x)
        x = np.expand_dims(x, axis=0)
        pred = net.predict(x)[0]
        top_inds = pred.argsort()[::-1][:3]  # top 3 predictions now
        print(f'File: {f}')
        for i in top_inds:
            print(f'    {pred[i]:.3f}  {cls_list[i]}')
