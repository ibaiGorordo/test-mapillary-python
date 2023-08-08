import mapillary.interface as mly
from imread_from_url import imread_from_url

import cv2
from mly_token import MLY_ACCESS_TOKEN

from segmentation_utils import Detection, geometry_to_coordinates, draw_detections, read_labels


def process_img(img_id):
    img_fields = ["camera_parameters", "thumb_original_url", "compass_angle", "computed_compass_angle", "computed_geometry"]
    img_data = eval(mly.image_from_key(img_id, fields=img_fields))
    print(img_data)
    img_url = img_data['features']['properties']['thumb_original_url'].replace('\\', '')
    img = imread_from_url(img_url)

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

def get_img_sequence(img_id):
    img_data = eval(mly.image_from_key(img_id, fields=["sequence"]))
    return img_data['features']['properties']['sequence']

if __name__ == '__main__':

    label_colors = read_labels('labels.txt')

    mly.set_access_token(MLY_ACCESS_TOKEN)

    img_id = "1013728389648827"
    get_img_sequence(img_id)

    img, detections = process_img(img_id)
    detection_img = draw_detections(img, detections, label_colors)

    combined_img = cv2.addWeighted(img, 0.5, detection_img, 0.5, 0)

    cv2.imshow('image', combined_img)
    cv2.waitKey(0)
