import sys
from pathlib import Path

import numpy as np

input_size: tuple[int, int] = (0, 0)

########################### PART 1 ############################
with Path(sys.argv[1]).open() as file:
    row_count: int = 0
    col_count: int = 0
    for _, row in enumerate(file):
        if row_count == 0:
            col_count = len(row.split())
        row_count += 1
    input_size = (row_count, col_count)

with Path(sys.argv[1]).open() as file:
    input_arr = np.zeros(shape=[input_size[0] - 1, input_size[1]], dtype=np.uint32)
    operators = np.zeros((1, input_size[1]), dtype=np.uint32)
    for i, row in enumerate(file):
        if i < input_arr.shape[0]:
            input_arr[i] = [int(j.strip()) for j in row.split()]
        else:
            operators = np.array([0 if x == "+" else 1 for x in row.split()])
    results = np.zeros((1, input_arr.shape[1]), dtype=int)
    indices_to_sum = np.where(operators == 0)[0]
    indices_to_multiply = np.where(operators == 1)[0]
    results[:, indices_to_sum] = input_arr[:, indices_to_sum].sum(
        axis=0,
    )
    results[:, indices_to_multiply] = input_arr[:, indices_to_multiply].prod(
        axis=0,
    )
    print("Part 1:", np.sum(results))


########################### PART 2 ############################
block_indices = []  # indices where new blocks begin
num_operands = 0
operator_types = []  # 0: add, 1: mul

with Path(sys.argv[1]).open() as file:
    for line in file:
        if line.lstrip()[0] in ["+", "*"]:
            for i, operator in enumerate(line):
                if operator == "+":
                    operator_types.append(0)
                    block_indices.append(i)
                elif operator == "*":
                    operator_types.append(1)
                    block_indices.append(i)
        else:
            num_operands += 1


def compute_block(inputs, block_index, operator):
    col = inputs[:, block_index]
    max_arity = len(str(max(col)))  # number of digits in the largest entry

    # right align digits with zero padding
    digits = np.zeros((num_operands, max_arity), dtype=int)
    for i, v in enumerate(col):
        s = str(v).rjust(max_arity, "0")
        digits[i] = np.array(list(map(int, s)))

    new_values = []

    # Walk digit positions from units to most-significant
    for j in range(max_arity):
        idx = max_arity - 1 - j
        col_digits = list(digits[:, idx])  # top to bottom

        while col_digits and col_digits[-1] == 0:
            col_digits.pop()

        number = 0 if not col_digits else int("".join(map(str, col_digits)))
        new_values.append(number)

    new_values = np.array(new_values)

    if operator == 0:  # add
        return int(new_values.sum())
    return int(np.prod(new_values))


with Path(sys.argv[1]).open() as file:
    num_blocks = len(block_indices)
    inputs = np.zeros((num_operands, num_blocks), dtype=int)
    for i, line in enumerate(file):
        if line.lstrip()[0] not in ["+", "*"]:
            for j, block_index in enumerate(block_indices):
                current_input = ""
                if j + 1 == num_blocks:
                    # last block before end of line
                    for s in line[block_index:]:
                        if s != " ":
                            current_input += s
                        else:
                            current_input += "0"
                else:
                    # read until one character before new block begins
                    for s in line[block_index : block_indices[j + 1] - 1]:
                        if s != " ":
                            current_input += s
                        else:
                            current_input += "0"
                inputs[i][j] = int(current_input)
    result = 0
    for i, operator in enumerate(operator_types):
        res = compute_block(inputs, i, operator)
        result += res

    print("Part 2:", result)
