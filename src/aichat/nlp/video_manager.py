from utils.app_utils import WebcamVideoStream
from utils.singleton import Singleton
from object_detection.constants import logging
import typing
import re


logger = logging.getLogger('object_detector')


@Singleton
class VideoManager:
    """
    Manages the lifecycle of incoming video streams
    """
    def __init__(self):
        """Constructor: Not called directly. """
        self.capture = None
        self.width = None
        self.height = None
        self.source = None

        logger.info('VideoManager initialized VideoStream on %s', self.source)

    def attach(self, capture: WebcamVideoStream):
        """Attaches a VideoStream to the manager"""

        self.capture = capture.start()
        self.width = capture.width
        self.height = capture.height
        self.source = capture.src

        logger.info('VideoManager initialized VideoStream on %s', self.source)

    def stop(self):
        """ Stops any VideoStream from consuming media. Brings VideoManager into stopped state."""
        if self.capture is None:
            return

        self.capture.stop()

        del self.capture
        self.capture = None

    def start(self, src: str):
        """Opens an new video stream with input URL.

        Args:
            src: A URL, used to compare with the instantiated video stream

        """
        if self.source != src:
            return

        if self.capture is not None:
            self.stop()

        self.capture = WebcamVideoStream(src=self.source,
                                         width=self.width,
                                         height=self.height)

        self.capture.stopped = False
        self.capture = self.capture.start()

        logger.info('VideoManager started new VideoStream on %s', src)

    def read(self):
        """Reads a frame from the Manager's current Video Stream.

        Returns:
            None - if there is no active video stream or the stream is stopped
            np.array(...) - A Numpy array containing a frame of video.

        """
        if self.capture is not None:
            return self.capture.read()
        return None

    def open(self):
        """Opens the cached source of the current VideoStream, if available."""
        if self.capture is not None and self.source is not None:
            self.capture.stream.open(self.source)

    @property
    def is_opened(self) -> bool:
        if self.capture is not None and not self.is_stopped:
            return self.capture.stream.isOpened()
        return False

    @property
    def is_stopped(self) -> bool:
        if self.capture is not None:
            return self.capture.stopped
        return True


_not_allowed_chars = re.compile(r'\W+', re.ASCII)


def build_video_url(user_id: typing.Union[int, str]) -> str:
    """ Construct a RSTP url from a User ID

    Args:
        user_id: the ID of the current user

    Returns:
        rtsp URL for the video stream

    Raises:
        ValueError -- occurs if user id contains invalid characters

    >>> build_video_url('1234')
    rtsp://52.39.224.108:1935/live/1234
    >>> build_video_url(1234)
    rtsp://52.39.224.108:1935/live/1234
    >>> build_video_url('AEX456')
    rtsp://52.39.224.108:1935/live/AEX456
    >>> build_video_url('*%$%')
    Traceback (most recent call last):
    ...
    ValueError: User ID must only contain [a-zA-Z0-9_]
    """

    tmpl = 'rtsp://52.39.224.108:1935/live/{}'
    user_id_str = str(user_id)

    has_invalid_chars = re.search(_not_allowed_chars, user_id_str) is not None

    if has_invalid_chars:
        raise ValueError('User ID must only contain [a-zA-Z0-9_]')

    return tmpl.format(user_id_str)


