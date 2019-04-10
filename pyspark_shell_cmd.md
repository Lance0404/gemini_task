
# pyspark shell cmd

* enter pyspark shell
```shell
spark - shell - -packages org.apache.spark: spark - sql - kafka - 0 - 10_2.12: 2.4.1
```
```
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
19 / 04 / 10 10: 43: 42 WARN Utils: Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
Spark context Web UI available at http: // 192.168.18.111: 4041
Spark context available as 'sc' (master=local[*], app id=local - 1554864222440).
Spark session available as 'spark'.
```

* under pyspark shell
```python
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
# import sys
import os

topic = 'firewall'
kafka_param = {
    "metadata.broker.list": 'localhost:9092',
    "auto.offset.reset": "smallest"
}

# sc = SparkContext(master='local[*]', appName='ps_consumer')

# print(sc)

ssc = StreamingContext(sc, 5)

# print(ssc)

directKafkaStream = KafkaUtils.createDirectStream(
    ssc, [topic], kafka_param)

# print(directKafkaStream)

lines = directKafkaStream.map(lambda x: json.loads(x[1]))

lines.pprint()

ssc.start()
ssc.awaitTermination()
```
