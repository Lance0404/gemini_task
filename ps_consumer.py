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



'''

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
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

    # sc = SparkContext(master='local[*]', appName='ps_consumer')
    sc = SparkContext(conf=sc_conf)
    sc.setLogLevel('WARN')
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
    # directKafkaStream = KafkaUtils.createDirectStream(
    # ssc, [topic], kafka_param, fromOffsets=fromOffsets)

    directKafkaStream = KafkaUtils.createDirectStream(
        ssc, [topic], kafka_param)
    print(directKafkaStream)

    lines = directKafkaStream.map(lambda x: json.loads(x[1]))
    lines.pprint()
    ssc.start()
    ssc.awaitTermination()

    # sys.exit()
