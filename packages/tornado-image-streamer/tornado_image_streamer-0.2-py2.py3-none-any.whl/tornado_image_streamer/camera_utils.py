"""TBW."""
from io import BytesIO

import numpy as np
from PIL import Image
import cv2


def convert_raw_image(raw):
    """TBW."""
    data = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(data)

    mem_file = BytesIO()
    im.save(mem_file, 'JPEG')
    return mem_file.getvalue()


class SimCam:
    """TBW."""

    counter = 0
    colors = [0.5, 0.75, 1.0]

    @staticmethod
    def simulate_image(w, h, dtype='uint16', shift=0, rgb=False):
        """Generate a 2d array of concentric circles.

        :param int w: the width in pixels
        :param int h: the height in pixels.
        :param str dtype: the pixel value data type
        :param int shift: the number of pixels to shift the final image.
        :param bool rgb: return a RGB (color) array.
        :return: a 2d numpy array of type uint8
        :rtype: ndarray
        """
        dx = 20.0 / w
        dy = 20.0 / h
        x = np.arange(-10, 10, dx)
        y = np.arange(-10, 10, dy)
        xx, yy = np.meshgrid(x, y, sparse=True)
        z = np.sin(xx ** 2 + yy ** 2) / (xx ** 2 + yy ** 2)
        z = np.nan_to_num(z)
        if z.min() < 0:
            z -= z.min()
        if dtype == 'uint16':
            z = (z / z.max()) * ((1 << 12) - 1)
        elif dtype == 'uint8':
            z = (z / z.max()) * ((1 << 8) - 1)
        z = z.astype(dtype)
        if shift > 0:
            z = np.roll(z, shift, axis=1)

        if rgb:
            SimCam.colors = np.array(SimCam.colors)
            SimCam.colors += 0.025
            SimCam.colors %= 1.0
            r = (z.astype(float) * SimCam.colors[0]).astype(dtype)
            g = (z.astype(float) * SimCam.colors[1]).astype(dtype)
            b = (z.astype(float) * SimCam.colors[2]).astype(dtype)
            return np.dstack((r, g, b))
        else:
            return z

    def read(self):
        """TBW."""
        SimCam.counter += 1
        data = SimCam.simulate_image(640, 480,
                                     dtype='uint8',
                                     shift=SimCam.counter,
                                     rgb=True)
        return True, data

    def read_image(self):
        """TBW."""
        ok, raw = self.read()
        return convert_raw_image(raw)


class WebCam(cv2.VideoCapture):
    """TBW."""

    def __init__(self, prop_id=0):
        """TBW."""
        super().__init__(prop_id)

    def read(self):
        """TBW."""
        return super().read()

    def read_image(self):
        """TBW."""
        ok, raw = self.read()
        return convert_raw_image(raw)
