# -----------------------
#
# Copyright Jin Fagang @2018
# 
# 4/23/19
# kitti_fusion
# -----------------------

import numpy as np


class LidarCamCalibData(object):
    """
    Suppose we have 1 lidar and 4 cameras,
    more sensors can add more params too.

    tr: 3x1, transform vector
    r: 3x3, rotation vector

    """
    def __init__(self, calib_f=None):
        # transformation between lidar and 4 cameras
        self.T_lidar_to_cam_0 = []
        self.T_lidar_to_cam_1 = []
        self.T_lidar_to_cam_2 = []
        self.T_lidar_to_cam_3 = []

        # rotation between lidar and 4 cameras
        self.R_lidar_to_cam_0 = []
        self.R_lidar_to_cam_1 = []
        self.R_lidar_to_cam_2 = []
        self.R_lidar_to_cam_3 = []

        # combined transform and rectify
        self.TR_lidar_to_cam_0 = []
        self.TR_lidar_to_cam_1 = []
        self.TR_lidar_to_cam_2 = []
        self.TR_lidar_to_cam_3 = []

        # this params only works on KITTI, rectify and project matrix
        self.P_cam_0 = []
        self.P_cam_1 = []
        self.P_cam_2 = []
        self.P_cam_3 = []

        # rectify for cam N to cam0
        self.Rect_cam_0 = []
        self.Rect_cam_1 = []
        self.Rect_cam_2 = []
        self.Rect_cam_3 = []

        # normal calibration
        self.K_cam_0 = []
        self.K_cam_1 = []
        self.K_cam_2 = []
        self.K_cam_3 = []

        self.d_cam_0 = []
        self.d_cam_1 = []
        self.d_cam_2 = []
        self.d_cam_3 = []

        self.checked = False

        self.calib_f = calib_f
        if self.calib_f is not None:
            self._read_kitti_calib_from_txt()
            self.bootstrap()

    def _read_kitti_calib_from_txt(self, is_video=False):
        if not is_video:
            data = {}
            with open(self.calib_f, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line != '':
                        key, value = line.split(': ')
                        # The only non-float values in these files are dates, which
                        # we don't care about anyway
                        try:
                            data[key] = [float(x) for x in value.split()]
                        except ValueError:
                            pass
            self.TR_lidar_to_cam_0 = data['Tr_velo_to_cam']
            self.P_cam_0 = data['P2']
            self.Rect_cam_0 = data['R0_rect']

    def bootstrap(self):
        if len(self.TR_lidar_to_cam_0) > 0:
            self.TR_lidar_to_cam_0 = np.reshape(self.TR_lidar_to_cam_0, (3, 4))
        else:
            self.TR_lidar_to_cam_0 = np.concatenate(
                (np.reshape(self.R_lidar_to_cam_0, (3, 3)),
                 np.array([self.T_lidar_to_cam_0]).T), axis=1
            )
        self.TR_lidar_to_cam_0 = np.pad(self.TR_lidar_to_cam_0, ((0, 1), (0, 0)), 'constant')

        if isinstance(self.Rect_cam_0, list):
            self.Rect_cam_0 = np.reshape(self.Rect_cam_0, (3, 3))
        self.Rect_cam_0 = np.pad(self.Rect_cam_0, ((0, 1), (0, 1)), 'constant')
        if isinstance(self.P_cam_0, list):
            self.P_cam_0 = np.reshape(self.P_cam_0, (3, 4))

        assert self.TR_lidar_to_cam_0.shape == (4, 4), 'TR_lidar_to_cam_0 is R|T, which is 3x4, but received wrong'
        assert self.Rect_cam_0.shape == (4, 4), 'Rect_cam_0 is 3x3, but solve failed (a 9 length list is also OK)'
        assert self.P_cam_0.shape == (3, 4), 'P_cam {} vs {} failed'.format('(3, 4)', self.P_cam_0.shape)
        self.checked = True

    def __str__(self):
        return 'TR_lidar_to_cam_0: {}\nP_cam_0: {}\nRect_cam_0: {}\nK_cam_0: {}'.format(
            self.TR_lidar_to_cam_0, self.P_cam_0, self.Rect_cam_0, self.K_cam_0
        )


def lidar_pts_to_cam0_frame(pts3d, calib, filter_intensity=False):
    """
    Directly convert all lidar points to camera frame
    :param pts3d:
    :param calib:
    :param filter_intensity
    :return:
    """
    # filter out intensity <= 0
    if filter_intensity:
        pts3d = pts3d[pts3d[:, 3] > 0, :]
    pts3d[:, 3] = 1
    pts3d = np.transpose(pts3d)
    # Pad the r0_rect matrix to a 4x4
    if isinstance(calib, LidarCamCalibData):
        if not calib.checked:
            ValueError('calib not bootstraped, did you called calib_data.bootstrap()?')
        else:
            cam0_xyz = np.dot(calib.TR_lidar_to_cam_0, pts3d)

            ret_xyz = np.dot(calib.Rect_cam_0, cam0_xyz)
            idx = (ret_xyz[2, :] >= 0)
            pts2d_cam = np.dot(calib.P_cam_0, ret_xyz[:, idx])
            return pts3d[:, idx], pts2d_cam / pts2d_cam[2, :]
    else:
        ValueError('frame_calib must be an LidarCamCalibData type')


def lidar_pt_to_cam0_frame(pt3d, calib):
    """
    Convert a single point of lidar
    :param pt3d:
    :param calib:
    :return:
    """
    # padding the 4th element to 1
    pt3d = np.append(pt3d, 1)
    # Pad the r0_rect matrix to a 4x4
    if isinstance(calib, LidarCamCalibData):
        if not calib.checked:
            raise ValueError('calib not bootstrap, did you called calib_data.bootstrap()?')
        else:
            # 1. Get xyz1 on cam0
            cam0_xyz = np.dot(calib.TR_lidar_to_cam_0, pt3d)

            # 2. Get cam0 after rectify
            ret_xyz = np.dot(calib.Rect_cam_0, cam0_xyz)

            # 3. if points not on image, then return None
            if ret_xyz[2] >= 0:
                # 6. Get projected coords
                pts2d_cam = np.dot(calib.P_cam_0, ret_xyz)
                return pts2d_cam / pts2d_cam[2]
            else:
                return None
    else:
        raise ValueError('frame_calib must be an LidarCamCalibData type')


def cam3d_to_pixel(cam3d, calib):
    """
    Convert a single point of lidar
    :param cam3d:
    :param calib:
    :return:
    """
    # padding the 4th element to 1
    pt3d = np.append(cam3d, 1)
    # Pad the r0_rect matrix to a 4x4
    if isinstance(calib, LidarCamCalibData):
        if not calib.checked:
            raise ValueError('calib not bootstrap, did you called calib_data.bootstrap()?')
        else:
            # 2. Get cam0 after rectify
            ret_xyz = np.dot(calib.Rect_cam_0, pt3d)

            # 3. if points not on image, then return None
            if ret_xyz[2] >= 0:
                # 6. Get projected coords
                pts2d_cam = np.dot(calib.P_cam_0, ret_xyz)
                return pts2d_cam / pts2d_cam[2]
            else:
                return None
    else:
        raise ValueError('frame_calib must be an LidarCamCalibData type')


def load_pc_from_file(v_f):
    return np.fromfile(v_f, dtype=np.float32, count=-1).reshape([-1, 4])


# ------------------------------ Drawing utilities ------------------------------------------

