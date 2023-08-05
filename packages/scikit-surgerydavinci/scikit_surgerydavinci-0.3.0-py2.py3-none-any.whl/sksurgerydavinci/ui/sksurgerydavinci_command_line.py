# coding=utf-8

"""Command line processing"""

import argparse
import logging
from sksurgerydavinci import __version__
from sksurgerydavinci.ui.sksurgerydavinci_demo import run_demo

LOGGER = logging.getLogger(__name__)

def main(args=None):
    """Entry point for ardavin application"""

    parser = argparse.ArgumentParser(description='ardavin')

    parser.add_argument(
        "-s",
        "--video_sources",
        required=False,
        default=[0],
        type=str,
        nargs='+',
        help="Video input source(s) (e.g. webcam/file). Default \
        source is 0 (webcam input). Usage: '-s 0 1'. \
        If two sources are given, the program will run in stereo\
        mode. Stereo mode can be tested with only one camera using: \
        '-s 0 -1'")

    parser.add_argument(
        "-o",
        "--output_screens",
        required=False,
        nargs='*',
        default=[1, 2, 3],
        type=int,
        help="Specify which screen(s) the outputs will be displayed on in \
        stereo mode. Usage: '-o UI_screen left_stereo right_stereo' \
        Default = '1 2 3'. 1 = Primary screen, 2 = Screen 2, 3 = Screen 3 etc.")

    parser.add_argument(
        "-m",
        "--model_dir",
        required=False,
        default=None,
        type=str,
        help="Location of directory containing models to be loaded")

    parser.add_argument(
        "-l",
        "--logging_debug",
        action="store_true",
        help="Enable Debug level logging"
    )

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "-v", "--version",
        action='version',
        version='ardavin version ' + friendly_version_string)

    args = parser.parse_args(args)

    if args.logging_debug:
        logging.basicConfig(level=logging.DEBUG)

    else:
        logging.basicConfig(level=logging.INFO)


    print(args)
    run_demo(args)
    