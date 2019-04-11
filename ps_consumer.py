from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark.sql import Row, SparkSession, SQLContext
from pyspark.streaming.util import rddToFileName
import sys
import os
import json

def getSqlContextInstance(sparkContext):
    """Lazily instantiated global instance of SQLContext
    Below from https://spark.apache.org/docs/1.5.2/streaming-programming-guide.html#dataframe-and-sql-operations."""
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(sparkContext)
    return globals()['sqlContextSingletonInstance']


def getSparkSessionInstance(sparkConf):
    '''
    not used
    '''
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']


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
    sqlDF = spark.sql("select server,app,count(*) from firewall group by server, app, action")
    sqlDF.show()

    sqlDF.write.parquet("data/firewall.parquet")

    if 0:
        enriched_data_path = 'data/firewall_df.json'
        if enriched_data_path:
            path = rddToFileName(enriched_data_path, None, time)
            df.write.json(path, mode='error')




if __name__ == '__main__':

    sc_conf = SparkConf()
    sc_conf.setAppName('ps_consumer')
    sc_conf.setMaster('local[*]')
    # sc_conf.set('spark.executor.memory', '2g')
    # sc_conf.set('spark.executor.cores', '4')
    # sc_conf.set('spark.cores.max', '40')
    sc_conf.set('spark.logConf', True)
    sc_conf.set('spark.io.compression.codec', 'snappy')

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

    messages = stream.map(lambda x: x[1])
    rows = messages.map(json_to_row)

    spark = SparkSession.builder.config(conf=sc_conf).getOrCreate()

    rows.foreachRDD(lambda t, rdd: dosth(t, rdd, spark))


    ssc.start()
    ssc.awaitTermination()

    # sys.exit() # checkpoint
