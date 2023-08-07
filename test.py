import mapillary.interface as mly
from imread_from_url import imread_from_url
import base64
import mapbox_vector_tile
from dataclasses import dataclass
import cv2
import numpy as np
from mly_token import MLY_ACCESS_TOKEN

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

def draw_detection(img, detection):
    coordinates = detection.coordinates
    label = detection.label
    color = label_colors[label]
    coordinates[:, 0] = coordinates[:, 0] * img.shape[1]
    coordinates[:, 1] = coordinates[:, 1] * img.shape[0]
    coordinates = coordinates.astype(int)

    cv2.fillPoly(img, pts=[coordinates], color=color)

def draw_detections(img, detections):
    img_copy = img.copy()
    for detection in detections:
        draw_detection(img_copy, detection)
    return img_copy

def read_labels(label_path):
    with open(label_path, 'r') as f:
        lines = f.readlines()
    labels = [line.strip() for line in lines]
    colors = rng.uniform(0, 255, size=(len(labels), 3))
    label_colors = dict(zip(labels, colors))
    return label_colors

def process_img(img_id):
    img_fields = ["camera_parameters", "thumb_original_url", "width", "height"]
    img_data = eval(mly.image_from_key(img_id, fields=img_fields))
    img_url = img_data['features']['properties']['thumb_original_url'].replace('\\', '')
    img = imread_from_url(img_url)
    width = img_data['features']['properties']['width']
    height = img_data['features']['properties']['height']

    detection_data = mly.get_detections_with_image_id(image_id=img_id).to_dict()

    detections = []
    for feature in detection_data['features']:
        detection_properties = feature['properties']
        label = detection_properties['value']
        if label not in label_colors:
            continue
        coordinates = geometry_to_coordinates(detection_properties['pixel_geometry'])
        detection = Detection(coordinates, label)
        detections.append(detection)

    return img, detections


if __name__ == '__main__':

    label_colors = read_labels('labels.txt')


    mly.set_access_token(MLY_ACCESS_TOKEN)

    img_id = "530868028403807"
    img, detections = process_img(img_id)
    detection_img = draw_detections(img, detections)

    combined_img = cv2.addWeighted(img, 0.5, detection_img, 0.5, 0)

    cv2.imshow('image', combined_img)
    cv2.waitKey(0)
