"""
Minimum Cost Path With Edge Reversals (node switches).

You are given a directed, weighted graph with `n` nodes labeled `0..n-1` and
`edges[i] = [u, v, w]` representing a directed edge `u -> v` with cost `w`.

Each node `x` has a switch that can be used at most once: when you are at `x`
and its switch is unused, you may pick one of its incoming edges `p -> x`,
temporarily reverse it into `x -> p`, and immediately traverse it at cost
`2*w` (where `w` is the original edge weight). The reversal is valid only for
that single move.

Return the minimum total cost to travel from node `0` to node `n - 1`, or `-1`
if it's not possible.

Approach
--------
Using a node's switch for a single move is equivalent to having an additional
edge for each original edge `u -> v`:

  - forward move:  `u -> v` with cost `w`
  - reversed move: `v -> u` with cost `2*w`

With strictly positive weights, an optimal path never needs to traverse more
than one reversed edge out of the same node: using a reversed edge requires
being at that node, and using a second reversed edge would require returning
to the node (a positive-cost cycle), which can be removed or replaced by using
the switch on the first visit.

So we can run Dijkstra on the graph augmented with these reverse-cost edges.

Time:  O((n + m) log n)
Space: O(n + m)
"""

from __future__ import annotations

import heapq
from typing import List, Tuple


class Solution:
    def minCost(self, n: int, edges: List[List[int]]) -> int:
        if n <= 1:
            return 0

        graph: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, 2 * w))

        dist = [10**30] * n
        dist[0] = 0
        pq: List[Tuple[int, int]] = [(0, 0)]

        while pq:
            cur_cost, node = heapq.heappop(pq)
            if cur_cost != dist[node]:
                continue
            if node == n - 1:
                return cur_cost

            for nxt, w in graph[node]:
                cand = cur_cost + w
                if cand < dist[nxt]:
                    dist[nxt] = cand
                    heapq.heappush(pq, (cand, nxt))

        return -1

    # Common alternative naming for this prompt/file name.
    def minCostPathEdgeReversals(self, n: int, edges: List[List[int]]) -> int:
        return self.minCost(n, edges)


if __name__ == "__main__":
    s = Solution()
    assert s.minCost(4, [[0, 1, 3], [3, 1, 1], [2, 3, 4], [0, 2, 2]]) == 5
    assert s.minCost(3, [[0, 1, 5]]) == -1
    assert s.minCost(1, []) == 0
