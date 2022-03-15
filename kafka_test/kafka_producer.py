"""
a simple producer , using the code in  https://github.com/dpkp/kafka-python

NOTE: use
pip install kafka-python
and not
pip install kafka

For one shot operations, consider using kafka_cat  https://docs.confluent.io/platform/current/app-development/kafkacat-usage.html
or kafka_-console-producer

kafkacat -b localhost:9093 -t <my_topic>  -P -l test_file.jsonl

To list metadata:
kafkacat -b localhost:9093 -L

WARNING:
    I found out that using the docker on my machine, I could connect to port 9093 (and if there are multiple brokers also 9094 9095)
    I don't know why I can connect to 9092 on the Azure installation(and getting produce errors!), but when changing
    the Azure connection to 9093 it worked fine!

"""
from kafka import KafkaProducer
import json, os
import argparse
import logging
kafka_server = 'dds2020s-kafka.eastus.cloudapp.azure.com:9093'
#kafka_server = 'localhost:9093'
def json_producer(file_path, current_topic):
    producer = KafkaProducer(bootstrap_servers=kafka_server,
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    with open(file_path, 'r') as data:
        i = 0
        futures = []
        for row in data:
            try:
                row_dict = json.loads(row)
                i += 1
                future = producer.send(current_topic, row_dict)
                futures.append(future)
            except Exception as e:
                logging.error(f"Failed to send row \n {row} \n Error: {e}")

        # wait for all the send() to complete
        for f in futures:
            print(str(f.get()))

        producer.flush()
        producer.close()


def topic_from_filename(filename: str):
    name, _ = filename.split('.')
    year, month, day = name.split('_', 1)[1].split('_', 3)
    return f"{day}-{month}-{year}"


def create_topic_by_files(files_path: str) -> dict:
    topic_dict = {}
    for subdir, dirs, files in os.walk(files_path):
        for file in files:
            topic = topic_from_filename(file)
            topic_dict[topic] = topic_dict.get(topic, []) \
                                + [os.path.join(files_path, file)]
    return topic_dict


def mini_test():
    """ send a few lines to a test topic"""
    json_producer('t3.jsonl', 'test_topic5')

if __name__ == "__main__":
    # Parsing script arguments
    mini_test()
    exit(0)

    parser = argparse.ArgumentParser(description='Process input')
    parser.add_argument('files_path', type=str, help='files directory')
    args = parser.parse_args()

    logging.basicConfig(filename='producer.log',
                        filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s : %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

    topic_dict = create_topic_by_files(args.files_path)

    for topic, files in topic_dict.items():
        for file in files:
            print(f"Topic: {topic}, File: {file}")
            try:
                json_producer(file, topic)
            except Exception as e:
                logging.error(f"Failed to produce \n {topic} \n Error: {e}")