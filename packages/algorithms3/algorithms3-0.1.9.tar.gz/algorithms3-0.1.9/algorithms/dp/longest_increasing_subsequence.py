'''
Given an unsorted array of integers, find the length of longest increasing 
subsequence.

Example:

Input: [10,9,2,5,3,7,101,18]
Output: 4 
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the 
length is 4. 
Note:

There may be more than one LIS combination, it is only necessary for you to 
return the length.
Your algorithm should run in O(n2) complexity.
'''

def longest_inc(word):
    cache = [1]*len(word)

    for i in range(1, len(word)):
        for j in range(i):
            if word[i] > word[j]:
                cache[i] = max(cache[i], 1+cache[j])

    return max(cache)

