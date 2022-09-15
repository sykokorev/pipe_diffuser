import sys
import json
import logging

from nx.nx_class import NX
import NXOpen



if __name__ == "__main__":

    json_file = sys.argv[0]
    
    with open(json_file, 'r') as fi:
        json_data = json.load(fi)

    twist = json_data['twist']
    cross_sections = json_data['cross_sections']
    mean_line = json_data['mean_line']
    prt_file = json_data['prt']


    nx = NX()
    is_created, log_new_file = nx.create_new_nx_file(file_name=prt_file)
    print(log_new_file)
    if is_created:
        nx.create_spline_with_points(
            points=mean_line, 
            name='mean_line', 
            coeff=25.4,
            closed_spline=False
            )
        nx.close_all(prt_file=prt_file)
