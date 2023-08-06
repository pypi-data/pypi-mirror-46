'''
Implement strStr().

Return the index of the first occurrence of needle in haystack, or -1 if needle is not 
part of haystack.

Example 1:
Input: haystack = "hello", needle = "ll"
Output: 2

Example 2:
Input: haystack = "aaaaa", needle = "bba"
Output: -1
'''

def strstr(haystack:str, needle:str) -> int:
    n = len(needle)
    if n == 0: return 0
    if n > len(haystack): return -1
    for i in range(len(haystack)-n+1):
        if haystack[i:i+n] == needle:
            return i
    return -1 
