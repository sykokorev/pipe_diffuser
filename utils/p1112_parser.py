import itertools
from utils.utils import Utils


def input_parameters_p1112(in_file: str) -> dict:
    
    foperate = Utils(in_file=in_file)

    input_parameter_values = []
    input_parameters_keys = [
        'num_pipes', 'diam_1st_sec', 'imp_tan_rad', 'tot_area_ratio',
        'len_star', 'del_len_star', 'radial_gap', 'cross_sec_gap', 'axial_length',
        'gg_inner_radius', 'r_exit_case', 'beta_init', 'x_swirl', 
        'cone_angle', 'cone_len', 'ml_wh', 'ml_twist', 'ml_cross_section_curve'
        ]

    index = foperate.find_string(string=r'input\s+parameters')
    for i in range(1, 4):
        input_parameter_values.append(foperate.get_line(index=index+i, split=True, sep=r'\s+'))

    input_parameter_values = list(itertools.chain(*input_parameter_values))

    try:
        input_parameter_values = [float(val) for val in input_parameter_values]
    except ValueError as ex:
        return ex, False

    out_dict = dict(zip(input_parameters_keys, input_parameter_values))

    return out_dict, True


def distribution(in_file: str, string: str) -> list:

    foperate = Utils(in_file=in_file)

    index = foperate.find_string(string=string)
    try:
        num_of_points = int(foperate.get_line(index=index+1))
    except ValueError as ex:
        return ex, False

    points = foperate.get_lines(start=index + 2, stop=index + num_of_points + 1, split=True, sep=' ')
    out = []
    try:
        for point in points:
            out.append([float(pi) for pi in point])
    except ValueError as ex:
        return ex, False
    return (out, True)
    
