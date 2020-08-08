# encoding=utf-8
import os
import time
import random

import numpy as np
import cv2
import pandas as pd

from tqdm import tqdm

import tensorflow as tf


def load_image_label(path: str, shuffle=False):
    class_list = os.listdir(data_root)
    class_list.sort()

    all_images = []
    all_labels = []

    for image_class in class_list:
        class_path = f'{data_root}/{image_class}'
        class_images = os.listdir(class_path)
        class_image_paths = [f'{class_path}/{img_file}' for img_file in class_images]
        all_images.extend(class_image_paths)
        all_labels.extend(len(class_images) * image_class)

    if shuffle:
        zipped = list(zip(all_images, all_labels))
        random.shuffle(zipped)

        all_images, all_labels = list(zip(*zipped))
        all_images = list(all_images)
        all_labels = list(all_labels)

    return all_images, all_labels

# The following functions can be used to convert a value to a type compatible
# with tf.Example.


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def compile_tfrecord(all_images, all_labels, filename):
    with tf.io.TFRecordWriter(filename) as tfrec_writer:
        dataset_list = list(zip(all_images, all_labels))
        for image_path, label, in tqdm(dataset_list):
            image_raw = open(image_path, 'rb').read()

            feature = {
                'image_raw': _bytes_feature(image_raw),
                'label': _int64_feature(label),
            }

            example_obj = tf.train.Example(features=tf.train.Features(feature=feature))
            tfrec_writer.write(example_obj.SerializeToString())


if __name__ == "__main__":
    data_root = 'ETL9G_IMG'

    class_list = pd.read_csv('classes.tsv', sep='\t', encoding='utf-8').values[:, 0]
    char2idx = {c: idx for idx, c in enumerate(class_list)}

    all_images, all_labels = load_image_label(data_root, shuffle=True)
    idx_labels = [char2idx[c] for c in all_labels]

    tfrec_filename = f'ETL9G_tf_version_{tf.__version__}.tfrecord'

    compile_tfrecord(all_images, idx_labels, tfrec_filename)
