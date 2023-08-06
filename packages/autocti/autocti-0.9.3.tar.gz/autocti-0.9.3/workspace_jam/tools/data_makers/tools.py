from autocti.charge_injection import ci_frame

def normalization_from_ci_data_resolution(ci_data_resolution):
    return [100.0, 500.0, 1000.0, 5000.0, 10000.0, 25000.0, 50000.0, 84700.0]

def parallel_ci_regions_from_ci_data_resolution(ci_data_resolution):
    shape = parallel_shape_from_ci_data_resolution(ci_data_resolution=ci_data_resolution)
    return [(0, 30, 51, shape[1]-20), (330, 360, 51, shape[1]-20),
              (660, 690, 51, shape[1]-20), (990, 1020, 51, shape[1]-20),
              (1320, 1350, 51, shape[1]-20), (1650, 1680, 51, shape[1]-20),
              (1980, 2010, 51, shape[1]-20)]


def serial_ci_regions_from_ci_data_resolution(ci_data_resolution):
    shape = serial_shape_from_ci_data_resolution(ci_data_resolution=ci_data_resolution)
    return [(0, shape[0], 51, shape[1]-20)]

def parallel_shape_from_ci_data_resolution(ci_data_resolution):

    if ci_data_resolution is 'high_resolution':
        return (2316, 2119)
    elif ci_data_resolution is 'mid_resolution':
        return (2316, 1034)
    elif ci_data_resolution is 'low_resolution':
        return (2316, 517)

def parallel_frame_geometry_from_ci_data_resolution(ci_data_resolution):

    if ci_data_resolution is 'high_resolution':
        return ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((2296, 2316, 51, 2099)),
                                                serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 2296, 2099, 2119)))

    elif ci_data_resolution is 'mid_resolution':
        return ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((2296, 2316, 51, 1014)),
                                                serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 2296, 1014, 1034)))

    elif ci_data_resolution is 'low_resolution':
        return ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((2296, 2316, 51, 497)),
                                                serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 2296, 497, 517)))

def serial_shape_from_ci_data_resolution(ci_data_resolution):

    if ci_data_resolution is 'high_resolution':
        return (2066, 2119)

    elif ci_data_resolution is 'mid_resolution':
        return (1033, 2119)

    elif ci_data_resolution is 'low_resolution':
        return (517, 2119)

def serial_frame_geometry_from_ci_data_resolution(ci_data_resolution):

    if ci_data_resolution is 'high_resolution':
        return ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((2296, 2316, 51, 2099)),
                                                serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 2296, 2099, 2119)))


    elif ci_data_resolution is 'mid_resolution':
        return ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((1138, 1158, 51, 2099)),
                                                serial_prescan=ci_frame.Region((0, 1158, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 1138, 2099, 2119)))


    elif ci_data_resolution is 'low_resolution':
        return ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                                parallel_overscan=ci_frame.Region((559, 579, 51, 2099)),
                                                serial_prescan=ci_frame.Region((0, 579, 0, 51)),
                                                serial_overscan=ci_frame.Region((0, 559, 2099, 2119)))

def parallel_and_serial_shape():
    return (2316, 2119)

def parallel_and_serial_frame_geometry():
    return ci_frame.FrameGeometry(corner=(0.0, 0.0),
                                            parallel_overscan=ci_frame.Region((2296, 2316, 51, 2099)),
                                            serial_prescan=ci_frame.Region((0, 2316, 0, 51)),
                                            serial_overscan=ci_frame.Region((0, 2296, 2099, 2119)))

def parallel_and_serial_ci_regions_from_ci_data_resolution():
    shape = parallel_and_serial_shape()
    return [(0, 30, 51, shape[1]-20), (330, 360, 51, shape[1]-20),
              (660, 690, 51, shape[1]-20), (990, 1020, 51, shape[1]-20),
              (1320, 1350, 51, shape[1]-20), (1650, 1680, 51, shape[1]-20),
              (1980, 2010, 51, shape[1]-20)]

def charge_line_shape_and_frame_geometry_from_direction(direction):

    if direction is 'parallel':

        shape = (2316, 1)
        frame_geometry = ci_frame.FrameGeometry.euclid_parallel_line()

        return shape, frame_geometry

    elif direction is 'serial':

        shape = (1, 2119)
        frame_geometry = ci_frame.FrameGeometry.euclid_serial_line()

        return shape, frame_geometry