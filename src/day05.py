import sys
from pathlib import Path
from typing import Literal


########################### PART 1 ############################
# use an interval tree for this
class Interval:
    def __init__(self, lower: int, upper: int) -> None:
        self.lower: int = lower
        self.upper: int = upper


class Node:
    def __init__(self, interval: Interval, max_value: int) -> None:
        self.interval: Interval = interval
        self.max_value: int = max_value
        self.left_child: Node | None = None
        self.right_child: Node | None = None


def create_node(interval: Interval) -> Node:
    node: Node = Node(interval, interval.upper)
    return node


def insert_node(root_node: Node | None, interval: Interval) -> Node:
    # tree is empty
    if root_node is None:
        return create_node(interval)
    # get lower bound of root interval
    root_lower = root_node.interval.lower
    # insert at the right place
    if interval.lower < root_lower:
        root_node.left_child = insert_node(root_node.left_child, interval)
    else:
        root_node.right_child = insert_node(root_node.right_child, interval)
    # update max value in root node
    root_node.max_value = max(interval.upper, root_node.max_value)
    return root_node


def contains(elem: int, interval: Interval) -> bool:
    return interval.lower <= elem <= interval.upper


def tree_to_string(root_node: Node) -> None:
    if root_node.left_child is not None:
        tree_to_string(root_node.left_child)
    print(
        f"[{root_node.interval.lower}, {root_node.interval.upper}]; {root_node.max_value}",
    )
    if root_node.right_child is not None:
        tree_to_string(root_node.right_child)


def search_interval(root_node: Node | None, elem: int) -> Literal[0, 1]:
    # root empty
    if root_node is None:
        return 0

    # root interval contains element
    if contains(elem, root_node.interval):
        # print(
        #     f"elem {elem} is fresh, in interval [{root_node.interval.lower}, {root_node.interval.upper}]",
        # )
        return 1

    if root_node.left_child is not None and root_node.left_child.max_value >= elem:
        # print(
        #     f"search {elem} in interval left node with max value {root_node.left_child.max_value}",
        # )
        return search_interval(root_node.left_child, elem)
    return search_interval(root_node.right_child, elem)


with Path(sys.argv[1]).open() as file:
    root_node: Node | None = None
    fresh_ingredient_count = 0
    for line in file:
        if not line or line == "\n":
            break
        root_node = insert_node(
            root_node,
            Interval(lower=int(line.split("-")[0]), upper=int(line.split("-")[1])),
        )
    for line in file:
        fresh_ingredient_count += search_interval(root_node, int(line))

    print("Part 1:", fresh_ingredient_count)


########################### PART 2 ############################
def sort_and_merge_intervals(intervals: list) -> int:
    def get_lower(list_elem: str) -> str:
        return list_elem[0]

    intervals.sort(key=get_lower)
    intervals_length: int = len(intervals)
    indices_to_remove: list = []
    i = 0
    while i < intervals_length:
        j: int = i
        while j + 1 < intervals_length and intervals[i][1] >= intervals[j + 1][0]:
            intervals[i][1] = max(intervals[i][1], intervals[j + 1][1])
            indices_to_remove.append(j + 1)
            j += 1
        i = j + 1
    result_intervals = [
        list_elem for i, list_elem in enumerate(intervals) if i not in indices_to_remove
    ]
    return sum(
        [len(range(list_elem[0], list_elem[1] + 1)) for list_elem in result_intervals],
    )


with Path(sys.argv[1]).open() as file:
    root_node = None
    intervals: list = []
    for line in file:
        if not line or line == "\n":
            break
        intervals.append([int(line.split("-")[0]), int(line.split("-")[1])])

    print("Part 2:", sort_and_merge_intervals(intervals))
