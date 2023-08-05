#coding=utf-8
""" AutoCropper Module. """

import numpy as np

class AutoCropBlackBorder:

    """ Class to generate a ROI for an image based on a threshold value.
    Originally developed for auto cropping video feed from the DaVinci Xi and
    Tile Pro, where there is a central image (which we want to keep), surrounded
    by a black region, and then other stuff that we're not interested in.

    By searching for the start/end of the black region, we can auto crop the
    bit we do want.

    For speed, only the red channel of the image is scanned when detecting
    black areas (See comment in set_roi for more details).

    :param threshold: Threshold value
    : param min_size: Minimum size (applies to both width and length)
                      of the expected output.

    """
    def __init__(self, threshold=1, min_size=0):
        self.min_size = min_size
        self.threshold = threshold
        self.roi = None

    def get_bounds(self, vector):
        """ Given a vector, skip any leading values that are > threshold,
        then find the first contiguous range of values that are below the
        threshold value.
        If the whole vector is above the threshold, return the start/end
        indexes.
        e.g.
        [0 0 0 50 50 50 0 0 0 ] return 3, 5 - [50 50 50]

        [25 25 0 0 25 25 25 0 0] returns 4, 7 [25 25 25] as the leading 25s are
        skipped.

        [100 100 100 100 100 100] returns 0, 5.

        :param vector: Input vector, in which to find the start/end bounds
        :return start: First element that is above the threshold.
        :return end: First element following start, that is below threshold.


        """

        # If the image starts with a non black area, skip this. We want
        # to start searching when the black border begins.
        skip = 0
        if vector[0] > self.threshold:
            skip = np.argmax(vector < self.threshold)

        start = skip + np.argmax(vector[skip:] > self.threshold)
        end = start + self.min_size + \
            np.argmax(vector[(start + self.min_size):] < self.threshold)

        # HANDLE EDGE CASES
        # argmax returns 0 if there is no match to the search criteria,
        # which can give incorrect results, so it is necessary to
        # identify some edge cases and act appropriately.

        # print(f"skip: {skip}, start: {start}, end: {end}")
        # There is a a border at the start, but not the end
        if start == end and start != skip:
            end = len(vector)

        # There is a border at the end, but not at the start
        if skip == start == end:
            start = 0

        # There is no border
        if skip == start == end == 0:
            end = len(vector)

        return start, end

    def get_roi(self, img):
        """ Calculate the ROI.
        Find the x/y extent of the ROI by averaging row and column values,
        and then finding the area of interest."""

        # Only use the red channel, otherwise we need to take the average along
        # two dimensions, which is slow. This should be acceptable for the
        # DaVinci.
        col_mean = np.mean(img[:, :, 1], axis=(0))
        row_mean = np.mean(img[:, :, 1], axis=(1))

        start_y, end_y = self.get_bounds(row_mean)
        start_x, end_x = self.get_bounds(col_mean)

        self.roi = []
        self.roi.append((start_x, start_y))
        self.roi.append((end_x, end_y))

        return self.roi
