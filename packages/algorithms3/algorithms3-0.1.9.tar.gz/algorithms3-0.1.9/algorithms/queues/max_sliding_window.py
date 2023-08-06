'''
Given an array nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position. Return the max sliding window.

Example:

Input: nums = [1,3,-1,-3,5,3,6,7], and k = 3
Output: [3,3,5,5,6,7] 
Explanation: 

Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
Note: 
You may assume k is always valid, 1 ≤ k ≤ input array's size for non-empty array.

Follow up:
Could you solve it in linear time?
'''

from collections import deque
class MaxQue:
    def __init__(self):
        self.que = deque()

    def push(self, x):
        count = 0
        while self.que and self.que[-1][0] < x:
            count += self.que[-1][1] + 1
            self.que.pop()
        self.que.append([x, count])
    
    def pop(self):
        if self.que[0][1] > 0:
            self.que[0][1] -= 1
            return
        self.que.popleft()
    
    def get_max(self):
        return self.que[0][0]


def max_sliding_window(nums, k: int):
    que = MaxQue()
    result = []
    for i in range(k):
        que.push(nums[i])
    
    result.append(que.get_max())
    
    for i in range(k, len(nums)):
        que.pop()
        que.push(nums[i])
        result.append(que.get_max())
    
    return result
