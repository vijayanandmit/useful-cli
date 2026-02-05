from __future__ import annotations

from typing import List


# You are given a 0-indexed integer array nums of length n.
#
# Create an array ans of length n where:
# - if nums[i] > 0, ans[i] = nums[(i + nums[i]) % n]
# - if nums[i] < 0, ans[i] = nums[(i - abs(nums[i])) % n]
# - if nums[i] == 0, ans[i] = nums[i]
#
# Return ans.


class Solution:
    def constructTransformedArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        return [nums[(i + v) % n] for i, v in enumerate(nums)]


if __name__ == "__main__":
    s = Solution()
    assert s.constructTransformedArray([3, -2, 1, 1]) == [1, 1, 1, 3]
    assert s.constructTransformedArray([-1, 4, -1]) == [-1, -1, 4]
