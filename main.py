import sys
import os
import logging


import utils.p1112_parser as p1112
from mathlib.math import *
from mathlib.bezier import *
from mathlib.line_interpolation import LineInterpolation
from diffuser.pipe_diffuser import PipeDiffuser as diffuser


if __name__ == "__main__":

    file_1112 = nx.open_file(propmt_string='Open 1112 data file', title='Open 1112 File', filter='')

    logger = logging.getLogger(__name__)
    logger_file = 'diffuser.log'
    if os.path.exists(logger_file):
        os.remove(logger_file)
    logging.basicConfig(filename=logger_file, encoding='utf-8', level=logging.DEBUG)

    indata_directory = os.path.join('.', 'indata')
    indata_file_name = r'diffuser7-original.p1112'
    indata_file = os.path.join(indata_directory, indata_file_name)
    mean_line_file = os.path.join(indata_directory, 'mean_line.dat')

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
    # Data for mean line
    xr, exception = p1112.distribution(in_file=indata_file, string=r'x-r\s+\w+')
    if not exception:
        msg = f'X-R distribution has not been found. Input data will be applied.'
        logger.info(msg)

    xbeta, exeption = p1112.distribution(in_file=indata_file, string=r'x-beta\s+\w+')
    if not exception:
        msg = f'X-BETA distribution has not been found. Input data will be applied.'
        logger.info(msg)

    # Data for cross section
    wh, exeption = p1112.distribution(in_file=indata_file, string=r'w\W+h\s+\w+')
    if not exception:
        msg = f'WH distribution has not been found. Input data will applied.'
        logger.info(msg)

    area, exception = p1112.distribution(in_file=indata_file, string=r'area\s+\w+')

    # x linear distribution
    x0, x1 = xr[0][0], xr[-1][0]
    x = linspace(x0, x1, 100)

    xr_bezier = BezierThroughPoints(points=xr, npoints=2)
    xbeta_bezier = BezierThroughPoints(points=xbeta, npoints=2)
    wh_line = LineInterpolation(points=wh)
    area_line = LineInterpolation(points=area)

    norm_length = arange(start=0.0, stop=1.01, step=0.01)
    xr_points = [xr_bezier.norm_length_point(ni)[1] for ni in norm_length]
    xr_points = [[abs(round(xri[0], 4)), abs(round(xri[1], 4))] for xri in xr_points]

    xi = [p[0] for p in xr_points]
    xbeta_points = xbeta_bezier.interpolate(points=(0, xi))
    xbeta_points = [[round(b[0], 4), round(b[1], 4)] for b in xbeta_points]

    diffuser_params = {
        'xr': xr_points,
        'xbeta': xbeta_points,
        'length_star': float(indata['len_star']),
        'del_length_star': float(indata['del_len_star']),
        'rimp': float(indata['imp_tan_rad'])
    }

    pipe_diffuser = diffuser(**diffuser_params)
    mean_line = pipe_diffuser.compute_mean_line()
    mean_line = [[round(p[0], 4), round(p[1], 4), round(p[2], 4)] for p in mean_line]
    mean_line_length = pipe_diffuser.get_mean_line_length()
    length = [mean_line_length * nl for nl in norm_length]

    point = xbeta_bezier.get_point(point=(0, 3.5))

    wh_points = wh_line.interpolate(points=length)
    area_points = area_line.interpolate(points=length)

    cross_section = pipe_diffuser.compute_cross_section(
            wh=wh_points[20][1], area=area_points[20][1], num_points=200
        )
