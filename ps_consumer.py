'''
issues:
https://github.com/jupyter/docker-stacks/issues/743

after setting:
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8:2.4.1 pyspark-shell'

another issue appeared:
module not found: org.apache.spark#spark-streaming-kafka-0-8;2.4.1

19/04/10 16:34:30 WARN Utils: Your hostname, ubuntu resolves to a loopback address: 127.0.1.1; using 192.168.18.111 instead (on interface ens160)
19/04/10 16:34:30 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address

https://stackoverflow.com/questions/2801087/java-nio-channels-closedchannelexception

# stared
https://github.com/claudiofahey/global_anomaly_detection_demo/blob/master/spark_streaming_processor.py

https://stackoverflow.com/questions/31076224/create-spark-dataframe-in-spark-streaming-from-json-message-on-kafka

'''

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark.sql import Row, SparkSession, SQLContext
from pyspark.streaming.util import rddToFileName
import sys
import os
import json
'''
* approach 1
kafkaStream = KafkaUtils.createStream(streamingContext,
                                      [ZK quorum], [consumer group id], [per - topic number of Kafka partitions to consume])
# approach 2
directKafkaStream = KafkaUtils.createDirectStream(
    ssc, [topic], {"metadata.broker.list": brokers})

'''


def getSqlContextInstance(sparkContext):
    """Lazily instantiated global instance of SQLContext
    Below from https://spark.apache.org/docs/1.5.2/streaming-programming-guide.html#dataframe-and-sql-operations."""
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(sparkContext)
    return globals()['sqlContextSingletonInstance']


def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']


def dict2sqlrow(x: dict):

    tmp = {
        'timestamp': x['timestamp'],
        'user': x['user'],
        'action': x['action'],
        'app': x['app'],
        'server': x['server']
    }
    return Row(**tmp)


def dict2tuple(x: dict):
    tmp = (x['timestamp'], x['user'], x['action'], x['app'], x['server'])
    return tmp


def json_to_row(s):
    return Row(**json.loads(s))


def dosth(time, rdd, spark):
    if rdd.isEmpty():
        return
    sqlContext = getSqlContextInstance(rdd.context)
    df = sqlContext.createDataFrame(rdd)
    df.show()
    df.printSchema()
    df.groupBy("user").count().show()

    df.createOrReplaceTempView('firewall')
    sqlDF = spark.sql("select * from firewall limit 3")
    sqlDF.show()
    if 0:
        enriched_data_path = 'data/firewall_df.json'
        if enriched_data_path:
            path = rddToFileName(enriched_data_path, None, time)
            df.write.json(path, mode='error')

    # return rdd.collect()


if __name__ == '__main__':

    # os.environ['SPARK_LOCAL_IP'] = '172.0.0.1'
    # os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8:2.4.1 pyspark-shell'

    sc_conf = SparkConf()
    sc_conf.setAppName('ps_consumer')
    sc_conf.setMaster('local[*]')
    # sc_conf.set('spark.executor.memory', '2g')
    # sc_conf.set('spark.executor.cores', '4')
    # sc_conf.set('spark.cores.max', '40')
    sc_conf.set('spark.logConf', True)
    sc_conf.set('spark.io.compression.codec', 'snappy')

    # spark = SparkSession \
    #     .builder \
    #     .appName("Python Spark SQL basic example") \
    #     .config(conf=sc_conf) \
    #     .getOrCreate()

    # sc = SparkContext(master='local[*]', appName='ps_consumer')
    sc = SparkContext(conf=sc_conf)
    sc.setLogLevel('INFO')
    # print(sc)

    ssc = StreamingContext(sc, 5)
    # print(ssc)

    topic = 'firewall'
    partition = 0
    kafka_param = {
        "metadata.broker.list": 'localhost:9092',
        "auto.offset.reset": "smallest",
        "group.id": 'mygroup',
    }
    # topicPartion = TopicAndPartition(topic, partition)
    # fromOffsets = {topicPartion: 500}
    # stream = KafkaUtils.createDirectStream(
    # ssc, [topic], kafka_param, fromOffsets=fromOffsets)

    stream = KafkaUtils.createDirectStream(
        ssc, [topic], kafka_param)
    # print(stream)
    messages = stream.map(lambda x: x[1])
    rows = messages.map(json_to_row)

    spark = SparkSession.builder.config(conf=sc_conf).getOrCreate()

    rows.foreachRDD(lambda t, rdd: dosth(t, rdd, spark))

    # lines = stream.map(lambda x: json.loads(x[1]))
    # print(f'lines type {type(lines)}')
    # lines = lines.map(lambda y: (
    # y['timestamp'], y['user'], y['action'], y['app'], y['server']))
    # lines.pprint()

    # df =

    # users = lines.map(lambda x: x['user'])
    # users.pprint()
    # tmp = (x['timestamp'], x['user'], x['action'], x['app'], x['server'])
    # spark = SparkSession(sc)
    if 0:
        col_header = ['timestamp', 'user', 'action', 'app', 'server']
        df = lines.toDF(col_header)
        df.show()

    if 0:

        # Convert RDDs of the words DStream to DataFrame and run SQL query

        # def process(time, rdd):
        def process(rdd):
            # print("========= %s =========" % str(time))
            spark = SparkSession.builder.config(conf=sc_conf).getOrCreate()
            # spark = getSparkSessionInstance(rdd.context.getConf())

            rowRdd = rdd.map(dict2sqlrow)
            # rowRdd = rdd.map(lambda w: Row(user=w))
            print(dir(rowRdd))
            print(type(rowRdd))
            rowRdd.collect()
            # print(rowRdd.toDF())
            # rowRdd.pprint()

            # https://stackoverflow.com/questions/44355416/need-instance-of-rdd-but-returned-class-pyspark-rdd-pipelinedrdd

            # df = spark.createDataFrame(rowRdd)
            # df.show()
            # df.createOrReplaceTempView("firewall")

            # aggdf = spark.sql(
            #     "select user, count(*) as ucount from firewall group by user")
            # aggdf.show()

        lines.foreachRDD(process)
        # users.foreachRDD(process(users))

    ssc.start()
    ssc.awaitTermination()

    # sys.exit() # checkpoint
