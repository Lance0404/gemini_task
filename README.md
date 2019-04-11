### Milestones
1. kafka and zookeeper finely installed with REAME_gemini.md (O)
2. firewall.json finely imported into kafka (O)
3. data exists in kafka confirmed (O)
4. pyspark installed with pipenv (O)
5. manually added a missing jar file into the pyspark env (O)
6. trying to consume kafka with pyspark (O)
7. convert Dstream to dataframe (O)
8. do sql query on dataframe (O)
9. output dataframe to parquet file (O) 

### Execute
* execute cmd under project dir
```shell
cd <prject dir>
pipenv shell
spark-submit --jars /root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/jars/spark-streaming-kafka-0-8-assembly_2.11-2.4.1.jar ps_consumer.py > ps_consumer.err 2>&1

ls data/firewall.parquet
```



