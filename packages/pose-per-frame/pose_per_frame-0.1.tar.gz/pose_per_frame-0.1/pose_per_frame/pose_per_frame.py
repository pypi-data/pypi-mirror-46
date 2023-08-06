import tensorflow as tf
import keras.models as kmodels
import keras.backend as K
import numpy as np


class ConfigClass:
    def __init__(self, MODEL_PATH=r'C:\dev\occupancy-detection\Guardian-RSIP\working_model_weights\20190422_HourGlass_RSIP\weights-03-11.67_block_2_converted.h5',
                 BODY_POSE_THRESHOLD=95, HEIGHT_WIDTH_FACTOR=1.45, BETWEEN_POINTS_FACTOR=0.47, ADDITIONAL_PIXELS_TO_THE_RIGHT=10, MIN_BBOX_HEIGHT=40, MIN_BBOX_WIDTH=40):
        self.MODEL_PATH = MODEL_PATH
        self.BODY_POSE_THRESHOLD = BODY_POSE_THRESHOLD
        self.HEIGHT_WIDTH_FACTOR = HEIGHT_WIDTH_FACTOR
        self.BETWEEN_POINTS_FACTOR = BETWEEN_POINTS_FACTOR
        self.ADDITIONAL_PIXELS_TO_THE_RIGHT = ADDITIONAL_PIXELS_TO_THE_RIGHT
        self.MIN_BBOX_HEIGHT = MIN_BBOX_HEIGHT
        self.MIN_BBOX_WIDTH = MIN_BBOX_WIDTH
        

