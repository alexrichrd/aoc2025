import sys
from pathlib import Path

########################### PART 1 ############################
MAX_JOLTAGE_PER_BANK_PART1 = 99
MIN_BANK_LENGTH_PART1 = 2
total_joltage_part1 = 0


def find_largest_joltage(bank: str) -> str:
    current_highest = bank[0]
    if len(bank) == 1:
        return current_highest
    return str(max(int(current_highest), int(find_largest_joltage(bank[1:]))))


def compute_joltage(bank: str) -> str:
    if len(bank) == MIN_BANK_LENGTH_PART1:
        return bank[0] + bank[1]
    current_joltage_candidate = int(bank[0] + find_largest_joltage(bank[1:]))
    if current_joltage_candidate == MAX_JOLTAGE_PER_BANK_PART1:
        return str(current_joltage_candidate)
    return str(max(current_joltage_candidate, int(compute_joltage(bank[1:]))))


with Path(sys.argv[1]).open() as file:
    for bank in file:
        total_joltage_part1 += int(compute_joltage(bank.strip()))

    print("Part 1:", total_joltage_part1)


########################### PART 2 ############################
total_joltage_part2 = 0


def find_largest_joltage_part2(bank: str, num_batteries: int) -> tuple[str, str]:
    places_to_check = len(bank) - num_batteries + 1
    largest_joltage = bank[0]
    place_of_largest_joltage = 0
    for i in range(places_to_check):
        if bank[i] > largest_joltage:
            largest_joltage = bank[i]
            place_of_largest_joltage = i
    return largest_joltage, bank[place_of_largest_joltage + 1 :]


def compute_joltage_part2(
    bank: str,
    num_batteries: int,
) -> str:
    if len(bank) < num_batteries:
        return "Error: Not enough batteries left to switch on 12"
    if len(bank) == num_batteries:
        return bank
    if num_batteries == 0:
        return ""
    largest_joltage, remaining_bank = find_largest_joltage_part2(bank, num_batteries)
    return largest_joltage + compute_joltage_part2(remaining_bank, num_batteries - 1)


with Path(sys.argv[1]).open() as file:
    for bank in file:
        total_joltage_part2 += int(
            compute_joltage_part2(bank.strip(), 12),
        )

    print("Part 2:", total_joltage_part2)
