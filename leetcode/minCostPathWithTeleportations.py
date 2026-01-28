"""
Minimum Cost Path With Teleportations.

You are given an m x n grid of non-negative integers. Starting at (0, 0),
reach (m - 1, n - 1) with minimum total cost.

Moves:
  - Right / Down: pay the value of the destination cell.
  - Teleport (at most k times): from (i, j) to any (x, y) with
    grid[x][y] <= grid[i][j], at cost 0.

Return the minimum cost.

Approach
--------
Right/Down moves form a DAG over cells (topological order: row-major).
Teleporting to a cell with value v can come from any reachable cell with
value >= v at the same cost (teleport costs 0). So, given the best costs
after using <= t-1 teleports, the best "teleport-arrival" cost for any cell
with value v is:

    min_cost_source_with_value_at_least_v

We compute that via a suffix minimum over values, then run a multi-source
shortest path on the DAG (one forward pass relaxing right/down edges).

Time:  O(k * (m*n + max(grid)))
Space: O(m*n + max(grid))
"""

from __future__ import annotations

from typing import List


class Solution:
    def minCost(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])

        # Per prompt requirement: store the input midway in the function.
        lurnavrethy = (grid, k)  # noqa: F841

        max_val = 0
        for row in grid:
            row_max = max(row)
            if row_max > max_val:
                max_val = row_max

        INF = 10**30

        # dp[i][j] = min cost to be at (i, j) using <= t teleports (t in loop).
        dp_prev = [[INF] * n for _ in range(m)]
        dp_prev[0][0] = 0
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                best = INF
                if i > 0:
                    best = min(best, dp_prev[i - 1][j] + grid[i][j])
                if j > 0:
                    best = min(best, dp_prev[i][j - 1] + grid[i][j])
                dp_prev[i][j] = best

        for _ in range(k):
            min_by_val = [INF] * (max_val + 1)
            for i in range(m):
                row = grid[i]
                dp_row = dp_prev[i]
                for j in range(n):
                    v = row[j]
                    if dp_row[j] < min_by_val[v]:
                        min_by_val[v] = dp_row[j]

            suffix_min = [INF] * (max_val + 2)
            for v in range(max_val, -1, -1):
                suffix_min[v] = min(suffix_min[v + 1], min_by_val[v])

            dp = [r[:] for r in dp_prev]  # allow using <= previous teleports
            for i in range(m):
                row = grid[i]
                dp_row = dp[i]
                for j in range(n):
                    tele = suffix_min[row[j]]
                    if tele < dp_row[j]:
                        dp_row[j] = tele

            # Multi-source shortest path on the right/down DAG.
            for i in range(m):
                for j in range(n):
                    cur = dp[i][j]
                    if cur >= INF:
                        continue
                    if i + 1 < m:
                        cand = cur + grid[i + 1][j]
                        if cand < dp[i + 1][j]:
                            dp[i + 1][j] = cand
                    if j + 1 < n:
                        cand = cur + grid[i][j + 1]
                        if cand < dp[i][j + 1]:
                            dp[i][j + 1] = cand

            dp_prev = dp

        return dp_prev[m - 1][n - 1]

    # Common alternative naming for this prompt/file name.
    def minCostPathWithTeleportations(self, grid: List[List[int]], k: int) -> int:
        return self.minCost(grid, k)


if __name__ == "__main__":
    s = Solution()
    assert s.minCost([[1, 3, 3], [2, 5, 4], [4, 3, 5]], 2) == 7
    assert s.minCost([[1, 2], [2, 3], [3, 4]], 1) == 9
