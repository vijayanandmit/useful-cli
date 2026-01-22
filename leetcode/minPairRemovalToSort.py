#Given an array nums, you can perform the following operation any number of times:

#Select the adjacent pair with the minimum sum in nums. If multiple such pairs exist, choose the leftmost one.
#Replace the pair with their sum.
#Return the minimum number of operations needed to make the array non-decreasing.

#An array is said to be non-decreasing if each element is greater than or equal to its previous element (if it exists).


#Example 1:

#Input: nums = [5,2,3,1]

#Output: 2

#Explanation:

#The pair (3,1) has the minimum sum of 4. After replacement, nums = [5,2,4].
#The pair (2,4) has the minimum sum of 6. After replacement, nums = [5,6].
#The array nums became non-decreasing in two operations

class Solution:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        count = 0

        while len(nums) > 1:
            isAscending = True
            minSum = float("inf")
            targetIndex = -1

            for i in range(len(nums) - 1):
                pair_sum = nums[i] + nums[i + 1]

                if nums[i] > nums[i + 1]:
                    isAscending = False

                if pair_sum < minSum:
                    minSum = pair_sum
                    targetIndex = i

            if isAscending:
                break

            count += 1
            nums[targetIndex] = minSum
            nums.pop(targetIndex + 1)

        return count
