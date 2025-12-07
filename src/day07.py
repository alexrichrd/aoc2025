import sys
from pathlib import Path

import numpy as np

input_size = (0, 0)


########################### PART 1 ############################
def take_step(position, input):
    row = position[0]
    col = position[1]
    if row + 1 == input.shape[0]:
        return (), ()
    if input[row + 1][col] == 0:
        return (row + 1, col), ()
    return (row + 1, col - 1), (row + 1, col + 1)


with Path(sys.argv[1]).open() as file:
    row_count = 0
    col_count = 0
    for row in file:
        if row_count == 0:
            for _ in row:
                col_count += 1
        row_count += 1
    input_size = (row_count, col_count)

with Path(sys.argv[1]).open() as file:
    positions: list = []
    input_arr = np.zeros(input_size)
    for i, row in enumerate(file):
        for j, col in enumerate(row):
            if col == ".":
                input_arr[i][j] = 0
            elif col == "^":
                input_arr[i][j] = 1
            elif col == "S":
                positions.append((i, j))
    splits = 0
    level = 1
    while positions:
        temp_positions = []
        for position in positions:
            next_pos1, next_pos2 = take_step(position, input_arr)
            if next_pos1:
                # print(next_pos1)
                temp_positions.append(next_pos1)
            if next_pos2:
                # print(next_pos2)
                temp_positions.append(next_pos2)
        if not list(set(temp_positions)):
            # reached the end of the grid
            break
        splits += len(temp_positions) - len(positions)
        temp_positions = list(set(temp_positions))
        positions = temp_positions
        level += 1
    print("Part 1:", splits)


########################### PART 2 ############################
visited_positions = {}


def take_timeline(position, input):
    if position in visited_positions:
        return visited_positions[position]
    row = position[0]
    col = position[1]
    if row + 1 == input.shape[0]:
        return 1
    if input[row + 1][col] == 0:
        visited_positions[position] = take_timeline((row + 1, col), input)
    else:
        visited_positions[position] = take_timeline(
            (row + 1, col - 1),
            input,
        ) + take_timeline(
            (row + 1, col + 1),
            input,
        )
    return visited_positions[position]


with Path(sys.argv[1]).open() as file:
    start_pos = (0, 0)
    input_arr = np.zeros(input_size)
    for i, row in enumerate(file):
        for j, col in enumerate(row):
            if col == ".":
                input_arr[i][j] = 0
            elif col == "^":
                input_arr[i][j] = 1
            elif col == "S":
                start_pos = (i, j)
    num_timelines = take_timeline(start_pos, input_arr)
    print("Part 2:", num_timelines)
