'''
purpose read from csv
'''

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
# from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
import sys
import os
import csv
from pyspark.sql import SQLContext
infile = "data/firewall.csv"
sc = SparkContext(master='local[*]', appName='ps_consumer')
sc.setLogLevel('INFO')


# ret = sc.textFile(infile) \
#     .map(lambda line: line.split(",")) \
#     .filter(lambda line: len(line) > 1) \
#     .map(lambda line: (line[0], line[1])) \
#     .collect()
ret = sc.textFile(infile) \
    .map(lambda line: line.split(",")) \
    .filter(lambda line: len(line) > 1) \
    .collect()


print(ret)
print(len(ret))

exit()

sqlContext = SQLContext(sc)

df = sqlContext.read.format('com.databricks.spark.csv') \
    .options(header='true', inferschema='true') \
    .load(infile)


exit()


def printline(s):
    print(s)


sc = SparkContext(master='local[*]', appName='ps_consumer')
sc.setLogLevel('INFO')

rdd = sc.textFile(infile)
# print(rdd.map(printline).collect())
rdd = rdd.map(lambda x: csv.reader(x))
print(rdd.collect())

exit()

rdd.take(5)
rddlens = rdd.map(lambda s: len(s))
print(f'rddlens {rddlens}')

rdd.map(printline)
