import sys
from pathlib import Path

import numpy as np


########################### PART 1 ############################
def compute_rectangle_size(i: int, locations) -> int:
    temp_size = 0
    for corner in locations[i + 1 :,]:
        x_length = abs(locations[i][0] - corner[0]) + 1
        y_length = abs(locations[i][1] - corner[1]) + 1
        temp_size = max(temp_size, x_length * y_length)
    return temp_size


locations = np.loadtxt(sys.argv[1], delimiter=",", dtype=int)

max_size = 0
for i in range(locations.shape[0] - 1):
    temp_size = compute_rectangle_size(i, locations)
    max_size = max(max_size, temp_size)
print("Part 1:", max_size)


########################### PART 2 ############################
def compute_valid_range(locations):
    # idea: create a boolean array LOC indicating the valid region
    # for each rectangle: compute a boolean array REC indicating the rectangle
    # compute RES = LOC `AND` REC
    # if RES == REC: rectangle is in valid region
    left_bound = np.min(locations[:, 0])
    upper_bound = np.min(locations[0, :])
    right_bound = np.max(locations[:, 0])
    lower_bound = np.max(locations[-1, :])
    # print(left_bound)
    # print(upper_bound)
    # print(right_bound)
    # print(lower_bound)


compute_valid_range(locations)
