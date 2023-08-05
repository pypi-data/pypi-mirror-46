""" Mono/Stereo viewing windows for Ardavinci"""
import logging
import datetime
from PySide2 import QtWidgets
from PySide2.QtCore import QTimer
from sksurgeryutils.common_overlay_apps import \
     OverlayOnVideoFeedCropRecord, DuplicateOverlayWindow
from sksurgeryutils.utils.screen_utils import ScreenController
from sksurgerydavinci.ui.gui import UI
from sksurgerydavinci.davinci_xi_auto_cropping import AutoCropBlackBorder


LOGGER = logging.getLogger(__name__)

#pylin: disable= no-member, attribute-defined-outside-init
#pylin: disable=protected-access, no-self-use

class FakeOverlayOnVideoFeed:
    """ Implement empty methods to replicate OverlayOnVideoFeed. """

    def start(self):
        """ Intentionally Blank. """

    def stop(self):
        """ Intentionally Blank. """

    def on_record_start(self):
        """ Intentionally Blank. """

    def on_record_stop(self):
        """ Intentionally Blank. """

    def set_roi(self):
        """ Intentionally Blank. """


class FakeVTKOverlayWindow:
    """ Implement empty methods to replicate VTKOverlayWindow. """
    def save_scene_to_file(self, fname):
        """ Intentionally Blank. """

    def get_foreground_camera(self):
        """ Intentionally Blank. """

    def set_foreground_camera(self, camera):
        """ Intentionally Blank. """

    def set_screen(self):
        """ Intentionally Blank. """

    def set_geometry(self):
        """ Intentionally Blank. """

    def add_vtk_models(self, models):
        """ Intentionally Blank. """


class StereoViewerBase(QtWidgets.QWidget):
    """
    Base class for StereoViewers.

    Child classes implment the left/right/ui video feeds as appropriate.
    """

    def __init__(self):
        super().__init__()

        self.primary_screen = None
        self.all_screens = None
        self.num_additional_screens = None

        self.UI.screenshot_button.clicked.connect(self.on_screenshot_clicked)
        self.UI.record_button.clicked.connect(self.on_record_start_clicked)
        self.UI.crop_button.clicked.connect(self.on_crop_clicked)
        self.UI.autocrop_button.clicked.connect(self.on_autocrop_started)
        self.UI.exit_signal.connect(self.run_before_quit)

        self.auto_cropper = AutoCropBlackBorder(threshold=5)
        self.autocrop_timer = QTimer()
        self.autocrop_timer.timeout.connect(self.update_autocrop)

        self.sync_camera_view_between_windows()

    def sync_camera_view_between_windows(self):
        """
        Set all the foreground cameras to the same vtkCamera,
        so that camera changes are synchronised.
        """
        camera = self.left_overlay.get_foreground_camera()
        self.right_overlay.set_foreground_camera(camera)
        self.ui_overlay.set_foreground_camera(camera)

    def set_external_screens(self, output_screens):
        """
         Set the display screens for each widget, if
        external monitors are available.

        :param output_screens: List of screens on which to put widgets
        :type output_screens:   List of ints
        """
        screen_controller = ScreenController()
        self.primary_screen, self.all_screens = \
            screen_controller.list_of_screens()

        self.num_additional_screens = len(self.all_screens)

        if self.sufficent_displays_for_stereo_view():
            self.set_widget_screens(output_screens)

    def sufficent_displays_for_stereo_view(self):
        """
        Check if there are enough additional displays to
        give each window it's own screen.
        """
        return self.num_additional_screens >= 2

    def set_widget_screens(self, screens_to_use):
        """
        Move each of the widgets to a particular screen.
        If each widget is on it's own screen, run fullscreen.

        :param screens_to_use: List of QScreen objects.
        """
        ordered_screens = \
             [self.primary_screen, self.all_screens[0], self.all_screens[1]]

        UI_screen = ordered_screens[screens_to_use[0]-1]
        left_screen = ordered_screens[screens_to_use[1]-1]
        right_screen = ordered_screens[screens_to_use[2]-1]

        self.left_overlay.set_screen(left_screen)
        self.right_overlay.set_screen(right_screen)
        self.ui_overlay.set_screen(UI_screen)

        if self.are_widgets_on_different_screens(screens_to_use):
            self.maximize_left_and_right_widgets()

    def are_widgets_on_different_screens(self, screens):
        #pylint:disable=no-self-use
        """
        Check if each widget has been placed on it's own screen.
        :param screens: List of screen numbers corresponding to the screen
                        each widget is displayed on.
        :type screens: list of ints
        """

        unique_screens = set(screens)

        if len(unique_screens) == len(screens):
            return True

        return False

    def maximize_left_and_right_widgets(self):
        """
        Fullscreen view for each widget. QWidget.setFullScreen()
        isn't working properly in all cases, so resizing maunally instead.
        """

        self.left_overlay.setGeometry(self.left_overlay.screen.geometry())
        self.right_overlay.setGeometry(self.right_overlay.screen.geometry())

    def add_vtk_models(self, models):
        """Add VTK models to all widgets.

        :param models: List of models to add.
        :type models: VTKSurfaceModel
        """

        self.left_overlay.add_vtk_models(models)
        self.right_overlay.add_vtk_models(models)
        self.UI.add_vtk_models(models)

    def start(self):
        """
        Start all widgets.
        """

        self.left_view.start()
        self.right_view.start()
        self.ui_view.start()

    def run_before_quit(self):
        """
        Clean up the VTK interactor instances
        before quitting
        """

        self.left_view.stop()
        self.right_view.stop()
        self.ui_view.stop()

    def on_screenshot_clicked(self):
        """ Save a screenshot to disk, using date and time as filename """
        fname_base = 'outputs/' \
            + datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")

        if self.__class__.__name__ == "MonoViewer":
            fname_left = fname_base + '-MONO.png'

        else:
            fname_left = fname_base + '-LEFT.png'

        fname_right = fname_base + '-RIGHT.png'

        self.left_overlay.save_scene_to_file(fname_left)
        self.right_overlay.save_scene_to_file(fname_right)

    def on_record_start_clicked(self):
        """ Start recording a video. In the MockStereoViewer we only need
        to record the 'left' input, as the right view is a duplicate of the
        left.
        The proper StereoViewer class extends this method to also record
        the right view."""
        fname_base = 'outputs/' + \
            datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")

        if self.__class__.__name__ == "MonoViewer":
            fname_left = fname_base + '-MONO.avi'

        else:
            fname_left = fname_base + '-LEFT.avi'

        fname_right = fname_base + '-RIGHT.avi'

        self.left_view.output_filename = fname_left
        self.left_view.on_record_start()

        self.right_view.output_filename = fname_right
        self.right_view.on_record_start()

        self.UI.record_button.setText("Stop recording")
        self.UI.record_button.clicked.disconnect()
        self.UI.record_button.clicked.connect(self.on_record_stop_clicked)

    def on_record_stop_clicked(self):
        """ Stop recording data to file and restore button settings. """
        self.left_view.on_record_stop()
        self.right_view.on_record_stop()

        self.UI.record_button.setText("Record video")
        self.UI.record_button.clicked.disconnect()
        self.UI.record_button.clicked.connect(self.on_record_start_clicked)

    def on_crop_clicked(self):
        """ Set the ROI on the left view, and copy it to the right. """
        self.left_view.set_roi()
        self.right_view.roi = self.left_view.roi

    def on_autocrop_started(self):
        """ Start auto cropping. """
        self.UI.autocrop_button.setText("Disable Auto Crop")
        self.UI.autocrop_button.clicked.disconnect()
        self.UI.autocrop_button.clicked.connect(self.on_autocrop_stopped)
        self.autocrop_timer.start(500)

    def on_autocrop_stopped(self):
        """ Stop auto cropping. """
        self.UI.autocrop_button.setText("Enable Auto Crop")
        self.UI.autocrop_button.clicked.disconnect()
        self.UI.autocrop_button.clicked.connect(self.on_autocrop_started)
        self.autocrop_timer.stop()

        self.set_all_roi(None)

    def update_autocrop(self):
        """ Automatically crop the incoming video stream using AutoCropper.
        """
        roi = self.auto_cropper.get_roi(self.left_view.img)
        self.set_all_roi(roi)

    def set_all_roi(self, roi):
        """ Set the roi for left/right views. """
        self.left_view.roi = roi
        self.right_view.roi = roi

