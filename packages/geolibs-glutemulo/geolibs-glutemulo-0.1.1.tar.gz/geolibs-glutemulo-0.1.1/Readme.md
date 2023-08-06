# Glutemulo

A HA geo socio demo data ingestor

## Usage

Read de [examples files](examples).

We use environ vars. See [Environ vars file example](.env.example) for complete list,
and examples.

### Using producer to upload data to kafka

See python examples bellow. You must produce a dict with column_mame:value

### Using the ingestor consumer
Use `gluto` docker and fill enviroment vars.

Select the backend using `GLUTEMULO_BACKEND` and specific vars for it (database, host, etc).
You can select 2 backends: `postgres` or `carto`
See [Environ vars file example](.env.example) for complete list.

Then set:

1. `GLUTEMULO_INGESTOR_DATASET`  
Table to upload data
2. `GLUTEMULO_INGESTOR_DATASET_COLUMNS`  
Comma separted list of column names

Now, create the table on backend or set `GLUTEMULO_INGESTOR_DATASET_DDL` and `GLUTEMULO_INGESTOR_DATASET_AUTOCREATE=False`

Then configure ingestor for kafka.
First read the [python-kafka doc](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html)
and then use the following vars:

1. `GLUTEMULO_INGESTOR_TOPIC`  
Topic to use
2. `GLUTEMULO_INGESTOR_BOOTSTRAP_SERVERS`  
List of servers to connect
3. `GLUTEMULO_INGESTOR_GROUP_ID`  
Group id.
4. `GLUTEMULO_INGESTOR_AUTO_OFFSET_RESET`  
latest or earliest.
5. `GLUTEMULO_INGESTOR_MAX_POLL_RECORDS`  
The maximum number of records returned in a batch of messages
6. `GLUTEMULO_INGESTOR_FETCH_MIN_BYTES`  
Minimum amount of data the server should return for a fetch request, otherwise wait up to fetch_max_wait_ms for more data to accumulate. Default: 1

For the docker, we include a [example docker-compose file](docker-compose.yml).
Remember you can scale with same group_id

```bash
docker-compose scale gluto=3
```

## Run flask demo

```bash
$ FLASK_ENV=development flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 194-409-049
```

## Test

```bash
$ http -j POST localhost:5000/v1/ uno=1 dos=2`
HTTP/1.0 201 CREATED
Content-Length: 13
Content-Type: text/html; charset=utf-8
Date: Thu, 02 May 2019 14:56:07 GMT
Server: Werkzeug/0.15.2 Python/3.7.2

DATA Received
```

## Producer / Consumer

### Kafka + json

Async producer:

```python
from glutemulo.kafka.producer import JsonKafka
productor = JsonKafka(bootstrap_servers="localhost:9092")
future = productor.produce('simple-topic', dict(dos='BB'))
```

Consumer in batches:
```python
from glutemulo.kafka.consumer import JsonKafka
consumer = JsonKafka('simple-topic', bootstrap_servers="localhost:9092")
for msg in consumer.consume():
    for msg in messages:
        print(msg)
```

### Kafka + Avro

sync producer:

```python
SCHEMA = {
    "type": "record",
    "name": "simpledata",
    "doc": "This is a sample Avro schema to get you started.",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "number1", "type": "int"},
    ],
}
SCHEMA_ID = 1
```

```python
from glutemulo.kafka.producer import AvroKafka as Producer
productor = Producer(SCHEMA, SCHEMA_ID,bootstrap_servers="localhost:9092")
future = productor.produce('simple-topic-avro', dict(name='Un nombre', number1=10))
```

Consumer:
```python
from glutemulo.kafka.consumer import AvroKafka as Consumer
consumer = Consumer('simple-topic-avro', SCHEMA, SCHEMA_ID, bootstrap_servers="localhost:9092")
for messages in consumer.consume():
    for msg in messages:
        print(msg)
```

## For testing

You can setup a Kafka Consumer using the kafka-console-consumer script that comes with Kafka.

```bash
$ bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.240:9092 --topic pylog --from-beginning

this is an awsome log
```

### Testing With KafkaCat

You ca use an application called KafkaCat.

After the application is installed we will run it in consumer mode (which is the default).

```bash
kafkacat -b 192.168.240.41:9092 -t one-test
```

This should not show anything yet because we haven't sent anything to our topic yet...

To send stuff we can copy any text file into our current directory and send it to our Kafka Topic. In another window, run the following command.

```bash
$ cat README | kafkacat -b 192.168.240.41 -t one-test
```
You should see the output in the first window which has KafkaCat still running in consumer mode.


## Links

- [Zoonavigator](http://localhost:8004). Use 'zoo1' as connection string
- [schema-registry-ui](http://localhost:8001)
- [Rebrow](http://localhost:5001)
- [kafka topics ui](http://localhost:8000)
- [kafka rest proxy](http://localhost:8082)
