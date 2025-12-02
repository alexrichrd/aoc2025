import fileinput

DIAL_UPPER_BOUND = 99


############################ PART 1 ############################
def perform_rotation_part1(
    current_pos: int,
    rot_str: str,
    zero_counter: int,
) -> tuple[int, int]:
    direction = rot_str[0]
    steps = int(rot_str[1:])
    # going left by n % 100 is going right by (100 - n) % 100
    if steps != 0:
        if direction == "R":
            current_pos = (current_pos + steps) % 100
            zero_counter = zero_counter if current_pos != 0 else zero_counter + 1
        else:
            current_pos = (current_pos + 100 - steps) % 100
            zero_counter = zero_counter if current_pos != 0 else zero_counter + 1
    return current_pos, zero_counter


with fileinput.input(encoding="utf-8") as file:
    # part 1
    zero_counter = 0
    current_pos = 50
    for line in file:
        current_pos, zero_counter = perform_rotation_part1(
            current_pos,
            line,
            zero_counter,
        )

    print("Part 1:", zero_counter)


############################ PART 2 ############################
def perform_rotation_part2(
    current_pos: int,
    rot_str: str,
    zero_counter: int,
) -> tuple[int, int]:
    direction = rot_str[0]
    steps = int(rot_str[1:])
    clicks_to_add = 0
    if steps > 0:
        if direction == "R":
            clicks_to_add = steps // 100  # number of full rotations
            condition = current_pos + (steps - clicks_to_add * 100) > DIAL_UPPER_BOUND
            clicks_to_add += 1 if condition else 0
            current_pos = (current_pos + steps) % 100
        else:
            clicks_to_add = steps // 100  # number of full rotations
            condition = (
                current_pos - (steps - clicks_to_add * 100) <= 0 and current_pos != 0
            )
            clicks_to_add += 1 if condition else 0
            current_pos = (current_pos + 100 - steps) % 100
    else:
        print("Invalid rotation!")
    return current_pos, zero_counter + clicks_to_add


with fileinput.input(encoding="utf-8") as file:
    # part 2
    zero_counter = 0
    current_pos = 50
    for line in file:
        current_pos, zero_counter = perform_rotation_part2(
            current_pos,
            line,
            zero_counter,
        )

    print("Part 2:", zero_counter)
