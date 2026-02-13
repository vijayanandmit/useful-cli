"""
Longest Balanced Substring II (LeetCode 3714).

A substring is balanced if all characters that appear in it appear the same
number of times. The string consists only of 'a', 'b', and 'c'.

With a 3-letter alphabet, a balanced substring must be one of:
1) only one letter: (t, 0, 0)
2) exactly two letters with equal counts: (t, t, 0)
3) all three letters with equal counts: (t, t, t)

We compute the best length for each case in O(n) total:
- Case (t, 0, 0): longest run of a single character.
- Case (t, t, 0): for each pair (x, y) with third char z absent,
  keep earliest index by key (pref[x] - pref[y], pref[z]).
- Case (t, t, t): keep earliest index by key
  (pref[a] - pref[b], pref[a] - pref[c]).

Time: O(n)
Space: O(n)
"""

from __future__ import annotations


class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)
        idx = {"a": 0, "b": 1, "c": 2}

        pref = [[0] * (n + 1) for _ in range(3)]
        for i, ch in enumerate(s, start=1):
            for k in range(3):
                pref[k][i] = pref[k][i - 1]
            pref[idx[ch]][i] += 1

        ans = 0

        # Case 1: one-letter substring.
        run = 0
        prev = ""
        for ch in s:
            if ch == prev:
                run += 1
            else:
                run = 1
                prev = ch
            ans = max(ans, run)

        # Case 2: two-letter substrings with equal counts and no third letter.
        pairs = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]
        for x, y, z in pairs:
            first = {(0, 0): 0}
            for i in range(1, n + 1):
                key = (pref[x][i] - pref[y][i], pref[z][i])
                if key in first:
                    ans = max(ans, i - first[key])
                else:
                    first[key] = i

        # Case 3: all three letters appear equally often.
        first_abc = {(0, 0): 0}
        for i in range(1, n + 1):
            key = (pref[0][i] - pref[1][i], pref[0][i] - pref[2][i])
            if key in first_abc:
                ans = max(ans, i - first_abc[key])
            else:
                first_abc[key] = i

        return ans


if __name__ == "__main__":
    sol = Solution()
    assert sol.longestBalanced("abccab") == 6
    assert sol.longestBalanced("aabb") == 4
    assert sol.longestBalanced("abcabc") == 6
    assert sol.longestBalanced("abba") == 4
    assert sol.longestBalanced("aaaa") == 4
    assert sol.longestBalanced("aba") == 2
    assert sol.longestBalanced("a") == 1