class MonoViewer(StereoViewerBase):
    """
    Generates a VTK interactor UI with a single video stream as background.
    :param video_source: OpenCV compatible video source (int or filename)

    Only use the left_view of StereoViewerBase. Set the other views to
    non-existent views.
    """
    def __init__(self, video_source):
        LOGGER.info("Creating Mono Viewer")
        self.left_view = OverlayOnVideoFeedCropRecord(video_source)
        self.left_overlay = self.left_view.vtk_overlay_window

        self.right_view = FakeOverlayOnVideoFeed()
        self.right_overlay = FakeVTKOverlayWindow()

        self.ui_view = FakeOverlayOnVideoFeed()
        self.ui_overlay = FakeVTKOverlayWindow()

        self.UI = UI(self.left_view)

        super().__init__()


class MockStereoViewer(StereoViewerBase):
    """
    Mock stereo viewer, duplicating a single camera input
    to multiple screens.

    :param video_source: OpenCV compatible video source (int or filename)
    """

    def __init__(self, video_source):

        LOGGER.info("Creating Mock Stereo Viewwer")
        self.left_view = OverlayOnVideoFeedCropRecord(video_source)
        self.left_overlay = self.left_view.vtk_overlay_window

        self.right_view = DuplicateOverlayWindow()
        self.right_view.set_source_window(self.left_view)
        self.right_overlay = self.right_view.vtk_overlay_window

        self.ui_view = DuplicateOverlayWindow()
        self.ui_view.set_source_window(self.left_view)
        self.ui_overlay = self.ui_view.vtk_overlay_window

        self.UI = UI(self.ui_view)

        super().__init__()

class StereoViewer(StereoViewerBase):
    """Stereo viewer, creates an overlay window for each
    video input.

    :param left_source: OpenCV compatible video source (int or filename)
    :param right_source: OpenCV compatible video source (int or filename)
    """

    def __init__(self, left_source, right_source):


        LOGGER.info("Creating Stereo Viewer")
        self.left_view = OverlayOnVideoFeedCropRecord(left_source)
        self.left_overlay = self.left_view.vtk_overlay_window

        self.right_view = OverlayOnVideoFeedCropRecord(right_source)
        self.right_overlay = self.right_view.vtk_overlay_window

        self.ui_view = DuplicateOverlayWindow()
        self.ui_view.set_source_window(self.left_view)

        self.ui_overlay = self.ui_view.vtk_overlay_window

        self.UI = UI(self.ui_view)

        super().__init__()
