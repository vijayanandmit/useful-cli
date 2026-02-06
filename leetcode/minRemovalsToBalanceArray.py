"""
Minimum Removals to Balance Array (LeetCode 3634).

An array is balanced if max(nums) <= k * min(nums). We can remove any number
of elements as long as at least one remains. The goal is to minimize removals.

Approach
--------
Sort the array. In sorted order, any balanced remaining set corresponds to a
contiguous window [l, r] with nums[r] <= nums[l] * k. Use a sliding window to
find the maximum window length; answer is n - max_len.

Time: O(n log n) due to sorting.
Space: O(1) extra (ignoring sort internals).
"""

from __future__ import annotations

from typing import List


class Solution:
    def minRemoval(self, nums: List[int], k: int) -> int:
        if not nums:
            return 0

        nums.sort()
        n = len(nums)
        best = 1
        l = 0

        for r in range(n):
            while nums[r] > nums[l] * k:
                l += 1
            best = max(best, r - l + 1)

        return n - best


if __name__ == "__main__":
    s = Solution()
    assert s.minRemoval([2, 1, 5], 2) == 1
    assert s.minRemoval([1, 6, 2, 9], 3) == 2
    assert s.minRemoval([4, 6], 2) == 0
    assert s.minRemoval([10], 1) == 0
