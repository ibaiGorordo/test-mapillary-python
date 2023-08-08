import base64
import mapbox_vector_tile
from dataclasses import dataclass

import cv2
import numpy as np

rng = np.random.default_rng(3)

@dataclass
class Detection:
    coordinates: np.ndarray
    label: str

def geometry_to_coordinates(pixel_geometry):
    decoded_data = base64.decodebytes(pixel_geometry.encode('utf-8'))
    detection_geometry = mapbox_vector_tile.decode(decoded_data)
    extent = detection_geometry['mpy-or']['extent']
    coordinates = np.array(detection_geometry['mpy-or']['features'][0]['geometry']['coordinates'][0])
    coordinates = coordinates / extent
    coordinates[:, 1] = 1 - coordinates[:, 1]
    return coordinates

def draw_detection(img, coordinates, color):
    coordinates[:, 0] = coordinates[:, 0] * img.shape[1]
    coordinates[:, 1] = coordinates[:, 1] * img.shape[0]
    coordinates = coordinates.astype(int)

    cv2.fillPoly(img, pts=[coordinates], color=color)

def draw_detections(img, detections, label_colors):
    img_copy = img.copy()
    for detection in detections:
        coordinates = detection.coordinates
        label = detection.label
        color = label_colors[label]
        draw_detection(img_copy, coordinates, color)
    return img_copy

def read_labels(label_path):
    with open(label_path, 'r') as f:
        lines = f.readlines()
    labels = [line.strip() for line in lines]
    colors = rng.uniform(0, 255, size=(len(labels), 3))
    label_colors = dict(zip(labels, colors))
    return label_colors