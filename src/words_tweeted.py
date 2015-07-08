# Feature 1:  Calculate the total number of times each word has been tweeted.
# My design approach is to use map and reduce in Spark context.

# First, initialize SparkContext

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("Words Tweeted")
sc = SparkContext(conf = conf)

# Open file and read data into Spark Resilient Distributed Dataset (RDD)
# In real life we would be creating RDD from HDFS.   

tweetsRDD = sc.textFile("./tweet_input/tweets.txt")

# Get tuples with counts of each word.
# Use flatMap() initially instead of map() because   
# map() would produce nested lists of tuples with split().
# Use map() create pair RDD, i.e., key-value pairs, set count 1 for each word.
# Then use reduceByKey() to accumulate counts for each unique word.
# reduceByKey() scales well to large datasets, unlike groupByKey().
# We end up with a pair RDD wordsAndCounts, sorted by key.  

wordsAndCounts = (tweetsRDD
                  .flatMap(lambda line: line.split(' ')) 
                  .map(lambda x: (x,1))
                  .reduceByKey(lambda x,y: x+y)
                  .sortByKey()
                  )
 
# I WOULD NEVER DO THE NEXT THING IN REAL LIFE BECAUSE IT DOES NOT SCALE.
# If I were really working with a huge dataset, I would do something like
# .saveAsTextFile() on HDFS in the wordsAndCounts pipeline above.  
# In order to save as a text file with a specific name I use .collect():

for kv in wordsAndCounts.collect():
  print kv[0] + " " + str(kv[1])

