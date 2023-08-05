"""VidStab: a class for stabilizing video files"""

from .cv2_utils import safe_import_cv2
safe_import_cv2()  # inform user of pip install vidstab[cv2] if ModuleNotFoundError

import os
import time
import warnings
import cv2
import numpy as np
import imutils.feature.factories as kp_factory
import matplotlib.pyplot as plt
from . import general_utils
from . import vidstab_utils
from . import border_utils
from . import auto_border_utils
from . import plot_utils
from .frame_queue import FrameQueue
from . frame import Frame


class VidStab:
    """A class for stabilizing video files

    The VidStab class can be used to stabilize videos using functionality from OpenCV.
    Input video is read from file, put through stabilization process, and written to
    an output file.

    The process calculates optical flow (``cv2.calcOpticalFlowPyrLK``) from frame to frame using
    keypoints generated by the keypoint method specified by the user.  The optical flow will
    be used to generate frame to frame transformations (``cv2.estimateRigidTransform``).
    Transformations will be applied (``cv2.warpAffine``) to stabilize video.

    This class is based on the `work presented by Nghia Ho <http://nghiaho.com/?p=2093>`_

    :param kp_method: String of the type of keypoint detector to use. Available options are:
                        ``["GFTT", "BRISK", "DENSE", "FAST", "HARRIS", "MSER", "ORB", "STAR"]``.
                        ``["SIFT", "SURF"]`` are additional non-free options available depending
                        on your build of OpenCV.  The non-free detectors are not tested with this package.
    :param args: Positional arguments for keypoint detector.
    :param kwargs: Keyword arguments for keypoint detector.

    :ivar kp_method: a string naming the keypoint detector being used
    :ivar kp_detector: the keypoint detector object being used
    :ivar trajectory: a 2d showing the trajectory of the input video
    :ivar smoothed_trajectory: a 2d numpy array showing the smoothed trajectory of the input video
    :ivar transforms: a 2d numpy array storing the transformations used from frame to frame
    """

    def __init__(self, kp_method='GFTT', *args, **kwargs):
        """instantiate VidStab class

        :param kp_method: String of the type of keypoint detector to use. Available options are:
                        ``["GFTT", "BRISK", "DENSE", "FAST", "HARRIS", "MSER", "ORB", "STAR"]``.
                        ``["SIFT", "SURF"]`` are additional non-free options available depending
                        on your build of OpenCV.  The non-free detectors are not tested with this package.
        :param args: Positional arguments for keypoint detector.
        :param kwargs: Keyword arguments for keypoint detector.
        """

        self.kp_method = kp_method
        # use original defaults in http://nghiaho.com/?p=2093 if GFTT with no additional (kw)args
        if kp_method == 'GFTT' and args == () and kwargs == {}:
            self.kp_detector = kp_factory.FeatureDetector_create('GFTT',
                                                                 maxCorners=200,
                                                                 qualityLevel=0.01,
                                                                 minDistance=30.0,
                                                                 blockSize=3)
        else:
            self.kp_detector = kp_factory.FeatureDetector_create(kp_method, *args, **kwargs)

        self._smoothing_window = 30
        self._raw_transforms = []
        self._trajectory = []
        self.trajectory = self.smoothed_trajectory = self.transforms = None

        self.frame_queue = FrameQueue()
        self.prev_kps = self.prev_gray = None

        self.writer = None

        self.layer_options = {
            'layer_func': None,
            'prev_frame': None
        }

        self.border_options = {}
        self.auto_border_flag = False
        self.extreme_frame_corners = {'min_x': 0, 'min_y': 0, 'max_x': 0, 'max_y': 0}
        self.frame_corners = None

        self._default_stabilize_frame_output = None

    def _update_prev_frame(self, current_frame_gray):
        self.prev_gray = current_frame_gray[:]
        self.prev_kps = self.kp_detector.detect(self.prev_gray)
        # noinspection PyArgumentList
        self.prev_kps = np.array([kp.pt for kp in self.prev_kps], dtype='float32').reshape(-1, 1, 2)

    def _update_trajectory(self, transform):
        if not self._trajectory:
            self._trajectory.append(transform[:])
        else:
            # gen cumsum for new row and append
            self._trajectory.append([self._trajectory[-1][j] + x for j, x in enumerate(transform)])

    def _gen_next_raw_transform(self):
        current_frame = self.frame_queue.frames[-1]
        current_frame_gray = current_frame.gray_image

        # calc flow of movement
        optical_flow = cv2.calcOpticalFlowPyrLK(self.prev_gray,
                                                current_frame_gray,
                                                self.prev_kps, None)

        matched_keypoints = vidstab_utils.match_keypoints(optical_flow, self.prev_kps)
        transform_i = vidstab_utils.estimate_partial_transform(matched_keypoints)

        # update previous frame info for next iteration
        self._update_prev_frame(current_frame_gray)
        self._raw_transforms.append(transform_i[:])
        self._update_trajectory(transform_i)

    def _init_is_complete(self, gen_all):
        if gen_all:
            return False

        max_ind = min([self.frame_queue.max_frames,
                       self.frame_queue.max_len])

        if self.frame_queue.inds[-1] >= max_ind:
            return True

        return False

    def _process_first_frame(self, array=None):
        # read first frame
        _, _ = self.frame_queue.read_frame(array=array)
        # convert to gray scale
        prev_frame = self.frame_queue.frames[-1]
        prev_frame_gray = prev_frame.gray_image
        # detect keypoints
        prev_kps = self.kp_detector.detect(prev_frame_gray)
        # noinspection PyArgumentList
        self.prev_kps = np.array([kp.pt for kp in prev_kps], dtype='float32').reshape(-1, 1, 2)

        self.prev_gray = prev_frame_gray[:]

    def _init_trajectory(self, smoothing_window, max_frames, gen_all=False, show_progress=False):
        self._smoothing_window = smoothing_window

        if max_frames is None:
            max_frames = float('inf')

        frame_count = self.frame_queue.source_frame_count
        bar = general_utils.init_progress_bar(frame_count, max_frames, show_progress, gen_all)

        self._process_first_frame()

        # iterate through frames
        while True:
            # read current frame
            _, break_flag = self.frame_queue.read_frame(pop_ind=False)
            if not self.frame_queue.grabbed_frame:
                general_utils.update_progress_bar(bar, show_progress)
                break

            self._gen_next_raw_transform()

            if self._init_is_complete(gen_all):
                break

            general_utils.update_progress_bar(bar, show_progress)

        self._gen_transforms()

        return bar

    def _init_writer(self, output_path, frame_shape, output_fourcc, fps):
        # set output and working dims
        h, w = frame_shape

        # setup video writer
        self.writer = cv2.VideoWriter(output_path,
                                      cv2.VideoWriter_fourcc(*output_fourcc),
                                      fps, (w, h), True)

    def _set_border_options(self, border_size, border_type):
        functional_border_size, functional_neg_border_size = border_utils.functional_border_sizes(border_size)

        self.border_options = {
            'border_type': border_type,
            'border_size': functional_border_size,
            'neg_border_size': functional_neg_border_size,
            'extreme_frame_corners': self.extreme_frame_corners,
            'auto_border_flag': self.auto_border_flag
        }

    def _apply_transforms(self, output_path, max_frames, use_stored_transforms,
                          output_fourcc='MJPG', border_type='black', border_size=0,
                          layer_func=None, playback=False, progress_bar=None):

        self._set_border_options(border_size, border_type)
        self.layer_options['layer_func'] = layer_func

        while True:
            general_utils.update_progress_bar(progress_bar)
            i, break_flag = self.frame_queue.read_frame()

            if not self.frame_queue.frames_to_process() or break_flag:
                break

            if not use_stored_transforms:
                self._gen_next_raw_transform()

            transformed = self._apply_next_transform(i, use_stored_transforms=use_stored_transforms)

            if transformed is None:
                warnings.warn('Video is longer than available transformations; halting process.')
                break

            break_playback = general_utils.playback_video(transformed, playback,
                                                          delay=min([self._smoothing_window, max_frames]))
            if break_playback:
                break

            if self.writer is None:
                self._init_writer(output_path, transformed.shape[:2], output_fourcc,
                                  fps=self.frame_queue.source_fps)

            self.writer.write(transformed)

        self.writer.release()
        general_utils.update_progress_bar(progress_bar, finish=True)
        cv2.destroyAllWindows()

    def _gen_transforms(self):
        self.trajectory = np.array(self._trajectory)
        self.smoothed_trajectory = general_utils.bfill_rolling_mean(self.trajectory, n=self._smoothing_window)
        self.transforms = np.array(self._raw_transforms) + (self.smoothed_trajectory - self.trajectory)

    def gen_transforms(self, input_path, smoothing_window=30, show_progress=True):
        """Generate stabilizing transforms for a video

        This method will populate the following instance attributes: trajectory, smoothed_trajectory, & transforms.
        The resulting transforms can subsequently be used for video stabilization by using ``VidStab.apply_transforms``
        or ``VidStab.stabilize`` with ``use_stored_transforms=True``.

        :param input_path: Path to input video to stabilize.
                           Will be read with ``cv2.VideoCapture``; see opencv documentation for more info.
        :param smoothing_window: window size to use when smoothing trajectory
        :param show_progress: Should a progress bar be displayed to console?
        :return: Nothing; this method populates attributes of VidStab objects

        >>> from vidstab.VidStab import VidStab
        >>> stabilizer = VidStab()
        >>> stabilizer.gen_transforms(input_path='input_video.mov')
        >>> stabilizer.apply_transforms(input_path='input_video.mov', output_path='stable_video.avi')
        """
        self._smoothing_window = smoothing_window

        if not os.path.exists(input_path):
            raise FileNotFoundError(f'{input_path} does not exist')

        self.frame_queue.set_frame_source(cv2.VideoCapture(input_path))
        self.frame_queue.reset_queue(max_len=smoothing_window, max_frames=float('inf'))
        bar = self._init_trajectory(smoothing_window=smoothing_window,
                                    max_frames=float('inf'),
                                    gen_all=True,
                                    show_progress=show_progress)

        general_utils.update_progress_bar(bar, finish=True)

    def apply_transforms(self, input_path, output_path, output_fourcc='MJPG',
                         border_type='black', border_size=0, layer_func=None, show_progress=True, playback=False):
        """Apply stored transforms to a video and save output to file

        Use the transforms generated by ``VidStab.gen_transforms`` or ``VidStab.stabilize`` in stabilization process.
        This method is a wrapper for ``VidStab.stabilize`` with ``use_stored_transforms=True``;
        it is included for backwards compatibility.

        :param input_path: Path to input video to stabilize.
                           Will be read with ``cv2.VideoCapture``; see opencv documentation for more info.
        :param output_path: Path to save stabilized video.
                            Will be written with ``cv2.VideoWriter``; see opencv documentation for more info.
        :param output_fourcc: FourCC is a 4-byte code used to specify the video codec.
        :param border_type: How to handle negative space created by stabilization translations/rotations.
                            Options: ``['black', 'reflect', 'replicate']``
        :param border_size: Size of border in output.
                            Positive values will pad video equally on all sides,
                            negative values will crop video equally on all sides,
                            ``'auto'`` will attempt to minimally pad to avoid cutting off portions of transformed frames
        :param layer_func: Function to layer frames in output.
                           The function should accept 2 parameters: foreground & background.
                           The current frame of video will be passed as foreground,
                           the previous frame will be passed as the background
                           (after the first frame of output the background will be the output of
                           layer_func on the last iteration)
        :param show_progress: Should a progress bar be displayed to console?
        :param playback: Should the a comparison of input video/output video be played back during process?
        :return: Nothing is returned.  Output of stabilization is written to ``output_path``.

        >>> from vidstab.VidStab import VidStab
        >>> stabilizer = VidStab()
        >>> stabilizer.gen_transforms(input_path='input_video.mov')
        >>> stabilizer.apply_transforms(input_path='input_video.mov', output_path='stable_video.avi')
        """
        self.stabilize(input_path, output_path, smoothing_window=self._smoothing_window, max_frames=float('inf'),
                       border_type=border_type, border_size=border_size, layer_func=layer_func, playback=playback,
                       use_stored_transforms=True, show_progress=show_progress, output_fourcc=output_fourcc)

    def _apply_next_transform(self, i, use_stored_transforms=False):
        if not use_stored_transforms:
            self._gen_transforms()

        frame_i = self.frame_queue.frames.popleft()

        try:
            transform_i = self.transforms[i, :]
        except IndexError:
            return None

        transformed = vidstab_utils.transform_frame(frame_i,
                                                    transform_i,
                                                    self.border_options['border_size'],
                                                    self.border_options['border_type'])

        transformed, self.layer_options = vidstab_utils.post_process_transformed_frame(transformed,
                                                                                       self.border_options,
                                                                                       self.layer_options)

        transformed = transformed.cvt_color(frame_i.color_format)

        return transformed

    def stabilize_frame(self, input_frame, smoothing_window=30,
                        border_type='black', border_size=0, layer_func=None,
                        use_stored_transforms=False):
        """Stabilize single frame of video being iterated

        Perform video stabilization a single frame at a time.  Outputted stabilized frame will be on a
        ``smoothing_window`` delay.  When frames processed is ``< smoothing_window``, black frames will be returned.
        When frames processed is ``>= smoothing_window``, the stabilized frame ``smoothing_window`` ago will be
        returned.  When ``input_frame is None`` stabilization will still be attempted, if there are not frames left to
        process then ``None`` will be returned.

        :param input_frame: An OpenCV image (as numpy array) or None
        :param smoothing_window: window size to use when smoothing trajectory
        :param border_type: How to handle negative space created by stabilization translations/rotations.
                            Options: ``['black', 'reflect', 'replicate']``
        :param border_size: Size of border in output.
                            Positive values will pad video equally on all sides,
                            negative values will crop video equally on all sides,
                            ``'auto'`` will attempt to minimally pad to avoid cutting off portions of transformed frames
        :param layer_func: Function to layer frames in output.
                           The function should accept 2 parameters: foreground & background.
                           The current frame of video will be passed as foreground,
                           the previous frame will be passed as the background
                           (after the first frame of output the background will be the output of
                           layer_func on the last iteration)
        :param use_stored_transforms: should stored transforms from last stabilization be used instead of
                                      recalculating them?
        :return: 1 of 3 outputs will be returned:

            * Case 1 - Stabilization process is still warming up
                + **An all black frame of same shape as input_frame is returned.**
                + A minimum of ``smoothing_window`` frames need to be processed to perform stabilization.
                + This behavior was based on ``cv2.bgsegm.createBackgroundSubtractorMOG()``.
            * Case 2 - Stabilization process is warmed up and ``input_frame is not None``
                + **A stabilized frame is returned**
                + This will not be the stabilized version of ``input_frame``.
                  Stabilization is on an ``smoothing_window`` frame delay
            * Case 3 - Stabilization process is finished
                + **None**

        >>> from vidstab.VidStab import VidStab
        >>> stabilizer = VidStab()
        >>> vidcap = cv2.VideoCapture('input_video.mov')
        >>> while True:
        >>>     grabbed_frame, frame = vidcap.read()
        >>>     # Pass frame to stabilizer even if frame is None
        >>>     # stabilized_frame will be an all black frame until iteration 30
        >>>     stabilized_frame = stabilizer.stabilize_frame(input_frame=frame,
        >>>                                                   smoothing_window=30)
        >>>     if stabilized_frame is None:
        >>>         # There are no more frames available to stabilize
        >>>         break
        """
        self._set_border_options(border_size, border_type)
        self.layer_options['layer_func'] = layer_func

        # Store first frame
        if self.frame_queue.max_len is None:
            self.frame_queue.reset_queue(max_len=smoothing_window, max_frames=float('inf'))

            self._process_first_frame(array=input_frame)

            blank_frame = Frame(np.zeros_like(input_frame))
            blank_frame = border_utils.crop_frame(blank_frame, self.border_options)

            if self.border_options['border_size'] > 0:
                blank_frame_alpha, _ = vidstab_utils.border_frame(blank_frame,
                                                                  self.border_options['border_size'],
                                                                  self.border_options['border_type'])

                blank_frame_np = Frame(blank_frame_alpha).cvt_color(blank_frame.color_format)
                blank_frame = Frame(blank_frame_np)

            self._default_stabilize_frame_output = blank_frame.image

            return self._default_stabilize_frame_output

        if len(self.frame_queue.frames) == 0:
            return None

        if input_frame is not None:
            _, _ = self.frame_queue.read_frame(array=input_frame, pop_ind=False)
            if not use_stored_transforms:
                self._gen_next_raw_transform()

        if not self._init_is_complete(gen_all=False):
            return self._default_stabilize_frame_output

        stabilized_frame = self._apply_next_transform(self.frame_queue.i, use_stored_transforms=use_stored_transforms)

        return stabilized_frame

    def stabilize(self, input_path, output_path, smoothing_window=30, max_frames=float('inf'),
                  border_type='black', border_size=0, layer_func=None, playback=False,
                  use_stored_transforms=False, show_progress=True, output_fourcc='MJPG'):
        """Read video, perform stabilization, & write stabilized video to file

        :param input_path: Path to input video to stabilize.
                           Will be read with ``cv2.VideoCapture``; see opencv documentation for more info.
        :param output_path: Path to save stabilized video.
                            Will be written with ``cv2.VideoWriter``; see opencv documentation for more info.
        :param smoothing_window: window size to use when smoothing trajectory
        :param max_frames: The maximum amount of frames to stabilize/process.
                           The list of available codes can be found in fourcc.org.
                           See cv2.VideoWriter_fourcc documentation for more info.
        :param border_type: How to handle negative space created by stabilization translations/rotations.
                            Options: ``['black', 'reflect', 'replicate']``
        :param border_size: Size of border in output.
                            Positive values will pad video equally on all sides,
                            negative values will crop video equally on all sides,
                            ``'auto'`` will attempt to minimally pad to avoid cutting off portions of transformed frames
        :param layer_func: Function to layer frames in output.
                           The function should accept 2 parameters: foreground & background.
                           The current frame of video will be passed as foreground,
                           the previous frame will be passed as the background
                           (after the first frame of output the background will be the output of
                           layer_func on the last iteration)
        :param use_stored_transforms: should stored transforms from last stabilization be used instead of
                                      recalculating them?
        :param playback: Should the a comparison of input video/output video be played back during process?
        :param show_progress: Should a progress bar be displayed to console?
        :param output_fourcc: FourCC is a 4-byte code used to specify the video codec.
        :return: Nothing is returned.  Output of stabilization is written to ``output_path``.

        >>> from vidstab.VidStab import VidStab
        >>> stabilizer = VidStab()
        >>> stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')

        >>> stabilizer = VidStab(kp_method = 'ORB')
        >>> stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')
        """
        if border_size == 'auto':
            self.auto_border_flag = True

        if not os.path.exists(input_path):
            raise FileNotFoundError(f'{input_path} does not exist')

        self.frame_queue.set_frame_source(cv2.VideoCapture(input_path))

        # wait for camera to start up
        if isinstance(input_path, int):
            time.sleep(0.1)

        self.frame_queue.reset_queue(max_len=smoothing_window, max_frames=max_frames)

        if self.auto_border_flag and not use_stored_transforms:
            use_stored_transforms = True
            self.gen_transforms(input_path, smoothing_window=smoothing_window, show_progress=show_progress)
            self.frame_queue.set_frame_source(cv2.VideoCapture(input_path))
            self.frame_queue.reset_queue(max_len=smoothing_window, max_frames=max_frames)

            bar = general_utils.init_progress_bar(self.frame_queue.source_frame_count,
                                                  max_frames,
                                                  show_progress)
            self.frame_queue.populate_queue(smoothing_window)

        elif not use_stored_transforms:
            bar = self._init_trajectory(smoothing_window, max_frames, show_progress=show_progress)
        else:
            bar = general_utils.init_progress_bar(self.frame_queue.source_frame_count,
                                                  max_frames,
                                                  show_progress)
            self.frame_queue.populate_queue(smoothing_window)

        if self.auto_border_flag:
            frame_1 = self.frame_queue.frames[0]
            self.extreme_frame_corners = auto_border_utils.extreme_corners(frame_1.image, self.transforms)
            border_size = auto_border_utils.min_auto_border_size(self.extreme_frame_corners)

        self._apply_transforms(output_path, max_frames, use_stored_transforms=use_stored_transforms,
                               border_type=border_type, border_size=border_size,
                               layer_func=layer_func, playback=playback,
                               output_fourcc=output_fourcc, progress_bar=bar)

    def plot_trajectory(self):
        """Plot video trajectory

        Create a plot of the video's trajectory & smoothed trajectory.
        Separate subplots are used to show the x and y trajectory.

        :return: tuple of matplotlib objects ``(Figure, (AxesSubplot, AxesSubplot))``

        >>> from vidstab import VidStab
        >>> import matplotlib.pyplot as plt
        >>> stabilizer = VidStab()
        >>> stabilizer.gen_transforms(input_path='input_video.mov')
        >>> stabilizer.plot_trajectory()
        >>> plt.show()
        """
        return plot_utils.plot_trajectory(self.transforms, self.trajectory, self.smoothed_trajectory)

    def plot_transforms(self, radians=False):
        """Plot stabilizing transforms

        Create a plot of the transforms used to stabilize the input video.
        Plots x & y transforms (dx & dy) in a separate subplot than angle transforms (da).

        :param radians: Should angle transforms be plotted in radians?  If ``false``, transforms are plotted in degrees.
        :return: tuple of matplotlib objects ``(Figure, (AxesSubplot, AxesSubplot))``

        >>> from vidstab import VidStab
        >>> import matplotlib.pyplot as plt
        >>> stabilizer = VidStab()
        >>> stabilizer.gen_transforms(input_path='input_video.mov')
        >>> stabilizer.plot_transforms()
        >>> plt.show()
        """
        return plot_utils.plot_transforms(self.transforms, radians)
