import sys
import json
import NXOpen


from nx.nx_class import NX


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
        print(msg)
        
        curves = []
        section_help_points = []
        for section in cross_sections:
            curves.append(
                nx.join_curves(
                shapes={
                    'arc': [section[1][0], section[1][1], section[1][2], section[1][3]],
                }, suppress=True
            ))
            section_help_points.append(section[1][0][1])

        arc_line = [curve[1] for curve in curves]
        body, msg = nx.through_curves(
            sections=arc_line, preserve_shape=True,
            align_points=section_help_points,
            distance_tolerance=10**-5,
            chaining_tolerance=9.5*10**-6
        )
        print(msg)

        tagged_curves = curves[-1][1]
        help_points = [point[0] for point in cross_sections[-1][1]]
        surface, msg = nx.fill_hole(curves=tagged_curves, help_points=help_points)
        print(msg)

        nx.close_all(prt_file=prt_file)
