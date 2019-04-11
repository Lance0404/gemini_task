#!/bin/bash
rm -rf data/firewall.parquet
spark-submit --jars /root/.local/share/virtualenvs/gemini_task-p6OkMWYi/lib/python3.7/site-packages/pyspark/jars/spark-streaming-kafka-0-8-assembly_2.11-2.4.1.jar ps_consumer.py
