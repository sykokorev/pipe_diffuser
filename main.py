from mailbox import linesep
import sys
import os
import logging

import utils.p1112_parser as p1112
from mathlib.math import *
from mathlib.bezier import *


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logger_file = 'diffuser.log'
    if os.path.exists(logger_file):
        os.remove(logger_file)
    logging.basicConfig(filename=logger_file, encoding='utf-8', level=logging.DEBUG)

    indata_directory = os.path.join('.', 'indata')
    indata_file_name = r'diffuser7-original.p1112'
    indata_file = os.path.join(indata_directory, indata_file_name)

    if not os.path.exists(indata_file):
        msg = f'File {os.path.abspath(indata_file)} doesn\'t exist'
        logger.error(msg)
        sys.exit(msg)

    # Parsing p1112 file
    # Input parameters
    indata, exception = p1112.input_parameters_p1112(in_file=indata_file)
    if not indata:
        msg = f'While parsing input parameters an error occurred {exception}'
        logger.error(msg)
        sys.exit(msg)

    # Distributions
    # Mean line distributions
    xr, exception = p1112.distribution(in_file=indata_file, string=r'x-r\s+\w+')
    if not exception:
        msg = f'X-R distribution has not been found. Input data will be applied.'
        logger.info(msg)

    xbeta, exeption = p1112.distribution(in_file=indata_file, string=r'x-beta\s+\w+')
    if not exception:
        msg = f'X-BETA distribution has not been found. Input data will be applied.'
        logger.info(msg)

    # x linear distribution
    x0, x1 = xr[0][0], xr[-1][0]
    x = linspace(x0, x1, 50)
    xr_bezier = BezierThroughPoints(points=xr, npoints=2)
    xbeta_bezier = BezierThroughPoints(points=xbeta, npoints=2)
    xr_coordinates = xr_bezier.get_coordinates()
        