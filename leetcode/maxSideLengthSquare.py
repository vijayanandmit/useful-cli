#Given a m x n matrix mat and an integer threshold, return the maximum side-length of a square with a sum less than or equal to threshold or return 0 if there is no such square.

 

#Example 1:


#Input: mat = [[1,1,3,2,4,3,2],[1,1,3,2,4,3,2],[1,1,3,2,4,3,2]], threshold = 4
#Output: 2
#Explanation: The maximum side length of square with sum less than 4 is 2 as shown.
#Example 2:

#Input: mat = [[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]], threshold = 1
#Output: 0

class Solution:
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        if not mat or not mat[0]:
            return 0
        
        m, n = len(mat), len(mat[0])
        
        # Create a prefix sum matrix
        prefix_sum = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                prefix_sum[i][j] = (mat[i - 1][j - 1] +
                                    prefix_sum[i - 1][j] +
                                    prefix_sum[i][j - 1] -
                                    prefix_sum[i - 1][j - 1])
        
        max_side = 0
        
        # Check for the largest square side length
        for side in range(1, min(m, n) + 1):
            for i in range(side, m + 1):
                for j in range(side, n + 1):
                    total = (prefix_sum[i][j] -
                            prefix_sum[i - side][j] -
                            prefix_sum[i][j - side] +
                            prefix_sum[i - side][j - side])
                    if total <= threshold:
                        max_side = side
        
        return max_side
