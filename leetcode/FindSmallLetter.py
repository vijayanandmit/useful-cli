"""
Find Smallest Letter Greater Than Target

You are given an array of characters letters that is sorted in non-decreasing order, and a character target. There are at least two different characters in letters.

Return the smallest character in letters that is lexicographically greater than target. If such a character does not exist, return the first character in letters.
"""
class Solution:
    def nextGreatestLetter(self, L: List[str], target: str) -> str:
        i=bisect_right(L, target)
        return L[i] if i<len(L) else L[0]
        
