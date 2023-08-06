from autocti.charge_injection import ci_frame

def parallel_shape_and_frame_geometry_from_ci_data_resolution(ci_data_resolution):

    if ci_data_resolution is 'high_resolution':

        shape = (2316, 2119)
        frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((2296, 2316, 51, 2099)),
                                                serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 2296, 2099, 2119)))

        return shape, frame_geometry

    elif ci_data_resolution is 'mid_resolution':

        shape = (2316, 1034)
        frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((2296, 2316, 51, 1014)),
                                                serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 2296, 1014, 1034)))

        return shape, frame_geometry

    elif ci_data_resolution is 'low_resolution':

        shape = (2316, 517)
        frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((2296, 2316, 51, 497)),
                                                serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 2296, 497, 517)))

        return shape, frame_geometry

def serial_shape_and_frame_geometry_from_ci_data_resolution(ci_data_resolution):

    if ci_data_resolution is 'high_resolution':

        shape = (2066, 2119)
        frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((2296, 2316, 51, 2099)),
                                                serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 2296, 2099, 2119)))

        return shape, frame_geometry

    elif ci_data_resolution is 'mid_resolution':

        shape = (1033, 2119)
        frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((1138, 1158, 51, 2099)),
                                                serial_prescan=ci_frame.Region((0, 1158, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 1138, 2099, 2119)))

        return shape, frame_geometry

    elif ci_data_resolution is 'low_resolution':

        shape = (517, 2119)
        frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((559, 579, 51, 2099)),
                                                serial_prescan=ci_frame.Region((0, 579, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 559, 2099, 2119)))

        return shape, frame_geometry

def parallel_and_serial_shape_and_frame_geometry():

    shape = (2316, 2119)
    frame_geometry = ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                            parallel_overscan=ci_frame.Region((2296, 2316, 51, 2099)),
                                            serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                            serial_overscan=ci_frame.Region((0, 2296, 2099, 2119)))

    return shape, frame_geometry

def charge_line_shape_and_frame_geometry_from_direction(direction):

    if direction is 'parallel':

        shape = (2316, 1)
        frame_geometry = ci_frame.FrameGeometry.euclid_parallel_line()

        return shape, frame_geometry

    elif direction is 'serial':

        shape = (1, 2119)
        frame_geometry = ci_frame.FrameGeometry.euclid_serial_line()

        return shape, frame_geometry