""" GUI for AR Davinci"""
# pylint: disable=too-many-instance-attributes, no-self-use
# pylint: disable=fixme, attribute-defined-outside-init
# pylint: disable=no-name-in-module, too-many-public-methods
import os

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QSlider, QVBoxLayout, QHBoxLayout, \
                              QLabel, QPushButton, \
                              QMessageBox, QApplication, \
                              QCheckBox, QWidget

class UI(QWidget):
    """User interface class, to combine vtk render
     view with buttons/sliders etc"""

    exit_signal = Signal()

    def __init__(self, overlay_window):
        """Constructor

        :param overlay_window: vtk_overlay_window that will be displayed
        in the UI.
        """

        super().__init__()

        self.child_windows = []
        self.vtk_models = []

        self.layout = QVBoxLayout(self)

        # Container for buttons at the bottom of the layout
        self.controls_vbox = QVBoxLayout()
        self.opacity_box = QHBoxLayout()
        self.visiblity_buttons = QHBoxLayout()
        self.other_buttons = QVBoxLayout()

        self.add_vtk_overlay_window(overlay_window)
        self.add_opacity_slider()
        self.layout.addLayout(self.visiblity_buttons)
        self.layout.addLayout(self.other_buttons)
        self.add_exit_button()
        self.add_record_buttons()
        self.add_crop_buttons()

        self.screen = None
        self.screen_geometry = None

        self.show()

    def add_vtk_overlay_window(self, overlay_window):
        """ Add the vtk_overlay_window to the UI layout.

        :param overlay_window: vtk_overlay_window
        """

        self.interactor_layout = QHBoxLayout()
        self.vtk_overlay = overlay_window.vtk_overlay_window

        self.interactor_layout.addWidget(self.vtk_overlay)
        self.layout.addLayout(self.interactor_layout)

    def add_opacity_slider(self):
        """Create a QSlider that controls VTK model opactity"""
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setSliderPosition(100)
        self.opacity_slider.valueChanged.connect(self.set_all_opacities)

        label = QLabel('Opacity')

        self.opacity_box.addWidget(label)
        self.opacity_box.addWidget(self.opacity_slider)

        self.layout.addLayout(self.opacity_box)

    def add_exit_button(self):
        """Add a button to exit the program"""
        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.on_exit_clicked)
        style_sheet = "QPushButton {background-color: rgb(155, 155, 155)}"
        self.exit_button.setStyleSheet(style_sheet)
        self.other_buttons.addWidget(self.exit_button)

    def add_record_buttons(self):
        """ Add buttons to take screenshot and record video.
        Button callbacks should be implmenented in the Viewer class. """
        self.screenshot_button = QPushButton('Take screenshot')

        self.record_button = QPushButton('Record video')

        self.record_buttons_layout = QHBoxLayout()
        self.record_buttons_layout.addWidget(self.screenshot_button)
        self.record_buttons_layout.addWidget(self.record_button)
        self.other_buttons.addLayout(self.record_buttons_layout)

    def add_crop_buttons(self):
        """ Add buttons to crop the video stream. """
        self.crop_buttons_layout = QHBoxLayout()
        self.crop_button = QPushButton('Crop')
        self.autocrop_button = QPushButton('Enable Auto Crop')

        self.crop_buttons_layout.addWidget(self.crop_button)
        self.crop_buttons_layout.addWidget(self.autocrop_button)
        self.other_buttons.addLayout(self.crop_buttons_layout)

    def on_exit_clicked(self):
        """ Close the application when the exit button has been clicked"""

        msg_box = QMessageBox()
        msg_box.setText("Do you want to quit?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)

        ret = msg_box.exec_()

        if ret == QMessageBox.Yes:
            self.exit_signal.emit()
            QApplication.exit()

    def add_vtk_models(self, vtk_models):
        """ Add VTK models to the UI and vtk_overlay_window

        :param vtk_models: List of vtk models to add
        :type vtk_models: List of VTKSurfaceModels
        """

        self.vtk_models = vtk_models
        self.vtk_overlay.add_vtk_models(self.vtk_models)

        for model in vtk_models:
            checkbox = self.create_toggle_checkbox_for_model(model)
            checkbox.clicked.connect(model.toggle_visibility)
            self.visiblity_buttons.addWidget(checkbox)

    def create_toggle_checkbox_for_model(self, model):
        """Create a checkbox that will toggle on/off model visiblity.

        :param model: VTKSurfaceModel
        :return: QCheckBox
        """

        # Parse model name from filename
        filename_no_path = os.path.basename(model.name)
        name, _ = os.path.splitext(filename_no_path)
        # Format nicely for display
        button_text = name.capitalize().replace('_', ' ')

        checkbox = QCheckBox(button_text)
        checkbox.setStyleSheet("QCheckBox {font: 12pt}")
        checkbox.setChecked(True)

        return checkbox

    def add_toggle_stereo_button(self):
        """ Add button to switch between L and R views"""
        toggle_button = QPushButton('Toggle L/R View')
        toggle_button.clicked.connect(self.toggle_stereo_view)
        self.visiblity_buttons.addWidget(toggle_button)

    def set_all_opacities(self, opacity_percent):
        """Set the opacity for all VTK models

        :param opacity_percent: Target opacity value, in %
        :type opacity_percent: int
        """

        opacity = opacity_percent / 100
        for vtk_model in self.vtk_models:
            vtk_model.set_opacity(opacity)

    def set_screen(self, screen):
        """Link the widget to a particular screen

        :param screen: QGuiQpplication.screen() object
        """

        self.screen = screen
        self.move(screen.geometry().x(), screen.geometry().y())
