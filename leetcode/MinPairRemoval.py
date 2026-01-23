"""
Minimum Pair Removal (LeetCode-style).

Operation (repeat any number of times):
- Pick the adjacent pair with the minimum sum (leftmost on ties),
- Replace the pair with their sum.

Goal: return the minimum number of operations needed to make the array non-decreasing.

Approach
--------
We simulate the process efficiently:
- Maintain a doubly-linked list of "alive" nodes (the current array).
- Maintain a min-heap of adjacent pairs keyed by (pair_sum, left_index) to enforce
  the "minimum sum, then leftmost" selection rule.
- Use lazy deletion for heap entries via `(alive, next-pointer, version)` checks.
- Track the number of descents (i.e. adjacent inversions) so we can stop as soon as
  the list becomes non-decreasing.

Time: O(n log n) heap operations with lazy invalidation.
Space: O(n) for nodes + heap.
"""

from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from typing import List, Tuple


@dataclass
class _Node:
    # Current value for this position in the evolving array.
    value: int
    # Indices in the `nodes` array implementing an implicit doubly-linked list.
    # `-1` represents "null" (no neighbor).
    prev: int
    next: int
    # Whether this node still represents a live element in the list (merged-away nodes become dead).
    alive: bool = True
    # Incremented whenever `value` changes; used to lazily invalidate heap entries that referenced
    # an older state of this node.
    version: int = 0


class Solution:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        """
        Return the number of merges required to reach a non-decreasing array.

        Implementation notes:
        - Each original element is a node in an implicit doubly-linked list.
        - Each heap item stores: (pair_sum, left_id, right_id, left_version, right_version).
        - When a merge happens, only pairs touching the merged node can change.
        """
        n = len(nums)
        if n <= 1:
            return 0

        # Build an implicit doubly-linked list of nodes 0..n-1.
        # We'll "remove" nodes by marking them dead and relinking neighbors.
        nodes = [_Node(nums[i], i - 1, i + 1 if i + 1 < n else -1) for i in range(n)]

        def is_descent(left_id: int, right_id: int) -> bool:
            # True if the adjacent pair is decreasing (violates non-decreasing order).
            return nodes[left_id].value > nodes[right_id].value

        # Count how many adjacent inversions currently exist. Once it hits 0, the list is
        # non-decreasing and we can stop immediately.
        descents = 0
        for i in range(n - 1):
            if is_descent(i, i + 1):
                descents += 1

        heap: List[Tuple[int, int, int, int, int]] = []

        def push_pair(left_id: int, right_id: int) -> None:
            # Push the current adjacent pair into the heap.
            # Versions allow us to later detect if this entry is stale.
            left = nodes[left_id]
            right = nodes[right_id]
            heappush(
                heap,
                (
                    left.value + right.value,
                    left_id,
                    right_id,
                    left.version,
                    right.version,
                ),
            )

        # Initialize heap with all adjacent pairs from the original list.
        for i in range(n - 1):
            push_pair(i, i + 1)

        ops = 0
        while descents > 0:
            # Extract the valid minimum-sum adjacent pair.
            # We use lazy deletion: stale pairs are discarded until we find a consistent one.
            while True:
                pair_sum, left_id, right_id, left_ver, right_ver = heappop(heap)
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

            # Snapshot neighbors before the merge because we'll relink pointers.
            prev_id = left.prev
            next_id = right.next

            # Remove descents involving (prev,left), (left,right), (right,next) based on the
            # current (pre-merge) values. We'll add back any new descents after relinking.
            if prev_id != -1 and nodes[prev_id].alive and nodes[prev_id].next == left_id:
                if is_descent(prev_id, left_id):
                    descents -= 1
            if is_descent(left_id, right_id):
                descents -= 1
            if next_id != -1 and nodes[next_id].alive and nodes[right_id].next == next_id:
                if is_descent(right_id, next_id):
                    descents -= 1

            # Merge: replace (left,right) with their sum stored in `left`, and delete `right`.
            left.value = pair_sum
            left.version += 1
            right.alive = False

            # Splice `right` out of the list: left -> next, and next.prev -> left.
            left.next = next_id
            if next_id != -1:
                nodes[next_id].prev = left_id

            # Only pairs adjacent to `left` can change; update descent count and heap accordingly.
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
    """Slow reference implementation used for quick local validation (O(n^2) or worse)."""
    nums = nums[:]
    ops = 0

    def non_decreasing(a: List[int]) -> bool:
        return all(a[i] <= a[i + 1] for i in range(len(a) - 1))

    while len(nums) > 1 and not non_decreasing(nums):
        # Find the leftmost adjacent pair with minimum sum.
        min_sum = nums[0] + nums[1]
        min_i = 0
        for i in range(len(nums) - 1):
            s = nums[i] + nums[i + 1]
            if s < min_sum:
                min_sum = s
                min_i = i
        # Merge the chosen pair.
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
