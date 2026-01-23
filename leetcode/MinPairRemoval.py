"""
Given an array nums, you can perform the following operation any number of times:

Select the adjacent pair with the minimum sum in nums. If multiple such pairs exist,
choose the leftmost one. Replace the pair with their sum.

Return the minimum number of operations needed to make the array non-decreasing.
"""

from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import List, Tuple


@dataclass
class _Node:
    value: int
    prev: int
    next: int
    alive: bool = True
    version: int = 0


class Solution:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 1:
            return 0

        nodes = [_Node(nums[i], i - 1, i + 1 if i + 1 < n else -1) for i in range(n)]

        def is_descent(left_id: int, right_id: int) -> bool:
            return nodes[left_id].value > nodes[right_id].value

        descents = 0
        for i in range(n - 1):
            if is_descent(i, i + 1):
                descents += 1

        heap: List[Tuple[int, int, int, int, int, int]] = []

        def push_pair(left_id: int, right_id: int) -> None:
            left = nodes[left_id]
            right = nodes[right_id]
            heappush(
                heap,
                (
                    left.value + right.value,
                    left_id,  # leftmost tiebreak
                    left_id,
                    right_id,
                    left.version,
                    right.version,
                ),
            )

        for i in range(n - 1):
            push_pair(i, i + 1)

        ops = 0
        while descents > 0:
            while True:
                pair_sum, left_pos, left_id, right_id, left_ver, right_ver = heappop(heap)
                left = nodes[left_id]
                right = nodes[right_id]
                if (
                    left.alive
                    and right.alive
                    and left.next == right_id
                    and left.version == left_ver
                    and right.version == right_ver
                ):
                    break

            prev_id = left.prev
            next_id = right.next

            if prev_id != -1 and nodes[prev_id].alive and nodes[prev_id].next == left_id:
                if is_descent(prev_id, left_id):
                    descents -= 1
            if is_descent(left_id, right_id):
                descents -= 1
            if next_id != -1 and nodes[next_id].alive and nodes[right_id].next == next_id:
                if is_descent(right_id, next_id):
                    descents -= 1

            left.value = pair_sum
            left.version += 1
            right.alive = False

            left.next = next_id
            if next_id != -1:
                nodes[next_id].prev = left_id

            if prev_id != -1 and nodes[prev_id].alive:
                if is_descent(prev_id, left_id):
                    descents += 1
                push_pair(prev_id, left_id)

            if next_id != -1 and nodes[next_id].alive:
                if is_descent(left_id, next_id):
                    descents += 1
                push_pair(left_id, next_id)

            ops += 1

        return ops


def _naive_minimum_pair_removal(nums: List[int]) -> int:
    nums = nums[:]
    ops = 0

    def non_decreasing(a: List[int]) -> bool:
        return all(a[i] <= a[i + 1] for i in range(len(a) - 1))

    while len(nums) > 1 and not non_decreasing(nums):
        min_sum = nums[0] + nums[1]
        min_i = 0
        for i in range(len(nums) - 1):
            s = nums[i] + nums[i + 1]
            if s < min_sum:
                min_sum = s
                min_i = i
        nums[min_i] = min_sum
        nums.pop(min_i + 1)
        ops += 1

    return ops


# if __name__ == "__main__":
#     import random
#
#     s = Solution()
#     assert s.minimumPairRemoval([5, 2, 3, 1]) == 2
#     assert s.minimumPairRemoval([1, 2, 2]) == 0
#     assert s.minimumPairRemoval([2, 1]) == 1
#     assert s.minimumPairRemoval([1]) == 0
#
#     for _ in range(300):
#         n = random.randint(1, 20)
#         arr = [random.randint(-10, 10) for _ in range(n)]
#         got = s.minimumPairRemoval(arr)
#         exp = _naive_minimum_pair_removal(arr)
#         assert got == exp, (arr, got, exp)
#
#     print("OK")