class BodyPoseHandler(object):
    def __init__(self):
        self.model = None
        self.body_to_index_dict = None
        self.load_model(config_class.MODEL_PATH)
        # :type: kmodels.Model

        self.pose_point_order = [
            'forhead', 'LEar', 'REar', 'LEye', 'REye', 'nose', 'neck', 'LShoulder', 'LElbow', 'LWrist', 'RShoulder',
            'RElbow', 'RWrist', 'Pelvis', 'LHip', 'LKnee', 'LFoot', 'RHip', 'RKnee', 'RFoot'
        ]
        self.create_body_part_to_index_dict()
        self.head_parts = ['forhead', 'LEar', 'REar', 'LEye', 'REye', 'nose']
        pass

    def load_model(self, model_path):
        """
        Loads the BP Keras model.
        :param model_path: a string containing the path to the saved Keras kmodels.Model.
        """
        custom_objects = {
            "heatmap_mse_loss_boolean_mask": self.heatmap_mse_loss_boolean_mask, }
        self.model = kmodels.load_model(model_path, custom_objects)

    def predict(self, frame):
        """
        This function gets a frame from the input and predicts bodypose_weigths keypoints and uses those to create
        a bbox around the face.
        :param frame: a 16 bit frame from the input source.
        :return: all_locations: a dictionary where the keys are the body part names and the values are a list of
                                keypoint coordinates in ints. Each element in the list corresponds to a different
                                passenger in the car, 0 is usually the driver.
                                The X values are element 1 and the Y values are element 2.
                 box: a bbox around the face in the format of @self.convert_bp_bbox_to_original_coordinates().
        """
        if frame is None:
            return
        frame_for_input = self.preprocess_frame(frame)
        all_locations = self.get_all_locations(frame_for_input, config_class.BODY_POSE_THRESHOLD)
        return all_locations

    def create_body_part_to_index_dict(self):
        """
        creates a dictionary where the key is the name of the body part and the value is a tuple with
        the location of the Y, X values of that keypoint in the output list of the BP network.
        """
        body_to_index_dict = {}
        for i, ppoint in enumerate(self.pose_point_order):
            body_to_index_dict[ppoint] = (i * 2, i * 2 + 1)

        self.body_to_index_dict = body_to_index_dict

    def get_all_locations(self, frame, keypoint_thresh):
        """
        Predicts the locations of all the body parts in the input frame with a default threshold of 100.
        :param keypoint_thresh:
        :param frame:
        :type frame:
        :return: all_locations: a dictionary where the keys are the body part names and the values are a list of
                                keypoint coordinates in ints. Each element in the list corresponds to a different
                                passenger in the car, 0 is usually the driver.
                                The X values are element 1 and the Y values are element 2.
        :rtype:
        """

        predictions = self.model.predict(frame, batch_size=1, verbose=0)
        predictions_out = np.squeeze(predictions[0])
        coors_from_heatmap = np.array(self.transform_frame_heatmaps_to_keypoints(predictions_out,
                                                                                 point_threshold=keypoint_thresh))
        coors_from_heatmap = self.translate_coors_to_frame(coors_from_heatmap, np.squeeze(frame).shape)
        part_coordinates_dict = self.get_all_part_locations_from_coordinates(coors_from_heatmap)
        return part_coordinates_dict

    def translate_coors_to_frame(self, coors, frame_shape):
        """
        translates the keypoints to the desired frame shape
        :param coors: keypoints as output by @transform_frame_heatmaps_to_keypoints()
        :param frame_shape: the shape of the frame, tuple of ints
        :return: coordinate relative to the frame in the same format as the input.
        """
        frame_height, frame_width = frame_shape
        height_mean, height_std = frame_height / 2, frame_height / 2
        width_mean, width_std = frame_width / 2, frame_width / 2
        coors = coors[:, 1:]
        coors[:, ::2] = (coors[:, ::2] * height_std) + height_mean
        coors[:, 1::2] = (coors[:, 1::2] * width_std) + width_mean
        return coors

    def get_part_locations_from_coordinates(self, coors_from_heatmap, body_part_name):
        """
        returns the coordinates of a given body part name.
        :param coors_from_heatmap: keypoints as output by @transform_frame_heatmaps_to_keypoints()
        :param body_part_name: the name of the desired body part.
        :return: a list containing the list of Y, X coordinates.
        """
        part_coordinates = []
        coor = coors_from_heatmap[0]
        part_location = [
            coor[self.body_to_index_dict[body_part_name][0]],
            coor[self.body_to_index_dict[body_part_name][1]]
        ]

        if not np.isnan(part_location[0]) and not np.isnan(part_location[1]):
            part_coordinates.append(part_location)

        return part_coordinates

    def get_all_part_locations_from_coordinates(self, coors_from_heatmap):
        """
        converts the format of the body part keypoints coordinates from the input format to the output format.
        :param coors_from_heatmap: keypoints as output by @transform_frame_heatmaps_to_keypoints()
        :return: locations of the body parts as output by the @get_all_locations() function
        """
        part_coordinates_dict = {}
        for part in self.pose_point_order:
            part_coordinates_dict[part] = self.get_part_locations_from_coordinates(coors_from_heatmap, part)

        return part_coordinates_dict

    def preprocess_frame(self, frame):
        """
        Rotates the frame by 90 degrees
        :param frame: 16 bit frame
        :return: 16 bit frame
        """
        frame_for_input = np.rot90(frame, 3)
        frame_for_input = np.expand_dims(frame_for_input, -1)
        frame_for_input = np.expand_dims(frame_for_input, 0)
        return frame_for_input

    def return_maximum_likelihood_indices(self, heatmap, point_threshold):
        y, x = np.unravel_index(np.argmax(heatmap, axis=None), heatmap.shape)
        score = heatmap[y, x].copy()
        if score < point_threshold:
            return np.nan, np.nan, score
        else:

            # compute boreders of 7x7 patch containing max value as middle point:
            min_x = max(0, x - 3)
            max_x = min(heatmap.shape[1] - 1, x + 3)
            min_y = max(0, y - 3)
            max_y = min(heatmap.shape[0] - 1, y + 3)

            # patch indices:
            patch = heatmap[min_y:max_y + 1, min_x:max_x + 1]
            sum_rows = np.sum(patch, axis=0)
            sum_columns = np.sum(patch, axis=1)

            normalization_term = np.sum(patch)
            y = np.inner(sum_columns, np.arange(min_y, max_y + 1)) / normalization_term
            x = np.inner(np.arange(min_x, max_x + 1), sum_rows) / normalization_term

            y = y / (heatmap.shape[0] / 2) - 1
            x = x / (heatmap.shape[1] / 2) - 1
            return y, x, score

    def transform_frame_heatmaps_to_keypoints(self, frame_heatmaps, regression_pred=None, num_of_seats=5, num_of_keypoints=20,
                                              point_threshold=100):
        """
        Inputs:
          frame_heatmaps - A 64x48x100 numpy array containing the heatmap info for the frame.
          regression_pred - A list of length 5 containing the occupancy predication for the frame, if None
                            ocuppency is calculated using the heatmaps.
          num_of_seat - int, number of seats in the car.
          num_of_keypoints - int, number of keypoints being predicted.
          point_threshold - int, the threshold for considering a heatmap point as a valid keypoint.
        Output:
          frame_pred - A (num_of_seats) x (2*num_of_keypoints + 1) numpy array containing keypoint predictions
                       per seat. Each row is as follows [occupancy_prediction, first_keypoint_row, first_keypoint_col,
                       second_keypoint_row, second_keypoint_col, ...]
        """
        frame_pred = np.empty((num_of_seats, 2 * num_of_keypoints + 1))
        occupency_prob = np.zeros(num_of_seats)
        for seat_idx in range(num_of_seats):
            for keypoint_idx in range(num_of_keypoints):
                y, x, score = self.return_maximum_likelihood_indices(
                    frame_heatmaps[..., seat_idx * num_of_keypoints + keypoint_idx], point_threshold)
                occupency_prob[seat_idx] += score
                frame_pred[seat_idx, 2 * keypoint_idx + 1] = y
                frame_pred[seat_idx, 2 * keypoint_idx + 2] = x
        if regression_pred is None:
            occupency_prob = occupency_prob / 300
            frame_pred[:, 0] = occupency_prob
        else:
            frame_pred[:, 0] = np.array(regression_pred)
        return frame_pred

    def heatmap_mse_loss_boolean_mask(self, y_true, y_pred):
        zeros = tf.zeros_like(y_true)
        loss_keypoint_mask_indices = tf.greater_equal(y_true, zeros)

        y_true_reg_masked = tf.boolean_mask(y_true, loss_keypoint_mask_indices)
        y_pred_reg_masked = tf.boolean_mask(y_pred, loss_keypoint_mask_indices)

        mse = K.mean(K.square(y_true_reg_masked - y_pred_reg_masked))

        return mse

    def get_factored_number_between_numbers(self, n1, n2, factor=0.5):
        """
        Finds a number between two numbers, the factor describes were the number is going to be if the scale between
        them is between 0-1.
        :param n1: a number, int.
        :param n2: same as n1.
        :param factor: a float between 0-1.
        :return: a number between n1 and n2, int.
        """
        nnew = int(factor * abs(n1 - n2) + min(n1, n2))
        return nnew

    def create_bbox_from_keypoints_algo1(self, all_locations):
        """
        left and right of the body parts are from the drivers perspective not from the camera's,
        L and R in the algorithm is in the frame (the camera's perspective).
        :param all_locations: same as in @processes_frame()
        :return: a bbox around the face in the format of @self.convert_bp_bbox_to_prnet().
        """
        LEye = all_locations['LEye']
        REye = all_locations['REye']
        nose = all_locations['nose']
        LEar = all_locations['LEar']
        REar = all_locations['REar']

        if not nose or (not LEar and not LEye) or (not REye and not REar):
            return None

        nose_x = nose[0][1]
        nose_y = nose[0][0]

        if REar:
            Lx = REar[0][1]
            Ly = REar[0][0]
        else:
            Lx = REye[0][1]
            Ly = REye[0][0]
        if LEar:
            Rx = LEar[0][1]
        else:
            Rx = LEye[0][1]

        Lx = min(Lx, nose_x)
        Rx = max(Rx, nose_x)

        height_width_factor = config_class.HEIGHT_WIDTH_FACTOR
        between_points_factor = config_class.BETWEEN_POINTS_FACTOR
        additional_pixels_to_the_right = config_class.ADDITIONAL_PIXELS_TO_THE_RIGHT
        min_bbox_height = config_class.MIN_BBOX_HEIGHT
        min_bbox_width = config_class.MIN_BBOX_WIDTH

        half_height = (height_width_factor * abs(Rx - Lx)) / 2
        Ymid = self.get_factored_number_between_numbers(Ly, nose_y, between_points_factor)

        top = int(Ymid - half_height)
        left = int(Lx)
        bottom = int(Ymid + half_height)
        right = int(Rx + additional_pixels_to_the_right)

        if bottom - top < min_bbox_height or right - left < min_bbox_width:
            return None

        bbox = {
            'top': top,
            'left': left,
            'bottom': bottom,
            'right': right


        }

        return bbox

    def convert_bp_bbox_to_original_coordinates(self, box, frame):
        """
        :param box: dict of ints
        :param frame: frame from the reader class
        :return: dict of ints with coordinates from the original frame before the preprocess
        """
        height = frame.shape[0]

        new_box = {
            'top': height - box['right'],
            'left': box['top'],
            'bottom': height - box['left'],
            'right': box['bottom']
        }
        return new_box


if __name__ == '__main__':
    from tools.load_functions import load_frame

    config_class = ConfigClass()
    bp_handler = BodyPoseHandler()
    f = np.rot90(load_frame(r'E:\all_recs_front_mc\rec_20190110_113636\video_raw',frame_num=10,frm_dims=(480,640)),k=-3)
    body_parts_dict = bp_handler.predict(f)