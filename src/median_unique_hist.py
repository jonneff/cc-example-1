# Feature 2: Calculate the median number of unique words per tweet, and update 
# this median as tweets come in. 

# Updated design approach:  use a Python dictionary to store the NUMBER of times
# a certain number of words in a tweet has been observed.  Since tweets are 
# limited to 140 characters, max key is 140.  For 1 month of tweets, values
# on the order of # tweets per month = about 15 billion.  You could keep doing
# this for a very long time.  We are creating a histogram of number of words
# per tweet.

import sys

def printmedian(filename):
  
  # initialize histogram dictionary, keys are word counts per tweet
  hist = {i: 0 for i in range(141)}
    
  f = open(filename,'r') # open file read only no unicode
  
  for line in f: # looping over file object is fast and memory efficient
    # split line on whitespace, get unique words, get number of unique words
    knum = len(set(line.split()))
    
    # update number of times this word count has been observed, O(1)
    hist[knum] += 1
    
    # calculate median
    # 1.  calculate median location using sum of word counts
    sumwc = sum(hist.itervalues())
    if sumwc == 0 or sumwc == 1:  # zero word tweets OR first tweet
      print knum
      continue
    medianloc = sumwc//2
    
    # 2.  odd number of word counts?
    if sumwc%2 != 0:
      medianloc += 1 # median is the middle number
      odd = True
    else:
      odd = False # even number, median will be average of 2 numbers
    
    # 3.  find bin containing median
    
    if odd:
      median = findbin(medianloc, hist)
      print median
    else:
      # have to find two "middle" numbers
      lower = findbin(medianloc, hist)
      next = medianloc + 1
      upper = findbin(next, hist)
      median = float(lower + upper)/2
      print median
    
  f.close()

def findbin(loc, hist):
  # iterate cumulative sum to find bin containing a location
  cumsum = 0
  for i in range(141):
    cumsum += hist[i]
    if cumsum >= loc:
      break
  return i 
  
def main():
  if len(sys.argv) != 2:
    print 'usage: ./median_unique_hist.py file'
    sys.exit(1)

  filename = sys.argv[1]
  printmedian(filename)

if __name__ == '__main__':
  main()