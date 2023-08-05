# coding=utf-8

"""Hello world demo module"""
import sys
import vtk

from PySide2.QtWidgets import QApplication

from sksurgeryvtk.models.vtk_surface_model_directory_loader \
     import VTKSurfaceModelDirectoryLoader

from sksurgeryvtk.models.vtk_surface_model import VTKSurfaceModel

from sksurgerydavinci.widgets.Viewers\
     import MonoViewer, StereoViewer, MockStereoViewer


def run_demo(args):
    """Show message"""

    model_dir = args.model_dir
    video_sources = args.video_sources
    output_screens = args.output_screens
    app = QApplication([])

    if model_dir:
        model_loader = VTKSurfaceModelDirectoryLoader(model_dir)
        vtk_models = model_loader.models

    # No models provided, generate one to use
    else:
        vtk_models = create_sample_model()

    num_of_input_sources = len(video_sources)

    if num_of_input_sources == 1:
        viewer = MonoViewer(int(video_sources[0]))

    elif int(video_sources[1]) == -1:
        viewer = MockStereoViewer(int(video_sources[0]))
        viewer.set_external_screens(output_screens)

    else:
        left_source = int(video_sources[0])
        right_source = int(video_sources[1])

        viewer = StereoViewer(left_source, right_source)
        viewer.set_external_screens(output_screens)

    viewer.add_vtk_models(vtk_models)
    viewer.start()

    sys.exit(app.exec_())

def create_sample_model():
    """
    Create an empty VTKSurfaceModel object, and set the actor
    to a vtkConeSource
    """
    model = VTKSurfaceModel(None, (0.5, 0.5, 0.5))

    cone = vtk.vtkConeSource()
    cone.SetResolution(32)

    cone_mapper = vtk.vtkPolyDataMapper()
    cone_mapper.SetInputConnection(cone.GetOutputPort())

    cone_actor = vtk.vtkActor()
    cone_actor.SetMapper(cone_mapper)

    model.actor = cone_actor
    model.set_name("Cone")

    return [model]
