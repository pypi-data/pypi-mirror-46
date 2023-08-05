#!/usr/bin/env python3

# Copyright (c) 2017 Adrian Rossiter <adrian@antiprism.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
Construct a cyclic rhombohedron with three bands of congruent skew rhombi.
'''
import argparse
import sys
from math import cos, sin, acos, sqrt, pi
import anti_lib


def make_3_band_rhombohedron(pgon, horz_diags):
    """Make a cyclic rhombohedron with three bands of congruent skew rhombi"""
    N = pgon.N
    a = pgon.angle() / 2
    k = 1 - 2*cos(a)
    h = sqrt(1 + 2*k)/k
    l = (1 - 2*(h > 0))*sqrt(1 + h*h)/2
    A = anti_lib.Vec(0, 0, 1)
    P1 = anti_lib.Vec(h*cos(a), h*sin(a), l)
    P2 = anti_lib.Vec(P1[0], P1[1], -P1[2])
    Q = anti_lib.Vec(h, 0, 0)
    points = [anti_lib.Vec(0, 0, 0)] * (3 * N + 2)
    faces = []
    for i in range(N):
        ang = 2*i*a
        points[i] = P1.rot_z(ang)
        points[i+N] = Q.rot_z(ang)
        points[i+2*N] = P2.rot_z(ang)
        if horz_diags:
            faces.append([3*N, i, (i - 1 + N) % N])
            faces.append([i, i + N, (i - 1 + N) % N])
            faces.append([i, (i + 1 + N) % N + N, (i + N) % N + N])
            faces.append([(i + 1 + N) % N + N, i+2*N, (i + N) % N + N])
            faces.append([i+N, (i - 1 + N) % N + 2*N,  (i + N) % N + 2*N])
            faces.append([(i - 1 + N) % N + 2*N, 3*N+1, (i + N) % N + 2*N])
        else:
            faces.append([3*N, i, i + N])
            faces.append([i + N, (i - 1 + N) % N, 3*N])
            faces.append([i, (i + 1 + N) % N + N, i+2*N])
            faces.append([i+2*N, (i + N) % N + N, i])
            faces.append([i+N, (i - 1 + N) % N + 2*N, 3*N+1])
            faces.append([3*N+1, (i + N) % N + 2*N, i + N])

    points[3*N] = A
    points[3*N+1] = -A

    return points, faces


def main():
    """Entry point"""
    epilog = '''
notes:
  Depends on anti_lib.py.

examples:
  Cuboctahedron
  barrel.py 4 | antiview

  Pentagonal square barrel capped with pyramids ("trapezobarrel")
  barrel.py -t 5 | antiview

  Pentagonal square barrel with two bands of squares
  barrel.py -n 2 5 | antiview
'''

    parser = argparse.ArgumentParser(formatter_class=anti_lib.DefFormatter,
                                     description=__doc__, epilog=epilog)

    parser.add_argument(
        'polygon_fraction',
        help='number of sides of the base polygon (N), '
        'or a fraction for star polygons (N/D) (default: 6)',
        default='6',
        nargs='?',
        type=anti_lib.read_polygon)
    parser.add_argument(
        '-z', '--horizontal_diagonals',
        help='use horizontal diagonals',
        action='store_true')
    parser.add_argument(
        '-o', '--outfile',
        help='output file name (default: standard output)',
        type=argparse.FileType('w'),
        default=sys.stdout)

    args = parser.parse_args()

    pgon = args.polygon_fraction
    if acos(3/4) > pi * pgon.D/pgon.N:
        parser.error('polyhedron is not constructible, '
                     'fraction > 4.3468... [pi/acos(3/4)])')
    points, faces = make_3_band_rhombohedron(pgon, args.horizontal_diagonals)

    out = anti_lib.OffFile(args.outfile)
    out.print_all_pgon(points, faces, pgon)


if __name__ == "__main__":
    main()
