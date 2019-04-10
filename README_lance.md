# assignment
* Consume data froma Kafka topic using Spark (pyspark)
* Perform an aggregation of your preference on the consumed data 
* Saved aggregated data to a file (preferably parquet format, other text formats are ok)
* Setup a simple Kafka environment with docker (instructions provided in attachment)


# background study
* [Apache Parquet: Parquet file internals and inspecting Parquet file structure](https://youtu.be/rVC9F1y38oU)
* [Spark + Parquet In Depth: Spark Summit East talk by: Emily Curtin and Robbie Strickland](https://youtu.be/_0Wpwj_gvzg)


# upgrade my docker-compose
* version check
```shell
docker -v
Docker version 18.06.1-ce, build e68fc7a
docker-compose -v
docker-compose version 1.18.0, build 8dd22a9
```
* [ref](https://docs.docker.com/compose/install/)

* procedure
```shell
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
* check version
```shell
docker-compose version
docker-compose version 1.24.0, build 0aa59064
docker-py version: 3.7.2
CPython version: 3.6.8
OpenSSL version: OpenSSL 1.1.0j  20 Nov 2018
```

* install pipenv python3.7
```
pipenv --python 3.7

pipenv shell

pipenv install pyspark
```

* install pyspark(standalone) 2.4.1
```shell
(gemini_task) root@ubuntu:/home/lance/gemini_task# pyspark
Python 3.7.2 (default, Jan 11 2019, 21:31:15)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
19/04/10 08:24:40 WARN Utils: Your hostname, ubuntu resolves to a loopback address: 127.0.1.1; using 192.168.18.111 instead (on interface ens160)
19/04/10 08:24:40 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
19/04/10 08:24:41 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.4.1
      /_/

Using Python version 3.7.2 (default, Jan 11 2019 21:31:15)
SparkSession available as 'spark'.
>>>

```


# issues
* port occupied 
```
ERROR: for zookeeper  Cannot start service zookeeper: driver failed programming external connectivity on endpoint zookeeper (9ddc14efb025aa97cf367f434ec3de4aabbd8763dd1c6a2528e6933ffa64ecc7): Error starting userland proxy: listen tcp 0.0.0.0:2181: bind: address already in use
```
* solved
```
netstat -nalp | grep 2181
tcp6       0      0 :::2181                 :::*                    LISTEN      19520/java

ps -ef | grep 19520
root     19520     1  0  2018 ?        04:25:41 java -Xmx512M -Xms512M -server -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:+ExplicitGCInvokesConcurrent -Djava.awt.headless=true -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dkafka.logs.dir=/tmp/confluent.iDxsNeml/zookeeper/logs -Dlog4j.configuration=file:/usr/local/confluent-4.1.1/bin/../etc/kafka/log4j.properties -cp /usr/local/confluent-4.1.1/bin/../share/java/kafka/*:/usr/local/confluent-4.1.1/bin/../share/java/confluent-support-metrics/*:/usr/share/java/confluent-support-metrics/* org.apache.zookeeper.server.quorum.QuorumPeerMain /tmp/confluent.iDxsNeml/zookeeper/zookeeper.properties

kill 19520
# gone
```

* pyspark issues
```shell
________________________________________________________________________________________________

  Spark Streaming's Kafka libraries not found in class path. Try one of the following.

  1. Include the Kafka library and its dependencies with in the
     spark-submit command as

     $ bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8:2.4.1 ...

  2. Download the JAR of the artifact from Maven Central http://search.maven.org/,
     Group Id = org.apache.spark, Artifact Id = spark-streaming-kafka-0-8-assembly, Version = 2.4.1.
     Then, include the jar in the spark-submit command as

     $ bin/spark-submit --jars <spark-streaming-kafka-0-8-assembly.jar> ...

________________________________________________________________________________________________
```
* debug
```shell
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8:2.4.1
```
* enter pyspark shell
```
>>> dir(sc._jvm.org.apache.spark.streaming.kafka.KafkaUtilsPythonHelper())
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'JavaPackage' object is not callable
```
* [TypeError: 'JavaPackage' object is not callable](https://github.com/JohnSnowLabs/spark-nlp/issues/232)
* self download jar from [link](https://jar-download.com/?search_box=spark-streaming-kafka-0-10-assembly)
* copy jar into dir
```shell
cp spark-streaming-kafka-0-8-assembly_2.11-2.4.1.jar /root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/jars/
```
* new err msg
* 
```shell
>>> directKafkaStream = KafkaUtils.createDirectStream(
...     ssc, [topic], kafka_param)
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/streaming/kafka.py", line 146, in createDirectStream
    ssc._jssc, kafkaParams, set(topics), jfromOffsets)
  File "/root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/python/lib/py4j-0.10.7-src.zip/py4j/java_gateway.py", line 1257, in __call__
  File "/root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/sql/utils.py", line 63, in deco
    return f(*a, **kw)
  File "/root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/python/lib/py4j-0.10.7-src.zip/py4j/protocol.py", line 328, in get_return_value
py4j.protocol.Py4JJavaError: An error occurred while calling o34.createDirectStreamWithoutMessageHandler.
: org.apache.spark.SparkException: java.nio.channels.ClosedChannelException
org.apache.spark.SparkException: Couldn't find leader offsets for Set([firewall,0])
    at org.apache.spark.streaming.kafka.KafkaCluster$$anonfun$checkErrors$1.apply(KafkaCluster.scala:387)
    at org.apache.spark.streaming.kafka.KafkaCluster$$anonfun$checkErrors$1.apply(KafkaCluster.scala:387)
    at scala.util.Either.fold(Either.scala:98)
    at org.apache.spark.streaming.kafka.KafkaCluster$.checkErrors(KafkaCluster.scala:386)
    at org.apache.spark.streaming.kafka.KafkaUtils$.getFromOffsets(KafkaUtils.scala:223)
    at org.apache.spark.streaming.kafka.KafkaUtilsPythonHelper.createDirectStream(KafkaUtils.scala:721)
    at org.apache.spark.streaming.kafka.KafkaUtilsPythonHelper.createDirectStreamWithoutMessageHandler(KafkaUtils.scala:689)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:498)
    at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
    at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
    at py4j.Gateway.invoke(Gateway.java:282)
    at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
    at py4j.commands.CallCommand.execute(CallCommand.java:79)
    at py4j.GatewayConnection.run(GatewayConnection.java:238)
    at java.lang.Thread.run(Thread.java:748)
```


* test w/ file
```
python spark_readfile.py > tmp 2>&1
```

# monitor
* ps -ef | grep spark
```
root     30808 30717  0 08:24 pts/4    00:00:18 /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -cp /root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/conf:/root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/jars/* -Xmx1g org.apache.spark.deploy.SparkSubmit --name PySparkShell pyspark-shell
```

* kafka related
```shell
# enter container
docker exec -it kafka bash

# deprecated
# kafka-console-consumer.sh --zookeeper docker-zookeeper:2181 --topic firewall --from-beginning --max-messages 100

# OK
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic firewall --from-beginning --max-messages 100


```

# reference
* [Spark Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
* [Spark Streaming + Kafka Integration Guide (Kafka broker version 0.8.2.1 or higher)
](https://spark.apache.org/docs/2.4.1/streaming-kafka-0-8-integration.html)
* [Structured Streaming + Kafka Integration Guide (Kafka broker version 0.10.0 or higher)](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
* [pyspark.streaming.kafka.KafkaUtils](https://spark.apache.org/docs/2.4.1/api/python/pyspark.streaming.html#pyspark.streaming.kafka.KafkaUtils)
* [example](https://www.programcreek.com/python/example/98361/pyspark.streaming.kafka.KafkaUtils.createDirectStream)
* [submitting app](https://spark.apache.org/docs/2.1.1/submitting-applications.html#launching-applications-with-spark-submit)

* [RDD methods](https://spark.apache.org/docs/latest/rdd-programming-guide.html#transformations)
* [java.nio.channels.ClosedChannelException
](https://stackoverflow.com/questions/2801087/java-nio-channels-closedchannelexception)
