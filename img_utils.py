from dataclasses import dataclass, fields
import mapillary.interface as mly

@dataclass
class ImageData:
    altitude: float
    atomic_scale: float
    camera_parameters: list
    camera_type: str
    captured_at: str
    compass_angle: float
    computed_altitude: float
    computed_compass_angle: float
    computed_geometry: dict
    computed_rotation: str
    exif_orientation: str
    geometry: dict
    height: int
    thumb_256_url: str
    thumb_1024_url: str
    thumb_2048_url: str
    thumb_original_url: str
    merge_cc: int
    mesh: dict
    sequence: str
    sfm_cluster: dict
    width: int
    detections: list

    def __init__(self, image_id):
        self.raw_data = eval(mly.image_from_key(image_id, fields=self.fields()))['features']

        self.altitude = self.get_altitude(self.raw_data)
        self.atomic_scale = self.get_atomic_scale(self.raw_data)
        self.camera_parameters = self.get_camera_parameters(self.raw_data)
        self.camera_type = self.get_camera_type(self.raw_data)
        self.captured_at = self.get_captured_at(self.raw_data)
        self.compass_angle = self.get_compass_angle(self.raw_data)
        self.computed_altitude = self.get_computed_altitude(self.raw_data)
        self.computed_compass_angle = self.get_computed_compass_angle(self.raw_data)
        self.computed_geometry = self.get_computed_geometry(self.raw_data)
        self.computed_rotation = self.get_computed_rotation(self.raw_data)
        self.exif_orientation = self.get_exif_orientation(self.raw_data)
        self.geometry = self.get_geometry(self.raw_data)
        self.height = self.get_height(self.raw_data)
        self.thumb_256_url = self.get_thumb_256_url(self.raw_data)
        self.thumb_1024_url = self.get_thumb_1024_url(self.raw_data)
        self.thumb_2048_url = self.get_thumb_2048_url(self.raw_data)
        self.thumb_original_url = self.get_thumb_original_url(self.raw_data)
        self.merge_cc = self.get_merge_cc(self.raw_data)
        self.mesh = self.get_mesh(self.raw_data)
        self.sequence = self.get_sequence(self.raw_data)
        self.sfm_cluster = self.get_sfm_cluster(self.raw_data)
        self.width = self.get_width(self.raw_data)
        self.detections = self.get_detections(self.raw_data)

    @staticmethod
    def fields():
        return [field.name for field in fields(ImageData)]

    @staticmethod
    def get_altitude(raw_data):
        return raw_data['properties']['altitude']

    @staticmethod
    def get_atomic_scale(raw_data):
        return raw_data['properties']['atomic_scale']

    @staticmethod
    def get_camera_parameters(raw_data):
        return raw_data['properties']['camera_parameters']

    @staticmethod
    def get_camera_type(raw_data):
        return raw_data['properties']['camera_type']

    @staticmethod
    def get_captured_at(raw_data):
        return raw_data['properties']['captured_at']

    @staticmethod
    def get_compass_angle(raw_data):
        return raw_data['properties']['compass_angle']

    @staticmethod
    def get_computed_altitude(raw_data):
        return raw_data['properties']['computed_altitude']

    @staticmethod
    def get_computed_compass_angle(raw_data):
        return raw_data['properties']['computed_compass_angle']

    @staticmethod
    def get_computed_geometry(raw_data):
        return raw_data['properties']['computed_geometry']

    @staticmethod
    def get_computed_rotation(raw_data):
        return raw_data['properties']['computed_rotation']

    @staticmethod
    def get_exif_orientation(raw_data):
        return raw_data['properties']['exif_orientation']

    @staticmethod
    def get_geometry(raw_data):
        return raw_data['geometry']

    @staticmethod
    def get_height(raw_data):
        return raw_data['properties']['height']

    @staticmethod
    def get_thumb_256_url(raw_data):
        return raw_data['properties']['thumb_256_url'].replace('\\', '')

    @staticmethod
    def get_thumb_1024_url(raw_data):
        return raw_data['properties']['thumb_1024_url'].replace('\\', '')

    @staticmethod
    def get_thumb_2048_url(raw_data):
        return raw_data['properties']['thumb_2048_url'].replace('\\', '')

    @staticmethod
    def get_thumb_original_url(raw_data):
        return raw_data['properties']['thumb_original_url'].replace('\\', '')

    @staticmethod
    def get_merge_cc(raw_data):
        return raw_data['properties']['merge_cc']

    @staticmethod
    def get_mesh(raw_data):
        return raw_data['properties']['mesh']

    @staticmethod
    def get_sequence(raw_data):
        return raw_data['properties']['sequence']

    @staticmethod
    def get_sfm_cluster(raw_data):
        return raw_data['properties']['sfm_cluster']

    @staticmethod
    def get_width(raw_data):
        return raw_data['properties']['width']

    @staticmethod
    def get_detections(raw_data):
        return raw_data['properties']['detections']

