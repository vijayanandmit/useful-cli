"""
Minimum Difference Between Highest and Lowest of K Scores (LeetCode 1984).

Given an array `nums` of student scores and an integer `k`, pick any `k` scores
such that the difference between the maximum and minimum of the chosen scores
is minimized. Return that minimum difference.

Approach
--------
Sort the array; for any optimal choice of `k` scores, they correspond to a
contiguous window in sorted order. Slide a window of size `k` and take the
minimum `sorted_nums[i+k-1] - sorted_nums[i]`.

Time: O(n log n) for sorting.
Space: O(1) extra (ignoring sort implementation details).
"""

from __future__ import annotations

from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0

        nums.sort()
        best = float("inf")
        for i in range(0, len(nums) - k + 1):
            best = min(best, nums[i + k - 1] - nums[i])
        return int(best)


if __name__ == "__main__":
    s = Solution()
    assert s.minimumDifference([90], 1) == 0
    assert s.minimumDifference([9, 4, 1, 7], 2) == 2
