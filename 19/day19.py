"""Solves day 19, Advent of Code 2021."""

from aocd.models import Puzzle
import numpy as np
import re
from io import StringIO
from collections import namedtuple

Fingerprint = namedtuple("Fingerprint", "all_dists each_dist")

def parse_data(input_data: str) -> list:
    """Return a list of each scanners' beacon data."""

    # split input data into a list of csv-formatted beacon data
    scanners = re.split("--- scanner .* ---", input_data)[1:]
    
    # convert the csv data into numpy.arrays
    return [np.loadtxt(StringIO(scanner),delimiter=',',dtype=int)
            for scanner in scanners]


def fingerprint(s: np.array) -> Fingerprint:
    """Provide a fingerprint for a collection of beacon data.

    The fingerprint collects the manhattan distances between beacons."""
    n = s.shape[0]
    a = s[:,0:1]
    b = s[:,1:2]
    c = s[:,2:3]
    x = abs(a-a.T) + abs(b-b.T) + abs(c-c.T)

    # for each beacon, a set of dists to other beacons
    each_dist = [set(dists) for dists in x.tolist()]

    # a set of dists from any beacon to any beacon
    all_dists = set.union(*each_dist)

    return Fingerprint(all_dists=all_dists, each_dist=each_dist)


def overlaps(a: Fingerprint, b: Fingerprint) -> bool:
    """Return True if fingerprints indicate an overlap in beacon data."""

    return len(a.all_dists & b.all_dists) > 60


def shared_beacon_idxs(a: Fingerprint, b: Fingerprint) -> list:
    """Return a list of (i,j) mapping common indices between some shared beacons."""

    # We might not find all 12 shared beacons, because we use a set rather than a
    # multiset to record distances, and so any identical distance values will cause
    # a lower overlap between the sets.  But we only need to find 3-4 shared
    # beacons anyway, at least for non-pathological cases.
    
    na = len(a.each_dist)
    nb = len(b.each_dist)
    return [(i,j)
            for i in range(na) for j in range(nb)
            if len(a.each_dist[i] & b.each_dist[j]) > 10]


ROTATIONS = [
    np.array([[1,0,0],[0,1,0],[0,0,1]]),
    np.array([[1,0,0],[0,0,1],[0,1,0]]),
    np.array([[0,1,0],[1,0,0],[0,0,1]]),
    np.array([[0,1,0],[0,0,1],[1,0,0]]),
    np.array([[0,0,1],[1,0,0],[0,1,0]]),
    np.array([[0,0,1],[0,1,0],[1,0,0]])
    ]
    

def find_transformation(a: np.array, b: np.array):
    """Returns a vector and matrix to convert b coordinates to a.

    Example:
    tr = find_tranformation(a, b)
    b_to_a = tr(b)
    Assumes a and b contain the same points, but rotated, translated, reflected."""

    # common beacons in cm coords
    a_offset = a.sum(axis=0)/len(a)
    b_offset = b.sum(axis=0)/len(b)
    a_cm = a - a_offset
    b_cm = b - b_offset

    # tolerance must be fairly large due to integer rounding
    TOLERANCE = 100
    
    for rot in ROTATIONS:
        deviation = np.sum(abs(abs(a_cm) - abs(b_cm @ rot)))

        if deviation < TOLERANCE:
            break
    else:
        raise ValueError("find_transformation: failed to find rotation.")

    reflection = [1,1,1]
    b_r = b_cm @ rot
    baseline = np.sum(abs(a_cm - b_r))
    for axis in range(3):
        reflection[axis] = -1
        deviation = np.sum(abs(a_cm - b_r * reflection))
        if deviation < baseline:
            baseline = deviation
        else:
            reflection[axis] = +1
    
    if baseline > TOLERANCE:
        raise ValueError("find_transformation: failed to find reflection.")

    rot = rot * reflection
    
    def transform(x: np.array) -> np.array:
        """Transformation constructed by find_transformation."""
        return np.array(((x - b_offset) @ rot + a_offset).round(), dtype=int)

    return transform
    
            
def reconcile_beacon_data(beacon_data: list) -> list:
    """Transforms the beacon coordinate data and returns a list of scanner coordinates.

    For each scanner, the beacon_data list itself is modified in-place so that
    the beacons are put into the coordinate system of scanner 0.

    The list of scanner coordinates is also in scanner 0's coordinate system."""
    
    f = [fingerprint(scanner) for scanner in beacon_data]
    transformed_scanners = {0}
    scanners_to_visit = [0]
    scanner_coords = [None] * len(beacon_data)
    origin = np.array([0,0,0], dtype=int)
    scanner_coords[0] = origin

    while scanners_to_visit:
        i = scanners_to_visit.pop()
        for j in range(len(beacon_data)):
            if j in transformed_scanners:
                continue
            if not overlaps(f[i], f[j]):
                continue
            sbi = shared_beacon_idxs(f[i], f[j])
            i_beacon_idxs, j_beacon_idxs = zip(*sbi)
            coords_i = beacon_data[i][i_beacon_idxs,:]
            coords_j = beacon_data[j][j_beacon_idxs,:]
            j_to_i = find_transformation(coords_i, coords_j)
            scanner_coords[j] = j_to_i(origin)
            beacon_data[j] = j_to_i(beacon_data[j])
            transformed_scanners |= {j}
            scanners_to_visit.append(j)
                 
    if len(transformed_scanners) != len(beacon_data):
        raise ValueError("Could not link all scanner data.")
    return scanner_coords


    

def part_ab(input_data: str) -> int:
    """Given the puzzle input data, return the solution for part A."""
    beacon_data = parse_data(input_data)
    scanners_list = reconcile_beacon_data(beacon_data)

    all_beacons = np.vstack(beacon_data)
    beacon_set = {tuple(coord) for coord in all_beacons}
    number_beacons = len(beacon_set)

    scanners_array = np.array(scanners_list)
    fp_scanners = fingerprint(scanners_array)
    max_scanner_dist = max(fp_scanners.all_dists)

    return number_beacons, max_scanner_dist



if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=19)

    print(f"Puzzle {puzzle.year}-12-{puzzle.day:02d}: {puzzle.title}")
    a, b = part_ab(puzzle.input_data)
    print(f"  Part A: {a}")
    print(f"  Part B: {b}")
