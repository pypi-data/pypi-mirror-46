import os

import pandas as pd
import cv2


def _ensure_path_exists(fpath):
    try:
        os.makedirs(fpath)
    except FileExistsError:
        pass


def _get_max_image_dim(fpath):
    """
    Open up all of the images to see their heights and widths.
    Keep a running max of each, which is returned at the end.
    """

    max_height = 0
    max_width = 0

    with open(fpath) as f:
        for row in f:
            im_path = row.split(',')[0]
            im = cv2.imread(im_path)
            height, width, _ = im.shape

            if height > max_height:
                max_height = height

            if width > max_width:
                max_width = width

    print('Max height:', max_height)
    print('Max width :', max_width)

    return max(max_height, max_width)


def _determine_pad_amount(image_array, max_height, max_width):
    """
    Given an image and desired max height/width,
    find how much height and width is needed to make
    the image the appropriate size
    """

    height, width, _ = image_array.shape

    height_needed = max_height - height
    width_needed = max_width - width

    return height_needed, width_needed


def _get_classes(fpath):
    df = pd.read_csv(fpath, names=['path', 'scores'])
    return [str(x) for x in list(df['scores'].unique())]
