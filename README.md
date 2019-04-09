## Read Me

This assumes you already have docker installed in your environment 

1. run `docker-compose up -d`

2. Wait a couple of minutes and run: 

        docker run --rm --tty --network=container:kafka confluentinc/cp-kafkacat kafkacat -b docker-kafka:9092  -L

3. Output should show that kafka is empty (no topics)

4. Push sample data with the following command:

        docker run --rm --network=container:kafka --volume $(pwd)/data:/data confluentinc/cp-kafkacat kafkacat -b docker-kafka:9092 -t firewall -P -l /data/firewall.json

5. To verify data has been push, run again:

        docker run --rm --tty --network=container:kafka confluentinc/cp-kafkacat kafkacat -b docker-kafka:9092  -L

6. It should show *firewall* topic with 1000 elements. You can run step 4 multiple times if needed

7. (Optional) To take a look at the data (consume), run:

        docker run --rm --tty --network=container:kafka confluentinc/cp-kafkacat kafkacat -b docker-kafka:9092 -C -o 0 -t firewall

8. To clean up, run:

        docker-compose down
        docker volume prune