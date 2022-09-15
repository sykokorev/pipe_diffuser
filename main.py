from statistics import mean
import sys
import os
import logging
import subprocess
import json

import utils.p1112_parser as p1112
from mathlib.math import *
from mathlib.bezier import *
from mathlib.line_interpolation import LineInterpolation
from diffuser.pipe_diffuser import PipeDiffuser as diffuser
from utils.open_file import *
from utils.utils import find_nx_journal_run


if __name__ == "__main__":

    indata_file = select_file(
        filetypes=(('p1112 Data Files', '*.p1112'), ('All Files', '*.*')),
        initialdir='/',
        title='Open p1112 Indata File'
    )

    logger = logging.getLogger(__name__)
    logger_file = 'diffuser.log'
    if os.path.exists(logger_file):
        os.remove(logger_file)
    logging.basicConfig(filename=logger_file, level=logging.DEBUG)

    saveas = save_file_as(title='Save NX model file')
    outdata_dir = os.path.join(os.path.split(saveas)[0], 'outdata')
    
    if not os.path.exists(outdata_dir):
        try:
            os.mkdir(outdata_dir)
        except FileExistsError as ex:
            msg = 'Directory has not been created an error occurs {ex}'
            logger.exception(msg)

    if not (os.path.exists(indata_file)):
        msg = 'File {file} doesn\'t exist'.format(file=os.path.abspath(indata_file))
        logger.error(msg)
        sys.exit(msg)

    # Parsing p1112 file
    # Input parameters
    indata, exception = p1112.input_parameters_p1112(in_file=indata_file)
    if not indata:
        msg = 'While parsing input parameters an error occurred {ex}'.format(ex=exception)
        logger.error(msg)
        sys.exit(msg)

    # Distributions
    # Data for mean line
    xr, exception = p1112.distribution(in_file=indata_file, string=r'x-r\s+\w+')
    if not exception:
        msg = 'X-R distribution has not been found. Input data will be applied.'
        logger.info(msg)

    xbeta, exeption = p1112.distribution(in_file=indata_file, string=r'x-beta\s+\w+')
    if not exception:
        msg = 'X-BETA distribution has not been found. Input data will be applied.'
        logger.info(msg)

    # Data for cross section
    wh, exeption = p1112.distribution(in_file=indata_file, string=r'w\W+h\s+\w+')
    if not exception:
        msg = 'WH distribution has not been found. Input data will applied.'
        logger.info(msg)

    area, exception = p1112.distribution(in_file=indata_file, string=r'area\s+\w+')
    if not exception:
        msg = 'Area distribution has not been found. Input data will applied.'
        logger.info(msg)

    twist, exception = p1112.distribution(in_file=indata_file, string=r'twist\s+\w+')
    if not exception:
        msg = 'Twist distribution has not been found. Input data will applied.'
        logger.info(msg)

    # x linear distribution
    x0, x1 = xr[0][0], xr[-1][0]
    x = linspace(x0, x1, 100)
    xr_bezier = BezierThroughPoints(points=xr, npoints=2)
    xbeta_bezier = BezierThroughPoints(points=xbeta, npoints=2)
    wh_line = LineInterpolation(points=wh)
    area_line = LineInterpolation(points=area)
    twist_line = LineInterpolation(points=twist)

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
    twist_points = twist_line.interpolate(points=length)

    pipe_diffuser.lengths = length
    pipe_diffuser.wh = wh_points
    pipe_diffuser.area = area_points
    pipe_diffuser.twist = twist_points

    cross_sections = pipe_diffuser.compute_cross_sections()

    json_outdata = {
        "twist": twist_points,
        "mean_line": mean_line,
        "cross_sections": cross_sections,
        "prt": os.path.normpath(saveas)
    }

    outdata_file = os.path.join(outdata_dir, 'json_data.json')

    with open(outdata_file, 'w') as fo:
        json.dump(json_outdata, fo)

    nx_journal_run = find_nx_journal_run()

    if nx_journal_run:
        command = [nx_journal_run, "nx_builder.py", '-args', os.path.normpath(os.path.abspath(outdata_file))]
        code = subprocess.run(command)
