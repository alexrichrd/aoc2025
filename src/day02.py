import sys
from pathlib import Path

########################### PART 1 ############################
invalid_ids_part1: list = []


def get_invalid_product_ids_part1(first_id: str, last_id: str) -> None:
    for prod_id in range(int(first_id), int(last_id) + 1):
        id_length = len(str(prod_id))
        if id_length % 2 == 0:
            first_half = str(prod_id)[: id_length // 2]
            second_half = str(prod_id)[id_length // 2 :]
            if first_half == second_half:
                invalid_ids_part1.append(prod_id)


with Path(sys.argv[1]).open() as file:
    product_id_ranges = file.read().strip().split(",")
    for prod_id_range in product_id_ranges:
        first_id = prod_id_range.split("-")[0]
        last_id = prod_id_range.split("-")[1]

        get_invalid_product_ids_part1(first_id, last_id)

    print("Part 1:", sum(invalid_ids_part1))


# ############################ PART 2 ############################
invalid_ids_part2: list = []
pattern_dicts: dict = {}


def compute_patterns_to_check(id_length: int) -> dict:
    pattern_dict: dict = {}
    divisors = []
    # compute all divisors for a given length
    for i in range(2, id_length + 1):
        if id_length % i == 0:
            divisors.append(i)
    # compute all pattern combinations we need to check
    for divisor1 in divisors:
        for divisor2 in divisors:
            if divisor1 * divisor2 == id_length:
                pattern_dict[divisor1] = divisor2
    pattern_dict[id_length] = 1
    return pattern_dict


def get_invalid_product_ids_part2(first_id: str, last_id: str) -> None:
    for prod_id in range(int(first_id), int(last_id) + 1):
        id_length = len(str(prod_id))
        if id_length == 1:
            continue
        for pattern_occurence in pattern_dicts[id_length].values():
            substrings = [
                str(prod_id)[i : i + pattern_occurence]
                for i in range(0, id_length, pattern_occurence)
            ]
            substrings_are_equal = True
            for substring in substrings:
                if substring != substrings[0]:
                    substrings_are_equal = False
                    break
            if substrings_are_equal:
                invalid_ids_part2.append(prod_id)
                break


with Path(sys.argv[1]).open() as file:
    product_id_ranges = file.read().strip().split(",")
    for prod_id_range in product_id_ranges:
        first_id = prod_id_range.split("-")[0]
        last_id = prod_id_range.split("-")[1]
        first_id_length = len(first_id)
        last_id_length = len(last_id)
        for id_length in range(first_id_length, last_id_length + 1):
            # check if patterns for the string lengths already exist
            if id_length not in pattern_dicts and id_length > 1:
                pattern_dicts[id_length] = compute_patterns_to_check(id_length)

        get_invalid_product_ids_part2(first_id, last_id)

    print("Part 2:", sum(invalid_ids_part2))
