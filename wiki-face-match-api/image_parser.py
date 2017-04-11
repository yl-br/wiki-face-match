import openface
import os

class ImageParser:
    def __init__(self, path_to_open_face_models):
        self.dlib_face_predictor_path = os.path.join(path_to_open_face_models,'dlib/shape_predictor_68_face_landmarks.dat')
        self.network_model_path = os.path.join(path_to_open_face_models, 'openface/nn4.small2.v1.t7')
        self.default_image_dimension = 96
        self.align = None
        self.net = None

    def init(self):
        self.align = openface.AlignDlib(str(self.dlib_face_predictor_path))
        self.net = openface.TorchNeuralNet(str(self.network_model_path), self.default_image_dimension)



    def get_face_bounding_box(self, rgb_image):
        bounding_box = self.align.getLargestFaceBoundingBox(rgb_image)
        return bounding_box

    def get_face_representation(self, rgb_image, bounding_box):
        aligned_face = self.align.align(self.default_image_dimension, rgb_image, bounding_box,
                                  landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if aligned_face is None:
            raise Exception("Unable to align image.")
        representation = self.net.forward(aligned_face)
        return representation



