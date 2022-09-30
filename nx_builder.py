import sys
import json
import logging
import NXOpen


from nx.nx_class import NX
import mathlib.vector as vc


if __name__ == "__main__":

    json_file = sys.argv[0]
    
    with open(json_file, 'r') as fi:
        json_data = json.load(fi)

    twist = json_data['twist']
    cross_sections = json_data['cross_sections']
    mean_line = json_data['mean_line']
    prt_file = json_data['prt']


    nx = NX(units=25.4)
    is_created, log_new_file = nx.create_new_nx_file(file_name=prt_file)

    if is_created:
        mean_line_tagged, msg = nx.create_spline_with_points(
            points=mean_line, 
            name='mean_line', 
            closed_spline=False
            )
        
        curves = []
        section_help_points = []
        guide_curves = [[], []]
        for section in cross_sections:
            curves.append(
                nx.join_curves(
                shapes={
                    'arc': [section[1][0], section[1][2]],
                    'line': [section[1][1], section[1][3]],
                }, suppress=True
            ))
            section_help_points.append(section[1][0][1])
            guide_curves[0].append(section[1][2][0])
            guide_curves[1].append(section[1][3][0])

        arc_line = [curve[1] for curve in curves]
        body, msg = nx.through_curves(sections=arc_line)

        # tagged_guide_curves = []
        # for i, curve in enumerate(guide_curves, 1):
        #     tagged_guide_curves.append(
        #         nx.create_spline_with_points(
        #             points=curve, 
        #             name='giude_curve_{}'.format(i), 
        #             closed_spline=False
        #         )[0]
        #     )

        # tagged_curves = [curve[0] for curve in curves]
        # guide_help_points = [
        #     guide_curves[0][0],
        #     guide_curves[1][0]
        # ]

        # body, msg = nx.swept(
        #     sections=tagged_curves, 
        #     set_direction=True,  direction=direction,
        #     guides=tagged_guide_curves,
        #     section_help_points=section_help_points, 
        #     guide_help_points=guide_help_points,
        #     preserve_shape=False, align_points=guide_curves[0]
        # )

        nx.close_all(prt_file=prt_file)
