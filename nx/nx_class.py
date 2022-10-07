# -*- coding: utf-8 -*-
import os

import NXOpen as Nx
import NXOpen.Features as Ftr

from NXOpen import SectionCollection as SecCol
from symbol import parameters


class NX:
    """
    A class provides methods to create Siemens NX objects

    Methods
    -------
    import_files(in_file=None, out_file=None, in_file_type='iges')
        Imports iges file and saves it to prt format
    create_prt_file(iges_file: str, prt_dir: str)
        Opens an iges file and saves it to the prt_dir folder
    close_all(prt_file: str)
        Saves and closes all modified files
    create_new_nx_file(**parameters)
        Creates new NX prt file with the set parameters
    add_part_to_assembly(part, assembly_file=None)
        Adds prt file to an assembly file
    create_spline_with_points(**parameters)
        Creates studio spline object with the set parameters
    through_curves(**parameters)
        Creates solid or sheet body passing through curves with the set parameters
    swept(**parameters)
        Creates solid or sheet body with swept method with the set parameters
    """

    session = None
    ui = None

    def __init__(self, **kwargs):
        """
        Constructs necessary attributes for handling NX Objects

        :param self.session: A NX current session
        :param self.new_file: A NXOpen NewFile Class for handling
        new nx file
        """

        self.session = Nx.Session.GetSession()
        self.new_file = self.session.Parts.FileNew()
        self.units = kwargs.get('units', 1.0)

    def import_file(self, in_file=None, out_file=None, in_file_type='iges'):
        """
        Imports file iges format (or another type file) and saves it to prt format
        :param in_file: File that will be imported to new NX file (str)
        :param out_file: File in which in_file will be saved (str)
        :param in_file_type: Type of input file (str)
        :return: Logging message (str)
        """

        if in_file:
            if in_file_type == 'iges':
                iges_importer = self.session.DexManager.CreateIgesImporter()
                iges_importer.CopiousData = Nx.IgesImporter.CopiousDataEnum.LinearNURBSpline
                iges_importer.SmoothBSurf = True
                iges_importer.LayerDefault = 10
                iges_importer.InputFile = in_file
                iges_importer.OutputFile = out_file
                iges_importer.FileOpenFlag = False
                iges_importer.LayerMask = "0-99999"
                try:
                    iges_importer.Commit()
                    iges_importer.Destroy()
                    msg = "Iges file {} has " \
                          "been successfully imported.".format(os.path.split(out_file)[1])
                    msg += "\nOutput file {}".format(out_file)
                    return msg
                except Nx.NXException as ex:
                    msg = "Iges file {} has not been imported.".format(os.path.split(out_file)[1])
                    msg += "An error occurred: {}.".format(str(ex))
                    return msg

    def create_prt_file(self, igs_file: str, prt_dir: str):

        """
        Create new NX prt file from an iges file
        :param igs_file: Input iges file (str)
        :param prt_dir: Full directory name in which prt file will be saved
        :return: Bool, str
            True if file has been created or False otherwise and logging message
        """

        prt_file = os.path.splitext(os.path.split(igs_file)[1])[0] + '.prt'
        prt_file = os.path.join(prt_dir, prt_file)

        try:
            base_part, part_load_status = self.session.Parts.OpenBase(igs_file)
            part_load_status.Dispose()
        except Nx.NXException as ex:
            msg = "Trying to open file '{}'. ".format(igs_file) + str(ex)
            return False, msg

        if part_load_status:
            try:
                part_save_status = base_part.SaveAs(prt_file)
                part_save_status.Dispose()
                msg = "File '{}' has been successfully created.".format(prt_file)
                close_modified = Nx.BasePart.CloseModified.CloseModified
                self.session.Parts.CloseAll(close_modified, None)
                return True, msg
            except Nx.NXException as ex:
                msg = "Trying to save '{}'. ".format(os.path.split(prt_file)[1]) + str(ex)
                return False, msg

    def close_all(self, prt_file):

        """
        Closes all parts of NX Work Part Object
        :param prt_file: File that will be closed
        :return: Bool, str
            True if file has been closed or False otherwise and logging message
        """

        whole_tree = Nx.BasePart.SaveComponents.TrueValue
        close_modified = Nx.BasePart.CloseAfterSave.FalseValue
        work_part = self.session.Parts.Work

        try:
            save_status = work_part.Save(whole_tree, close_modified)
            save_status.Dispose()
            self.session.Parts.CloseAll(Nx.BasePart.CloseModified.CloseModified, None)
            work_part = Nx.Part.Null
            msg = "File {} has been successfully saved and closed.".format(prt_file)
            return True, msg
        except Nx.NXException as ex:
            msg = "Trying to save and close file '{}'. An error occurred {}.".format(prt_file, str(ex))
            return False, msg

    def create_new_nx_file(self, **parameters):

        """
        Creates new NX file
        :param file_name: str
            Creating file name
        :param template: srt,
            Sets the name of the template part from which the new
            file being created
        :param app_name: str,
            Sets the application type for the new file being created
        :param tmp_presentation_name: str,
            Sets the presentation name of the underlying template
            which is used for the new file being created
        :return: Bool, str
            True if NewFile Class has been created successfully or False otherwise
            and logging message
        """

        file_name = parameters.get('file_name', None)
        template = parameters.get('template', 'model-plain-1-mm-template.prt')
        app_name = parameters.get('app_name', 'ModelTemplate')

        if file_name:
            self.new_file.NewFileName = file_name
            self.new_file.TemplateFileName = template
            self.new_file.ApplicationName = app_name
            self.new_file.UseBlankTemplate = False
            self.new_file.Units = Nx.Part.Units.Millimeters
            self.new_file.RelationType = ""
            self.new_file.TemplateType = Nx.FileNewTemplateType.Item
            self.new_file.ItemType = ""
            self.new_file.MasterFileName = ""
            self.new_file.SetCanCreateAltrep(False)

            try:
                nx_obj_file = self.new_file.Commit()
                file_name = os.path.split(file_name)[1]
                msg = "File '{}' has been successfully created.".format(file_name)
                self.new_file.Destroy()
                return True, msg
            except Nx.NXException as ex:
                file_name = os.path.split(file_name)[1]
                msg = "File '{fn}' has not been created. An error occurred: " \
                    "{expt}".format(fn=file_name, expt=str(ex))
                return False, msg

    def add_part_to_assembly(self, part, assembly_file=None):

        """
        Creates ComponentBuilder Class for adding an assembly part and
        adds an assembly part to an assembly
        :param part: str,
            Full part file name which is being added
        :param assembly_file: str,
            Full assembly file name in which part is being added
        :return: False or Tagged Object and logging message
        """

        if assembly_file:
            self.session.ApplicationSwitchImmediate("UG_APP_MODELING")

            work_part = self.session.Parts.Work
            component_name = os.path.splitext(os.path.split(part)[1])[0]
            component_builder = work_part.AssemblyManager.CreateAddComponentBuilder()
            component_pos = work_part.ComponentAssembly.Positioner
            component_pos.ClearNetwork()
            component_pos.BeginAssemblyConstraints()
            allow_interpart_positioning = self.session.Preferences.Assemblies.InterpartPositioning
            component_network = component_pos.EstablishNetwork()
            component_network.MoveObjectsState = True
            component_builder.SetInitialLocationType(
                Nx.Assemblies.AddComponentBuilder.LocationType.WorkPartAbsolute
            )
            component_builder.SetComponentAnchor(
                Nx.Assemblies.ProductInterface.InterfaceObject.Null
            )
            component_builder.Layer = 10
            component_builder.ReferenceSet = "Use Model"
            component_builder.ComponentName = component_name

            base_part, part_load_status = self.session.Parts.Open(part)
            part_load_status.Dispose()

            part_to_use = [Nx.BasePart.Null] * 1
            part_to_use[0] = base_part
            component_builder.SetPartsToAdd(part_to_use)
            component_network.Solve()
            work_part.AssignPermanentName(assembly_file)

            try:
                nx_obj_builder = component_builder.Commit()
                obj_tag = nx_obj_builder.Tag
                component_builder.Destroy()
                component_pos.ClearNetwork()
                msg = "Part {} has been successfully added.".format(part)
                return obj_tag, msg
            except Nx.NXException as ex:
                msg = "Error committing component {}. ".format(part) + str(ex)
                return False, msg

    def create_spline_with_points(self, **parameters):

        """
        Creates StudioSplineBuilder for drawing a spline from points
        and draws Studio Spline
        :param curve_points: list,
            A list of curve points in format
            [[x0, y0, z0], [x1, y1, z1], ... [xn, yn, zn]]
        :param spline_degree: int,
            Degree of spline curve
        :param matched_knot: Bool,
            Placed knots only where you locate defining points
        :param spline_type: str,
            Can take two values ThroughPoints or ByPoles
        :param closed_spline: Bool,
            If spline has to be closed or not
        :return: False or Tagged object and logging message
        """

        curve_points = parameters.get('points', None)
        spline_degree = parameters.get('degree', 3)
        matched_knot = parameters.get('matched_knot', True)
        spline_type = parameters.get('spline_type', 'ThroughPoints')
        closed_spline = parameters.get('closed_spline', True)
        name = parameters.get('name', False)

        if curve_points:
            work_part = self.session.Parts.Work
            studio_spline_builder = work_part.Features.CreateStudioSplineBuilderEx(Nx.NXObject.Null)

            if matched_knot:
                studio_spline_builder.MatchKnotsType = Ftr.StudioSplineBuilderEx.MatchKnotsTypes.Cubic
            else:
                studio_spline_builder.MatchKnotsType = Ftr.StudioSplineBuilderEx.MatchKnotsTypes.NotSet

            if spline_type == 'ThroughPoints':
                studio_spline_builder.Type = Ftr.StudioSplineBuilderEx.Types.ThroughPoints
            elif spline_type == 'ByPoles':
                studio_spline_builder.Type = Ftr.StudioSplineBuilderEx.Types.ByPoles
            else:
                studio_spline_builder.Type = Ftr.StudioSplineBuilderEx.Types.NotSet

            studio_spline_builder.Degree = spline_degree
            studio_spline_builder.IsPeriodic = closed_spline

            for point in curve_points:
                x, y, z = point[0], point[1], point[2]

                try:
                    x, y, z = float(x), float(y), float(z)
                    x *= self.units
                    y *= self.units
                    z *= self.units
                except ValueError:
                    msg = "Coordinates value x: {x}, y: {y}, z: {z}. ".format(x=x, y=y, z=z)
                    msg += "Data type mismatches."
                    return False, msg

                coordinates = Nx.Point3d(x, y, z)
                spline_point = work_part.Points.CreatePoint(coordinates)
                geometric_constraint_data = studio_spline_builder.ConstraintManager.CreateGeometricConstraintData()
                geometric_constraint_data.Point = spline_point
                studio_spline_builder.ConstraintManager.Append(geometric_constraint_data)
            try:
                nx_object = studio_spline_builder.Commit()
                obj_tag = nx_object.Tag
                studio_spline = nx_object
                if name:
                    studio_spline.SetName(name)
                else:
                    studio_spline.SetName('spline')

                studio_spline_builder.Destroy()
                msg = "Studio spline has been successfully created."
                return obj_tag, msg
            except Nx.NXException as ex:
                msg = "Studio spline has not been created. An error occurred {}.".format(str(ex))
                return False, msg

    def through_curves(self, **parameters):

        """
        Create solid body or surfaces through  curves
        :param parameters: dict;
            :parameter: section_curves: curves tags dict
            :parameter: preserve_shape: bool allows to keep shape edges
            :parameter: help_points: list of helping points for the constraint
            :parameter: check_direction: bool is the directions of all sections should be checked
            :parameter: surface_type: str ThroughCurves object or StudioSurface object
                        need to be created
            :parameter: distance_tolerance: float=0.01 sets the distance tolerance
            :parameter: chaining_tolerance: float=0.0095 sets the chaining tolerance
            :parameter: angle_tolerance: float=0.5 sets the angle tolerance
        :return: False or Tagged Object and logging message.
        """

        section_curves = parameters.get('sections', [])
        preserve_shape = parameters.get('preserve_shape', False)
        help_points = parameters.get(
            'help_points', [[-100/self.units, -100/self.units, -100/self.units]]*len(section_curves)
        )
        check_directions = parameters.get('check_directions', False)
        surface_type = parameters.get('surface_type', 'through_curves')
        align_points = parameters.get('align_points', [0.0, 0.0, 0.0] * len(section_curves))
        use_spine_curve = parameters.get('use_spine_curve', False)
        spine_curve = parameters.get('spine_curve', None)
        spine_help_point = parameters.get('spine_help_point', None)

        set_start_and_direction = parameters.get('set_start_and_direction', False)
        direction = parameters.get('direction')

        distance_tolerance = parameters.get('distance_tolerance', 0.01)
        chaining_tolerance = parameters.get('chaining_tolerance', 0.0095)
        angle_tolerance = parameters.get('angle_tolerance', 0.5)

        if section_curves:
            work_part = self.session.Parts.Work
            self.session.Preferences.Modeling.BodyType
            if surface_type == 'studio_surface':
                builder = work_part.Features.CreateStudioSurfaceBuilder(Ftr.Feature.Null)
                builder.BodyPreference = Ftr.ThroughCurvesBuilder.BodyPreferenceTypes.Sheet
                builder.AlignmentMethod.AlignCurve.DistanceTolerance = distance_tolerance
                builder.AlignmentMethod.AlignCurve.ChainingTolerance = chaining_tolerance
                builder.AlignmentMethod.AlignCurve.AngleTolerance = angle_tolerance
                builder.PositionTolerance = distance_tolerance
            elif surface_type == 'through_curves':
                builder = work_part.Features.CreateThroughCurvesBuilder(Ftr.Feature.Null)
                builder.BodyPreference = Ftr.ThroughCurvesBuilder.BodyPreferenceTypes.Sheet
                builder.PreserveShape = preserve_shape

                if use_spine_curve:
                    builder.Alignment.AlignType = Nx.GeometricUtilities.AlignmentMethodBuilder.Type.SpineCurve
                    builder.LoftingSurfaceRebuildData.RebuildType = Nx.GeometricUtilities.Rebuild.RebuildTypes.Advanced

                builder.PatchType = Nx.Features.ThroughCurvesBuilder.PatchTypes.Multiple
                builder.Alignment.AlignCurve.DistanceTolerance = distance_tolerance
                builder.Alignment.AlignCurve.ChainingTolerance = chaining_tolerance
                builder.Alignment.AlignCurve.AngleTolerance = angle_tolerance
                builder.SectionTemplateString.DistanceTolerance = distance_tolerance
                builder.SectionTemplateString.ChainingTolerance = chaining_tolerance
                builder.SectionTemplateString.AngleTolerance = angle_tolerance
                builder.PositionTolerance = distance_tolerance
            else:
                builder = work_part.Features.CreateThroughCurvesBuilder(Ftr.Feature.Null)

            # Set secionts
            sections = []
            for i, (obj, point) in enumerate(zip(section_curves, align_points)):
                help_point = [p * self.units for p in help_points[i]]
                help_point = Nx.Point3d(*help_points[i])

                curves_ = [Nx.IBaseCurve.Null] * len(obj)
                for i, c in enumerate(obj):
                    curves_[i] =  Nx.TaggedObjectManager.GetTaggedObject(c)
                rule = [work_part.ScRuleFactory.CreateRuleBaseCurveDumb(curves_)]

                section = work_part.Sections.CreateSection(
                    chaining_tolerance, distance_tolerance, angle_tolerance
                )
                section.AllowSelfIntersection(False)
                section.SetAllowedEntityTypes(Nx.Section.AllowTypes.CurvesAndPoints)
                curve = Nx.TaggedObjectManager.GetTaggedObject(obj[0])
                section.AddToSection(
                    rule, curve, Nx.NXObject.Null, Nx.NXObject.Null,
                    help_point, Nx.Section.Mode.Create, False
                )

                if set_start_and_direction:
                    dir = direction[i]
                    try:
                        pt = [p * self.units for p in point]
                        curve = section.GetStartAndDirection()[0]
                        section.SetStartAndDirection(curve, Nx.Point3d(*pt), Nx.Vector3d(*dir))
                        section.DistanceTolerance = distance_tolerance
                        section.ChainingTolerance = chaining_tolerance
                        builder.SectionsList.Append(section)
                        sections.append(section)
                    except Nx.NXException as ex:
                        print(str(ex))
                        section.Destroy()
                else:
                    section.DistanceTolerance = distance_tolerance
                    section.ChainingTolerance = chaining_tolerance
                    builder.SectionsList.Append(section)
                    sections.append(section)

            if surface_type == 'studio_spline':
                builder.AlignmentMethod.SetSections(sections)
            else:
                builder.Alignment.SetSections(sections)

            if preserve_shape:
                on_path_dim_builders = []
                builder.Alignment.ComputeDefaultPoints()
                on_path_dim_builders = []
                for i, sec in enumerate(sections):
                    num_points = builder.Alignment.NumberOfPointsPerSection
                    for j in range(num_points):
                        on_path_dim_builder = builder.Alignment.GetPoint(i, j)
                        builder.Alignment.RemovePoint(on_path_dim_builder)
                for point, sec in zip(align_points, sections):
                    pt = [p * self.units for p in point]
                    nx_pt = work_part.Points.CreatePoint(Nx.Point3d(*pt))
                    on_path_dim_builder = builder.Alignment.CreateOnPathDimBuilder(sec, Nx.Point3d(*pt))
                    on_path_dim_builder.ThroughPoint = nx_pt
                    if on_path_dim_builder.IsFlipped:
                        print(on_path_dim_builder.IsFlipped)
                        on_path_dim_builder.IsFlipped = False
                    on_path_dim_builder.Update(
                        Nx.GeometricUtilities.OnPathDimensionBuilder.UpdateReason.ThroughPoint
                    )
                    on_path_dim_builders.append(on_path_dim_builder)

            if use_spine_curve:
                builder.Alignment.AlignCurve.SetAllowedEntityTypes(Nx.Section.AllowTypes.OnlyCurves)
                builder.Alignment.AlignCurve.AllowSelfIntersection(True)
                builder.Alignment.AlignCurve.AddToSection
                nx_spine_curve = Nx.TaggedObjectManager.GetTaggedObject(spine_curve)
                feature_spine = [nx_spine_curve]
                curve_feature_rule = work_part.ScRuleFactory.CreateRuleCurveFeature(feature_spine)
                spine_rules = [curve_feature_rule]
                spine_help_point = [p * self.units for p in spine_help_point]
                nx_spine_help_point = Nx.Point3d(*spine_help_point)
                builder.Alignment.AlignCurve.AddToSection(
                    spine_rules, Nx.NXObject.Null, Nx.NXObject.Null, Nx.NXObject.Null,
                    nx_spine_help_point, Nx.Section.Mode.Create, False
                )

            for section in sections:
                direction = section.GetStartAndDirection()
                # Set same direction for all sections
                if check_directions:
                    if direction[2].Z < 0:
                        section.ReverseDirection()

            try:
                nx_object = builder.CommitFeature()
                nx_object.HideParents()
                obj_tag = nx_object.Tag
                builder.Destroy()
                msg = 'Through curves object has been created successfully'
                return obj_tag, msg
            except Nx.NXException as ex:
                builder.Destroy()
                msg = 'Through curves object has not been created. An error occurred: {}'.format(str(ex))
                return False, msg

    def swept(self, **parameters):

        """
        Create solid body through swept method
        :param parameters: dict
            :parameter: section_curves: dict of tagged objects, studio splines of the sections curves
            :parameter: guide_curves: dict of tagged objects, studio splines of the guide curves
            :parameter: section_help_points: list of section help points for the constrain
            :parameter: guide_help_points: list of guide help points for the constrain
            :parameter: preserve_shape: bool allows to keep shape edges
            :parameter: distance tolerance: float=0.01 sets the distance tolerance
            :parameter: chaining_tolerance: float=0.0095 sets the chaining tolerance
            :parameter: g0_tolerance: float=0.01 sets the G0 (Position) tolerance
            :parameter: g1_tolerance: float=0.5 sets the G1 (Tangent) tolerance
        :return: False or Tagged Object and logging message
        """

        section_curves = parameters.get('sections', [])
        guide_curves = parameters.get('guides', [])
        section_help_points = parameters.get('section_help_points', None)
        guide_help_points = parameters.get('guide_help_points', None)
        preserve_shape = parameters.get('preserve_shape', False)
        align_points = parameters.get('align_points', None)
        
        direction = parameters.get('direction')
        set_direction = parameters.get('set_direction', False)

        distance_tolerance = parameters.get('distance_tolerance', 0.01)
        chaining_tolerance = parameters.get('chaining_tolerance', 0.0095)
        angle_tolerance = parameters.get('angle_tolerance', 0.5)
        g0_tolerance = parameters.get('g0', 0.01)
        g1_tolerance = parameters.get('g1', 0.5)

        if section_curves and guide_curves:
            work_part = self.session.Parts.Work
            self.session.Preferences.Modeling.BodyType

            # Create object of SweptBuilder class
            builder = work_part.Features.CreateSweptBuilder(Ftr.Swept.Null)
            builder.InterpolationOption = Ftr.SweptBuilderInterpolationOptions.Linear
            builder.G0Tolerance = g0_tolerance
            builder.G1Tolerance = g1_tolerance
            builder.PreserveShapeOption = preserve_shape

            # Spine tolerances
            builder.Spine.DistanceTolerance = distance_tolerance
            builder.Spine.ChainingTolerance = chaining_tolerance
            builder.Spine.AngleTolerance = angle_tolerance

            builder.OrientationMethod.AngularLaw.AlongSpineData.Spine.DistanceTolerance = distance_tolerance
            builder.OrientationMethod.AngularLaw.AlongSpineData.Spine.ChainingTolerance = chaining_tolerance
            builder.OrientationMethod.AngularLaw.AlongSpineData.Spine.AngleTolerance = angle_tolerance

            builder.ScalingMethod.AreaLaw.AlongSpineData.Spine.DistanceTolerance = distance_tolerance
            builder.ScalingMethod.AreaLaw.AlongSpineData.Spine.ChainingTolerance = chaining_tolerance
            builder.ScalingMethod.AreaLaw.AlongSpineData.Spine.AngleTolerance = angle_tolerance

            builder.ScalingMethod.PerimeterLaw.AlongSpineData.Spine.DistanceTolerance = distance_tolerance
            builder.ScalingMethod.PerimeterLaw.AlongSpineData.Spine.ChainingTolerance = chaining_tolerance
            builder.ScalingMethod.PerimeterLaw.AlongSpineData.Spine.AngleTolerance = angle_tolerance

            # Section tolerances
            builder.AlignmentMethod.AlignCurve.DistanceTolerance = distance_tolerance
            builder.AlignmentMethod.AlignCurve.ChainingTolerance = chaining_tolerance
            builder.AlignmentMethod.AlignCurve.AngleTolerance = angle_tolerance

            builder.OrientationMethod.OrientationCurve.DistanceTolerance = distance_tolerance
            builder.OrientationMethod.OrientationCurve.ChainingTolerance = chaining_tolerance
            builder.OrientationMethod.OrientationCurve.AngleTolerance = angle_tolerance

            builder.OrientationMethod.AngularLaw.LawCurve.DistanceTolerance = distance_tolerance
            builder.OrientationMethod.AngularLaw.LawCurve.ChainingTolerance = chaining_tolerance
            builder.OrientationMethod.AngularLaw.LawCurve.AngleTolerance = angle_tolerance

            builder.ScalingMethod.AreaLaw.LawCurve.DistanceTolerance = distance_tolerance
            builder.ScalingMethod.AreaLaw.LawCurve.ChainingTolerance = chaining_tolerance
            builder.ScalingMethod.AreaLaw.LawCurve.AngleTolerance = angle_tolerance

            builder.ScalingMethod.ScalingCurve.DistanceTolerance = distance_tolerance
            builder.ScalingMethod.ScalingCurve.ChainingTolerance = chaining_tolerance
            builder.ScalingMethod.ScalingCurve.AngleTolerance = angle_tolerance

            builder.ScalingMethod.PerimeterLaw.LawCurve.DistanceTolerance = distance_tolerance
            builder.ScalingMethod.PerimeterLaw.LawCurve.ChainingTolerance = chaining_tolerance
            builder.ScalingMethod.PerimeterLaw.LawCurve.AngleTolerance = angle_tolerance

            if preserve_shape:
                builder.AlignmentMethod.AlignType = Nx.GeometricUtilities.AlignmentMethodBuilder.Type.Points
                builder.PreserveGuideShapeOption = True

            # Create features, section and guide curves
            features = []
            sections = []
            guides_features = []

            # Setting sections
            for i, (obj, point) in enumerate(zip(section_curves, align_points)):
                studio_spline = Nx.TaggedObjectManager.GetTaggedObject(obj)
                spline = studio_spline.GetEntities()[0]
                hp = [point * self.units for point in section_help_points[i]]
                help_point = Nx.Point3d(*hp)
                feature = [Ftr.Feature.Null] * 1
                feature[0] = studio_spline
                features.append(spline)
                rule = [work_part.ScRuleFactory.CreateRuleCurveFeature(feature)]

                section = work_part.Sections.CreateSection(
                    chaining_tolerance, distance_tolerance, angle_tolerance
                )
                section.AllowSelfIntersection(False)
                section.SetAllowedEntityTypes(Nx.Section.AllowTypes.CurvesAndPoints)

                section.AddToSection(
                    rule, spline, Nx.NXObject.Null, Nx.NXObject.Null,
                    help_point, Nx.Section.Mode.Create, False
                )
                if set_direction:
                    dir = direction[i]
                    try:
                        pt = [p * self.units for p in point]
                        curve = section.GetStartAndDirection()[0]
                        section.SetStartAndDirection(curve, Nx.Point3d(*pt), Nx.Vector3d(*dir))
                        builder.SectionList.Append(section)
                        sections.append(section)
                    except Nx.NXException as ex:
                        print(str(ex))
                        section.Destroy()

                else:
                    builder.SectionList.Append(section)
                    sections.append(section)


            # Setting guide curves
            for i, obj in enumerate(guide_curves):

                guide_spline = Nx.TaggedObjectManager.GetTaggedObject(obj)
                spline = guide_spline.GetEntities()[0]
                ghp = [p * self.units for p in guide_help_points[i]]
                help_point = Nx.Point3d(*ghp)
                feature = [Ftr.Feature.Null] * 1
                feature[0] = guide_spline
                guides_features.append(spline)
                rule = [work_part.ScRuleFactory.CreateRuleCurveFeature(feature)]

                section = work_part.Sections.CreateSection(
                    chaining_tolerance, distance_tolerance, angle_tolerance
                )
                builder.GuideList.Append(section)
                section.AllowSelfIntersection(True)
                section.SetAllowedEntityTypes(Nx.Section.AllowTypes.OnlyCurves)
                section.AddToSection(
                    rule, spline, Nx.NXObject.Null, Nx.NXObject.Null,
                    help_point, Nx.Section.Mode.Create, False
                )

                builder.ScalingMethod.AreaLaw.AlongSpineData.SetFeatureSpine(section)
                builder.ScalingMethod.PerimeterLaw.AlongSpineData.SetFeatureSpine(section)
                builder.OrientationMethod.AngularLaw.AlongSpineData.SetFeatureSpine(section)

            builder.ScalingMethod.ScalingOption = Nx.GeometricUtilities.ScalingMethodBuilder.ScalingOptions.Uniform
            builder.AlignmentMethod.SetSections(sections)

            builder.AlignmentMethod.ComputeDefaultPoints()
            if preserve_shape:
                on_path_dim_builders = []
                for i, sec in enumerate(sections):
                    num_points = builder.AlignmentMethod.NumberOfPointsPerSection
                    for j in range(num_points):
                        on_path_dim_builder = builder.AlignmentMethod.GetPoint(i, j)
                        builder.AlignmentMethod.RemovePoint(on_path_dim_builder)
                for point, sec in zip(align_points, sections):
                    pt = [p * self.units for p in point]
                    nx_pt = work_part.Points.CreatePoint(Nx.Point3d(*pt))
                    on_path_dim_builder = builder.AlignmentMethod.CreateOnPathDimBuilder(sec, Nx.Point3d(*pt))
                    on_path_dim_builder.ThroughPoint = nx_pt
                    on_path_dim_builder.Update(
                        Nx.GeometricUtilities.OnPathDimensionBuilder.UpdateReason.ThroughPoint
                    )
                    on_path_dim_builders.append(on_path_dim_builder)

                builder.AlignmentMethod.SetAlignPoints(on_path_dim_builders)

            builder.Validate()
            try:
                nx_object = builder.Commit()
                obj_tag = nx_object.Tag
                nx_object.HideParents()
                msg = 'Swept object has been created successfully.'
                return obj_tag, msg
            except Nx.NXException as ex:
                msg = 'Swept object has not been created. An error occured {}'.format(str(ex))
                return False, msg

    def create_plane(self, method: int=1, **kwargs):
        
        angle_tolerance = kwargs.get('angle_tolerance', 0.5)
        distance_tolerance = kwargs.get('distance_tolerance', 0.01)
        chaining_tolerance = kwargs.get('chaining_tolerance', 0.0095)

        work_part = self.session.Parts.Work
        datum_plane_builder = work_part.Features.CreateDatumPlaneBuilder(Nx.Features.Feature.Null)
        plane = datum_plane_builder.GetPlane()

        if method == 1:
            point = kwargs.get('point')
            point = [p * self.units for p in point]
            spline = kwargs.get('spline')
            if not (point or spline):
                msg = 'Plane at point {} through {} has not been created.'.format(point, spline)
                return False, msg

            plane.SetUpdateOption(Nx.SmartObject.UpdateOption.WithinModeling)
            section = work_part.Sections.CreateSection(
                chaining_tolerance, distance_tolerance, angle_tolerance
            )
            section.SetAllowedEntityTypes(Nx.Section.AllowTypes.OnlyCurves)

            nx_studio_spline = Nx.TaggedObjectManager.GetTaggedObject(spline)
            nx_spline = nx_studio_spline.GetEntities()[0]

            feature = [nx_studio_spline]
            rule = [work_part.ScRuleFactory.CreateRuleCurveFeatureTangent(
                feature, nx_spline, Nx.Curve.Null, False, 0.0095, 0.5)]

            section.AllowSelfIntersection(False)
            help_point = Nx.Point3d(*point)
            nx_point = work_part.Points.CreatePoint(help_point)
            section.AddToSection(rule, nx_spline, Nx.NXObject.Null, Nx.NXObject.Null,
                help_point, Nx.Section.Mode.Create, False)
            plane.SetMethod(Nx.PlaneTypes.MethodType.Frenet)
            geometry = [section, nx_point]
            plane.SetGeometry(geometry)
            plane.SetFrenetSubtype(Nx.PlaneTypes.FrenetSubtype.ThruPoint)
            plane.SetReverseSection(False)
            plane.SetAlternate(Nx.PlaneTypes.AlternateType.One)
            plane.SetFlip(True)

            try:
                datum_plane_builder = datum_plane_builder.CommitFeature()
                datum_plane = datum_plane_builder.DatumPlane
                plane_tag = datum_plane.Tag
                msg = 'Plane through point {} tangent to curve {} has' \
                ' been successfully creates.'.format(point, nx_studio_spline)
                return plane_tag, msg
            except Nx.NXException as ex:
                msg = 'Plane through point {} tangent to curve {} has not' \
                ' been creates. An error occurred{}'.format(point, nx_studio_spline, str(ex))
                return False, msg

    def create_sketch(self, **kwargs):
        
        work_part = self.session.Parts.Work
        datum = kwargs.get('datum', None)
        datum_axis = kwargs.get('datum_axis', [1.0, 0.0, 0.0])

        if not datum:
            msg = 'Sketch has not been created'
            return False, msg
        else:
            nx_datum = Nx.TaggedObjectManager.GetTaggedObject(datum)

        origin = kwargs.get('origin', [0.0, 0.0, 0.0])
        origin = [p * self.units for p in origin]
        normal = kwargs.get('normal', [0.0, 0.0, 1.0])
        normal = [p * self.units for p in normal]

        sketch_builder = work_part.Sketches.CreateSketchInPlaceBuilder2(Nx.Sketch.Null)

        nx_origin = Nx.Point3d(*origin)
        nx_normal = Nx.Vector3d(*normal)
        nx_point = work_part.Points.CreatePoint(nx_origin)

        datum_axis = work_part.Datums.FindObject("DATUM_CSYS(0) X axis")
        direction = work_part.Directions.CreateDirection(
            datum_axis, Nx.Sense.Forward, Nx.SmartObject.UpdateOption.WithinModeling
        )

        xform = work_part.Xforms.CreateXformByPlaneXDirPoint(
            nx_datum, direction, nx_point, Nx.SmartObject.UpdateOption.WithinModeling, 1.0, False, False
        )
        cartesian_system = work_part.CoordinateSystems.CreateCoordinateSystem(
            xform, Nx.SmartObject.UpdateOption.WithinModeling
        )
        sketch_builder.Csystem = cartesian_system
        plane = work_part.Planes.CreatePlane(nx_origin, nx_normal, Nx.SmartObject.UpdateOption.WithinModeling)
        plane.SetMethod(Nx.PlaneTypes.MethodType.Coincident)
        plane.SetGeometry([nx_datum])
        sketch_builder.Csystem = cartesian_system
        sketch_builder.PlaneReference = plane
        sketch_builder.SketchOrigin = nx_point
        
        try:
            nx_sketch = sketch_builder.Commit()
            msg = 'Sketch object has successfully been created.'
            nx_sketch_tag = nx_sketch.Tag
            return nx_sketch_tag, msg
        except Nx.Exception as ex:
            msg = 'Sketch object has not been created. An error occurred {}.'.format(str(ex))
            return False, msg

    def join_curves(self, **kwargs):

        shapes = kwargs.get('shapes', ['line'])
        distance_tolerance = kwargs.get('distance_tolerance', 0.01)
        angle_tolerance = kwargs.get('angle_tolerance', 0.5)
        sec_distance_tolerance = kwargs.get('sec_distance_tolerance', 0.01)
        sec_chaining_tolerance = kwargs.get('sec_chaining_tolerance', 0.0095)
        sec_angle_tolerance = kwargs.get('angle_tolerance', 0.5)
        suppress = kwargs.get('suppress', True)

        work_part = self.session.Parts.Work

        join_curve_builder = work_part.Features.CreateJoinCurvesBuilder(Nx.Features.Feature.Null)
        join_curve_builder.DistanceTolerance = distance_tolerance
        join_curve_builder.AngleTolerance = angle_tolerance
        join_curve_builder.Section.DistanceTolerance = sec_distance_tolerance
        join_curve_builder.Section.AngleTolerance = sec_angle_tolerance
        join_curve_builder.Section.ChainingTolerance = sec_chaining_tolerance
        join_curve_builder.Section.SetAllowedEntityTypes(Nx.Section.AllowTypes.OnlyCurves)

        curves = []
        tagged_curves = []
        for shape, points in shapes.items():
            if shape == 'arc':
                for arc in points:
                    if arc:
                        points = arc
                        pt = [p * self.units for p in points[0]]
                        statr_pt = Nx.Point3d(*pt)
                        pt = [p * self.units for p in points[1]]
                        help_point = pt
                        point_on = Nx.Point3d(*pt)
                        pt = [p * self.units for p in points[2]]
                        end_point = Nx.Point3d(*pt)
                        nx_arc = work_part.Curves.CreateArc(statr_pt, point_on, end_point, False)
                        obj_tag = nx_arc[0].Tag
                        curves.append(nx_arc[0])
                        tagged_curves.append(obj_tag)
            elif shape == 'line':
                for line in points:
                    if line:
                        points = line
                        pt = [p * self.units for p in points[0]]
                        start_point = Nx.Point3d(*pt)
                        pt = [p * self.units for p in points[1]]
                        end_point = Nx.Point3d(*pt)
                        nx_line = work_part.Curves.CreateLine(start_point, end_point)
                        obj_tag = nx_line.Tag
                        curves.append(nx_line)
                        tagged_curves.append(obj_tag)

        curve_dumb_rule = [work_part.ScRuleFactory.CreateRuleBaseCurveDumb(curves)]

        nx_help_point = Nx.Point3d(*help_point)
        join_curve_builder.Section.AddToSection(
            curve_dumb_rule, curves[0], Nx.NXObject.Null, Nx.NXObject.Null, nx_help_point,
            Nx.Section.Mode.Create, False
        )
        try:
            nx_obj = join_curve_builder.Commit()
            if suppress:
                nx_obj.Suppress()
            nx_obj.HideParents()
            msg = 'Join curve has been created'
            return nx_obj.Tag, tagged_curves, msg
        except Nx.Exception as ex:
            msg = 'Join curve has not been created. An error occurred {}'.format(str(ex))
            return False, False, msg
