# Feature 2: Calculate the median number of unique words per tweet, and update 
# this median as tweets come in. 

# My design approach is to use the two heaps solution to the streaming median
# problem.  It has O(logN) time complexity so should scale well.  
# The weakness is that the heaps will eventually exhaust memory.  I see no
# good solution to this unless you change the requirement to a moving window
# median or a statistical estimation of the median using sampling or binning.

"""
Thanks to Arden Dertat for the streamMedian class.
http://www.ardendertat.com/2011/11/03/programming-interview-questions-13-median-of-integer-stream/  
"""
import sys
import heapq

class streamMedian: 
  def __init__(self): 
    self.minHeap, self.maxHeap = [], [] 
    self.N=0   
    
  def insert(self, num): 
    if self.N%2==0: 
      heapq.heappush(self.maxHeap, -1*num) 
      self.N+=1 
      if len(self.minHeap)==0: 
        return 
      if -1*self.maxHeap[0]>self.minHeap[0]: 
        toMin=-1*heapq.heappop(self.maxHeap) 
        toMax=heapq.heappop(self.minHeap) 
        heapq.heappush(self.maxHeap, -1*toMax) 
        heapq.heappush(self.minHeap, toMin) 
    else: 
      toMin=-1*heapq.heappushpop(self.maxHeap, -1*num) 
      heapq.heappush(self.minHeap, toMin) 
      self.N+=1   
      
  def getMedian(self): 
    if self.N%2==0: 
      return (-1*self.maxHeap[0]+self.minHeap[0])/2.0 
    else: 
      return -1*self.maxHeap[0]

def printmedian(filename):
  f = open(filename,'r') # open file read only no unicode
  sm = streamMedian()
  for line in f: # looping over file object is fast and memory efficient
    # split line on whitespace, get unique words, get number, insert
    # the insert operation is O(logn)
    sm.insert(len(set(line.split())))
    # calculate median, O(1)
    print sm.getMedian()
  f.close()
  
def main():
  if len(sys.argv) != 2:
    print 'usage: ./median_unique.py file'
    sys.exit(1)

  filename = sys.argv[1]
  printmedian(filename)

if __name__ == '__main__':
  main()