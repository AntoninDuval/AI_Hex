import math

class Hex:
    def __init__(self, q, r):
        self.q = q
        self.r = r

class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def pixel_to_pointy_hex(pixel, size):
    q = (math.sqrt(3) / 3 * pixel.x - 1. / 3 * pixel.y) / size
    r = (2. / 3 * pixel.y) / size
    return hex_round(Hex(q, r))


def hex_round(hex):
    return cube_to_axial(cube_round(axial_to_cube(hex)))


def cube_to_axial(cube):
    q = cube.x
    r = cube.z
    return Hex(q, r)


def cube_round(cube):
    rx = round(cube.x)
    ry = round(cube.y)
    rz = round(cube.z)

    x_diff = abs(rx - cube.x)
    y_diff = abs(ry - cube.y)
    z_diff = abs(rz - cube.z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    else:
        if y_diff > z_diff:
            ry = -rx-rz
        else:
            rz = -rx-ry

    return Cube(rx, ry, rz)


def axial_to_cube(hex):
    x = hex.q
    z = hex.r
    y = -x - z
    return Cube(x, y, z)
