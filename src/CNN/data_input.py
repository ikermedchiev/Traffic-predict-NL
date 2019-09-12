import tensorflow as tf
import numpy as np
from typing import List
import parameters


# Images class
class ImageData:
    def __init__(self, is_congestion: bool, image_data: List[List[List[float]]], details: List[int]):
        # is_congestion: boolean indicating whether the image leads to a congestion or not
        self.is_congestion = is_congestion
        # image_data: 3D tensor [img height, img width, 2 channels]
        self.image_data = image_data
        # details: list [year, month, day, measurement minute, history length, future prediction]
        self.details = details


# Functions which extracts the data from the files and builds the objects
def congestion_data(year: int, month: int, day: int) -> List[int]:
    data = open(parameters.ROOT_DIR + '/data/Files_A4/' + str(year) + '-' + str(month).zfill(2) + '-' +
                str(day).zfill(2) + '.txt')\
        .read()\
        .split(',')
    return list(map(int, data))


def stack_lists(a, b):
    if not isinstance(a, list):
        return [a, b]
    else:
        if len(a) != len(b):
            raise IndexError("(Nested) Lists should have the same dimensions to be stacked.")
        else:
            return list(map(stack_lists, a, b))


def sort_image_rows(data: List[List[str]], sort_list: List[str], datatype: type) -> list:
    sorted_list = []
    for station in sort_list:
        for i in range(len(data)):
            if station in data[i][0]:
                sorted_list.append(list(map(datatype, data.pop(i)[1:])))
                break
    return sorted_list


def traffic_image(year: int, month: int, day: int, minute: int, length: int, normalization_flow: float = 1.0,
                  normalization_speed: float = 1.0) -> List[List[List[float]]]:
    if minute < length:
        raise ValueError("Minute parameter should be larger than the length parameter!")

    station_list = open(parameters.ROOT_DIR + '/data/measurementSiteIDs.txt').readlines()
    station_list = [line.strip() for line in station_list]

    flowdata = open(parameters.ROOT_DIR + '/data/a4_14_21-03-2018/' + str(day).zfill(2) + '-' + str(month).zfill(2) +
                    '-' + str(year) + '/joinedFlow.txt').readlines()
    flowdata = [line.strip().split(',') for line in flowdata]
    flowdata = sort_image_rows(flowdata, station_list, float)

    speeddata = open(parameters.ROOT_DIR + '/data/a4_14_21-03-2018/' + str(day).zfill(2) + '-' + str(month).zfill(2) +
                     '-' + str(year) + '/joinedSpeed.txt').readlines()
    speeddata = [line.strip().split(',') for line in speeddata]
    speeddata = sort_image_rows(speeddata, station_list, float)

    flowdata = map(lambda x: x[minute - length:minute], flowdata)
    speeddata = map(lambda x: x[minute - length:minute], speeddata)

    flowdata = list(map(lambda row: list(map(lambda e: e / normalization_flow, row)), flowdata))
    speeddata = list(map(lambda row: list(map(lambda e: e / normalization_speed, row)), speeddata))

    return list(map(stack_lists, flowdata, speeddata))


def image_object(year: int, month: int, day: int, minute: int, image_history: int, prediction_future: int,
                 normalized: bool, normalization_flow: float, normalization_speed: float) -> 'ImageData':
    if normalized:
        image = traffic_image(year, month, day, minute, image_history, normalization_flow, normalization_speed)
    else:
        image = traffic_image(year, month, day, minute, image_history)

    if minute + prediction_future >= 900:
        is_congestion = False
    else:
        is_congestion = bool(congestion_data(year, month, day)[minute + prediction_future])

    return ImageData(is_congestion, image, [year, month, day, minute, image_history, prediction_future])


# Function which can transform a set of image data object to a 4D tensor required by the
# Convolutional Neural Network as input and the 1D tensor for the output (single batch).
def image_list_to_tensor(images: List['ImageData']) -> (tf.Tensor, tf.Tensor):
    image_list_tensor = []
    congestion_tensor = []
    for image in images:
        image_list_tensor.append(image.image_data)
        congestion_tensor.append(image.is_congestion)
    return tf.convert_to_tensor(image_list_tensor, dtype=tf.float32), \
        tf.convert_to_tensor(list(congestion_tensor), dtype=tf.int32)


def image_list_to_np_array(images: List['ImageData']) -> (np.array, np.array):
    image_list_array = []
    congestion_array = []
    for image in images:
        image_list_array.append(image.image_data)
        congestion_array.append(image.is_congestion)
    return np.array(image_list_array, dtype=np.float32), \
        np.array(congestion_array, dtype=np.int32)
