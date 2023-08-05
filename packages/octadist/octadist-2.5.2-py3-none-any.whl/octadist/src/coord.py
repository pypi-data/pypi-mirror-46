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
coord: Manipulating atomic labels and atomic coordinates
"""

from operator import itemgetter

import numpy as np

from octadist.src import elements, linear


def count_line(file):
    """Count line in input file

    :param file: absolute path of input file
    :type file: str
    :return: number of line in file
    :rtype: int
    """
    with open(file) as f:
        for i, l in enumerate(f):
            pass

    return i + 1


def find_metal(a_full, c_full):
    """Find and count the metal center atom in complex

    :param a_full: full atomic labels of complex
    :param c_full: full atomic coordinates of complex
    :type a_full: list
    :type c_full: array
    :return count: the total number of metal center atom
    :return a_metal: atomic labels of metal center atom
    :return c_metal: atomic coordinates of metal center atom
    :rtype count: int
    :rtype a_metal: list
    :rtype c_metal: array
    """
    count = 0
    c_metal = []

    for i in range(len(a_full)):
        number = elements.check_atom(a_full[i])
        if 21 <= number <= 30 or 39 <= number <= 48 or 57 <= number <= 80 or 89 <= number <= 109:
            count += 1
            c_metal.append(c_full[i])

    return count, c_metal


def extract_file(f):
    """Extract full atomic symbols and coordinates from input file

    **Support file type**::
        - XYZ
        - Gaussian
        - NWChem
        - ORCA
        - Q-Chem

    :param f: user input filename
    :type f: str
    :return a_full: full atomic labels of complex
    :return c_full: full atomic coordinates of complex
    :rtype a_full: list
    :rtype c_full: array
    """
    a_full = []
    c_full = []

    # Check file extension
    if f.endswith(".xyz"):
        if check_xyz_file(f):
            a_full, c_full = get_coord_xyz(f)

    elif f.endswith(".out") or f.endswith(".log"):
        if check_gaussian_file(f):
            a_full, c_full = get_coord_gaussian(f)
        elif check_nwchem_file(f):
            a_full, c_full = get_coord_nwchem(f)
        elif check_orca_file(f):
            a_full, c_full = get_coord_orca(f)
        elif check_qchem_file(f):
            a_full, c_full = get_coord_qchem(f)

    # Remove empty string in list
    a_full = list(filter(None, a_full))

    return a_full, c_full


def extract_octa(a_full, c_full, m_index=1):
    """Extract atomic symbols and coordinates of octahedral structure from full atomic coordinates list

    :param a_full: full atomic labels of complex
    :param c_full: full atomic coordinates of complex
    :param m_index: the number of metal center atom - default is 1
    :type a_full: list
    :type c_full: list, array, tuple
    :type m_index: int
    :return a_octa: atomic labels of octahedral structure
    :return c_octa: atomic coordinates of octahedral structure
    :rtype a_octa: list
    :rtype c_octa: array
    """
    # make sure that c_full is array, not list
    c_full = np.asarray(c_full)

    # Count the number of metal center atom
    count, c_metal = find_metal(a_full, c_full)

    if m_index > count:
        print("Error: the index of metal you defined is greater than the total number of metal in complex.")
        return 1

    metal_index = m_index - 1
    dist_list = []

    for i in range(len(a_full)):
        dist = linear.distance_bwn_points(c_metal[metal_index], c_full[i])
        dist_list.append([a_full[i], c_full[i], dist])

    dist_list.sort(key=itemgetter(2))  # sort list of tuples by distance in ascending order
    dist_list = dist_list[:7]  # Get only first 7 atoms
    a_octa, c_octa, distance = zip(*dist_list)  # Collect atom and coordinates

    a_octa = list(a_octa)  # Convert a_octa to list
    c_octa = np.asarray(c_octa)  # Convert c_octa to np.array

    return a_octa, c_octa


def check_xyz_file(f):
    """Check if the input file is .xyz file format

    xyz file format
    ---------------

    <number of atom>
    comment
    <index 0> <X> <Y> <Z>
    <index 1> <X> <Y> <Z>
    ...
    <index 6> <X> <Y> <Z>

    :param f: user input filename
    :type f: str
    :return: if the file is .xyz format, return True
    :rtype: bool

    **Example**
        7
        Comment: From Excel file
        Fe  6.251705    9.063211    5.914842
        N   8.15961     9.066456    5.463087
        N   6.749414    10.457551   7.179682
        N   5.709997    10.492955   4.658257
        N   4.350474    9.106286    6.356091
        O   5.789096    7.796326    4.611355
        O   6.686381    7.763872    7.209699

    """
    # import extract module here to avoid circular dependencies

    file = open(f, "r")

    first_line = file.readline()

    # Check if the first line is integer
    try:
        int(first_line)
    except ValueError:
        return False

    if count_line(f) < 9:
        return False
    else:
        return True


def get_coord_xyz(f):
    """Get coordinate from .xyz file

    :param f: user input filename
    :type f: str
    :return a_full: full atomic labels of complex
    :return c_full: full atomic coordinates of complex
    :rtype a_full: list
    :rtype c_full: array
    """
    file = open(f, "r")
    # read file from 3rd line
    line = file.readlines()[2:]
    file.close()

    a_full = []
    for l in line:
        # read atom on 1st column and insert to list
        l_strip = l.strip()
        lst = l_strip.split(' ')[0]
        a_full.append(lst)

    file = open(f, "r")
    c_full = np.loadtxt(file, skiprows=2, usecols=[1, 2, 3])
    file.close()

    return a_full, c_full


def check_gaussian_file(f):
    """Check if the input file is Gaussian file format

    :param f: user input filename
    :type f: str
    :return: if file is Gaussian output file, return True
    :rtype: bool
    """
    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()
    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            return True

    return False


def get_coord_gaussian(f):
    """Extract XYZ coordinate from Gaussian output file

    :param f: user input filename
    :type f: str
    :return a_full: full atomic labels of complex
    :return c_full: full atomic coordinates of complex
    :rtype a_full: list
    :rtype c_full: array
    """
    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    start = 0
    end = 0
    a_full, c_full = [], []
    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            start = i

    for i in range(start + 5, len(nline)):
        if "---" in nline[i]:
            end = i
            break

    for line in nline[start + 5: end]:
        data = line.split()
        data1 = int(data[1])
        coord_x = float(data[3])
        coord_y = float(data[4])
        coord_z = float(data[5])
        data1 = elements.check_atom(data1)
        a_full.append(data1)
        c_full.append([coord_x, coord_y, coord_z])

    gaussian_file.close()

    return a_full, c_full


def check_nwchem_file(f):
    """Check if the input file is NWChem file format

    :param f: user input filename
    :type f: str
    :return: if file is NWChem output file, return True
    :rtype: bool
    """
    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()
    for i in range(len(nline)):
        if "No. of atoms" in nline[i]:
            if not int(nline[i].split()[4]):
                return False

    for j in range(len(nline)):
        if "Optimization converged" in nline[j]:
            return True

    return False


def get_coord_nwchem(f):
    """Extract XYZ coordinate from NWChem output file

    :param f: user input filename
    :type f: str
    :return a_full: full atomic labels of complex
    :return c_full: full atomic coordinates of complex
    :rtype a_full: list
    :rtype c_full: array
    """
    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()

    start = 0
    end = 0
    a_full, c_full = [], []
    for i in range(len(nline)):
        if "Optimization converged" in nline[i]:
            start = i

    for i in range(len(nline)):
        if "No. of atoms" in nline[i]:
            end = int(nline[i].split()[4])

    start = start + 18
    end = start + end
    # The 1st line of coordinate is at 18 lines next to 'Optimization converged'
    for line in nline[start:end]:
        dat = line.split()
        dat1 = int(float(dat[2]))
        coord_x = float(dat[3])
        coord_y = float(dat[4])
        coord_z = float(dat[5])
        dat1 = elements.check_atom(dat1)
        a_full.append(dat1)
        c_full.append([coord_x, coord_y, coord_z])

    nwchem_file.close()

    return a_full, c_full


def check_orca_file(f):
    """Check if the input file is ORCA file format

    :param f: user input filename
    :type f: str
    :return: if file is ORCA output file, return True
    :rtype: bool
    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()
    for i in range(len(nline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in nline[i]:
            return True

    return False


def get_coord_orca(f):
    """Extract XYZ coordinate from ORCA output file

    :param f: user input filename
    :type f: str
    :return a_full: full atomic labels of complex
    :return c_full: full atomic coordinates of complex
    :rtype a_full: list
    :rtype c_full: array
    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0
    a_full, c_full = [], []
    for i in range(len(nline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in nline[i]:
            start = i

    for i in range(start + 2, len(nline)):
        if "---" in nline[i]:
            end = i - 1
            break

    for line in nline[start + 2:end]:
        dat = line.split()
        dat1 = dat[0]
        coord_x = float(dat[1])
        coord_y = float(dat[2])
        coord_z = float(dat[3])
        a_full.append(dat1)
        c_full.append([coord_x, coord_y, coord_z])

    orca_file.close()

    return a_full, c_full


def check_qchem_file(f):
    """Check if the input file is Q-Chem file format

    :param f: user input filename
    :type f: str
    :return: if file is Q-Chem output file, return True
    :rtype: bool
    """

    qchem_file = open(f, "r")
    nline = qchem_file.readlines()
    for i in range(len(nline)):
        if "OPTIMIZATION CONVERGED" in nline[i]:
            return True

    return False


def get_coord_qchem(f):
    """Extract XYZ coordinate from Q-Chem output file

    :param f: user input filename
    :type f: str
    :return a_full: full atomic labels of complex
    :return c_full: full atomic coordinates of complex
    :rtype a_full: list
    :rtype c_full: array
    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0
    a_full, c_full = [], []
    for i in range(len(nline)):
        if "OPTIMIZATION CONVERGED" in nline[i]:
            start = i

    for i in range(start + 5, len(nline)):
        if "Z-matrix Print:" in nline[i]:
            end = i - 1
            break

    for line in nline[start + 5:end]:
        dat = line.split()
        dat1 = dat[1]
        coord_x = float(dat[2])
        coord_y = float(dat[3])
        coord_z = float(dat[4])
        a_full.append(dat1)
        c_full.append([coord_x, coord_y, coord_z])

    orca_file.close()

    return a_full, c_full
