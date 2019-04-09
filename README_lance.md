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
