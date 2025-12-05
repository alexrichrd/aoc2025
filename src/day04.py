import sys
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

NEIGHBOR_LIMIT = 3
padded_input_shape = (0, 0)


# determine the file size
with Path(sys.argv[1]).open() as file:
    line_count = 0
    column_count = 0
    for line in file:
        if line_count == 0:
            column_count = len(line.strip())
        line_count += 1
    padded_input_shape = (line_count + 2, column_count + 2)


########################### PART 1 ############################
def stencil(row: int, col: int, padded_input_diagram: NDArray[np.bool_]) -> bool:
    submask = padded_input_diagram[row - 1 : row + 2, col - 1 : col + 2]
    return (
        np.sum(
            np.logical_and(
                submask, [[True, True, True], [True, False, True], [True, True, True]],
            ),
        )
        <= NEIGHBOR_LIMIT
    )


def diagram_to_string(diagram: NDArray[np.bool_]) -> None:
    for row in diagram[1 : diagram.shape[0] - 1, 1 : diagram.shape[1] - 1]:
        for elem in row:
            if elem:
                print("@", end="")
            else:
                print(".", end="")
        print("\n")


with Path(sys.argv[1]).open() as file:
    padded_input_diagram = np.zeros(padded_input_shape, dtype=np.bool_)
    for row_index, row in enumerate(file):
        for col_index, col in enumerate(row.strip()):
            padded_input_diagram[row_index + 1][col_index + 1] = bool(col == "@")
    # store which rolls are accessible in a second array
    accessibility_diagram = np.zeros(padded_input_shape, dtype=np.bool_)
    for row_index in range(1, padded_input_diagram.shape[0] - 1):
        for col_index in range(1, padded_input_diagram.shape[1] - 1):
            if padded_input_diagram[row_index][col_index]:
                accessibility_diagram[row_index][col_index] = stencil(
                    row_index,
                    col_index,
                    padded_input_diagram,
                )

    print("Part 1:", np.sum(accessibility_diagram))


########################### PART 2 ############################
def rolls_removable(padded_input_diagram: NDArray[np.bool_]) -> bool:
    for row_index in range(1, padded_input_diagram.shape[0] - 1):
        for col_index in range(1, padded_input_diagram.shape[1] - 1):
            if padded_input_diagram[row_index][col_index] and stencil(
                row_index,
                col_index,
                padded_input_diagram,
            ):
                return True
    return False


def remove_rolls(
    padded_input_diagram: NDArray[np.bool_],
) -> tuple[int, NDArray[np.bool_]]:
    current_input_diagram = padded_input_diagram
    removed_rolls = 0
    for row_index in range(1, padded_input_diagram.shape[0] - 1):
        for col_index in range(1, padded_input_diagram.shape[1] - 1):
            if padded_input_diagram[row_index][col_index] and stencil(
                row_index,
                col_index,
                padded_input_diagram,
            ):
                current_input_diagram[row_index][col_index] = 0
                removed_rolls += 1
    return removed_rolls, current_input_diagram


with Path(sys.argv[1]).open() as file:
    padded_input_diagram = np.zeros(padded_input_shape, dtype=np.bool_)
    for row_index, row in enumerate(file):
        for col_index, col in enumerate(row.strip()):
            padded_input_diagram[row_index + 1][col_index + 1] = bool(col == "@")
    # store which rolls are accessible in a second array
    accessibility_diagram = np.zeros(padded_input_shape, dtype=np.bool_)
    total_removed_rolls = 0
    while rolls_removable(padded_input_diagram):
        removed_rolls, padded_input_diagram = remove_rolls(padded_input_diagram)
        total_removed_rolls += removed_rolls

    print("Part 2:", np.sum(total_removed_rolls))
