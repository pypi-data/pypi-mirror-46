# OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
tools: Useful tools
"""

import numpy as np

from octadist.src import linear, projection


def find_bonds(fal, fcl):
    """Find all bond distance and filter the possible bonds

    - Compute distance of all bonds
    - Screen bonds out based on global cutoff distance
    - Screen H bonds out based on local cutoff distance

    :param fal: list of atomic labels of full complex
    :param fcl: list of atomic coordinates of full complex
    :type fal: list
    :type fcl: list
    :return check_2_bond_list: selected bonds
    :rtype check_2_bond_list: list
    """
    global_distance_cutoff = 2.0
    hydrogen_distance_cutoff = 1.2

    pair_list = []
    bond_list = []
    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            if i == 0:
                distance = linear.distance_bwn_points(fcl[i], fcl[j])
            else:
                distance = linear.distance_bwn_points(fcl[i], fcl[j])

            pair_list.append([fal[i], fal[j]])
            bond_list.append([fcl[i], fcl[j], distance])

    check_1_bond_list = []
    screen_1_pair_list = []
    for i in range(len(bond_list)):
        if bond_list[i][2] <= global_distance_cutoff:
            check_1_bond_list.append([bond_list[i][0], bond_list[i][1], bond_list[i][2]])
            screen_1_pair_list.append([pair_list[i][0], pair_list[i][1]])

    check_2_bond_list = []
    for i in range(len(check_1_bond_list)):
        if screen_1_pair_list[i][0] == "H" or screen_1_pair_list[i][1] == "H":
            if check_1_bond_list[i][2] <= hydrogen_distance_cutoff:
                check_2_bond_list.append([check_1_bond_list[i][0], check_1_bond_list[i][1]])
        else:
            check_2_bond_list.append([check_1_bond_list[i][0], check_1_bond_list[i][1]])

    return check_2_bond_list


def find_faces_octa(c_octa):
    """Find the eight faces of octahedral structure

    1) Choose 3 atoms out of 6 ligand atoms. The total number of combination is 20
    2) Orthogonally project metal center atom onto the face: m ----> m'
    3) Calculate the shortest distance between original metal center to its projected point
    4) Sort the 20 faces in ascending order of the shortest distance
    5) Delete 12 faces that closest to metal center atom (first 12 faces)
    6) The remaining 8 faces are the (reference) face of octahedral structure
    7) Find 8 opposite faces

    For example,
         Reference plane            Opposite plane
            [[1 2 3]                   [[4 5 6]
             [1 2 4]        --->        [3 5 6]
               ...                        ...
             [2 3 5]]                   [1 4 6]]

    :param c_octa: atomic coordinates of octahedral structure
    :type c_octa: list, array, tuple    :return a_ref_f: list - atomic labels of reference face
    :return a_ref_f: atomic labels of reference face
    :return c_ref_f: atomic coordinates of reference face
    :return a_oppo_f: atomic labels of opposite face
    :return c_oppo_f: atomic coordinates of opposite face
    :rtype a_ref_f: list
    :rtype c_ref_f: array
    :rtype a_oppo_f: list
    :rtype c_oppo_f: array
    """
    ########################
    # Find reference faces #
    ########################

    # Find the shortest distance from metal center to each triangle
    distance = []
    a_ref_f = []
    c_ref_f = []
    for i in range(1, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                a, b, c, d = linear.find_eq_of_plane(c_octa[i], c_octa[j], c_octa[k])
                m = projection.project_atom_onto_plane(c_octa[0], a, b, c, d)
                d_btw = linear.distance_bwn_points(m, c_octa[0])
                distance.append(d_btw)
                a_ref_f.append([i, j, k])
                c_ref_f.append([c_octa[i], c_octa[j], c_octa[k]])

    # Sort faces by distance in ascending order
    dist_a_c = list(zip(distance, a_ref_f, c_ref_f))
    dist_a_c.sort()
    distance, a_ref_f, c_ref_f = list(zip(*dist_a_c))
    c_ref_f = np.asarray(c_ref_f)

    # Remove first 12 triangles, the rest of triangles is 8 faces of octahedron
    a_ref_f = a_ref_f[12:]
    c_ref_f = c_ref_f[12:]

    #######################
    # Find opposite faces #
    #######################

    all_atom = [1, 2, 3, 4, 5, 6]
    a_oppo_f = []
    # loop over 4 reference planes
    for i in range(len(a_ref_f)):
        # Find atoms of opposite plane
        new_a_ref_f = []
        for j in all_atom:
            if j not in (a_ref_f[i][0], a_ref_f[i][1], a_ref_f[i][2]):
                new_a_ref_f.append(j)
        a_oppo_f.append(new_a_ref_f)

    v = np.array(c_octa)
    c_oppo_f = []
    for i in range(len(a_oppo_f)):
        coord_oppo = []
        for j in range(3):
            coord_oppo.append([v[int(a_oppo_f[i][j])][0], v[int(a_oppo_f[i][j])][1], v[int(a_oppo_f[i][j])]][2])
        c_oppo_f.append(coord_oppo)

    return a_ref_f, c_ref_f, a_oppo_f, c_oppo_f
