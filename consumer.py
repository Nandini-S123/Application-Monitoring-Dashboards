from confluent_kafka import Consumer, KafkaError
import mysql.connector
from datetime import datetime
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'log-consumer-group',
    'auto.offset.reset': 'earliest'
}

def connect_to_kafka():
    max_retries = 10
    for i in range(max_retries):
        try:
            consumer = Consumer(conf)
            consumer.subscribe(['logs'])  # Standardized topic name
            logger.info("Connected to Kafka successfully")
            return consumer
        except Exception as e:
            logger.error(f"Failed to connect to Kafka ({i+1}/{max_retries}): {e}")
            time.sleep(5)
    raise Exception("Could not connect to Kafka after retries")

def connect_to_db():
    max_retries = 5
    for i in range(max_retries):
        try:
            db = mysql.connector.connect(
                host="mysql",
                user="root",
                password="Nandini@2004",
                database="CC_MINIPROJECT"
            )
            logger.info("Connected to MySQL successfully")
            return db
        except Exception as e:
            logger.error(f"Failed to connect to MySQL ({i+1}/{max_retries}): {e}")
            time.sleep(5)
    raise Exception("Could not connect to MySQL after retries")

consumer = connect_to_kafka()

def process_log(message):
    db = None
    cursor = None
    try:
        log_data = json.loads(message.value().decode('utf-8'))
        timestamp = datetime.now()
        endpoint = log_data.get('endpoint', 'unknown')[:255]
        status = log_data.get('status', 'unknown')[:50]
        response_time = min(max(int(log_data.get('response_time', 0)), 0), 999999)
        error_type = log_data.get('error_type')[:255] if log_data.get('error_type') else None

        db = connect_to_db()
        cursor = db.cursor()

        insert_query = """
        INSERT INTO logs (timestamp, endpoint, status, response_time, error_type)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (timestamp, endpoint, status, response_time, error_type))
        db.commit()
        logger.info(f"Processed log: {log_data}")
    except ValueError as e:
        logger.error(f"Invalid data format: {e}")
    except Exception as e:
        logger.error(f"Error processing log: {e}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logger.info(f"End of partition reached {msg.topic()} [{msg.partition}] at offset {msg.offset()}")
            else:
                logger.error(f"Kafka error: {msg.error()}")
        else:
            process_log(msg)
except KeyboardInterrupt:
    logger.info("Consumer interrupted.")
finally:
    consumer.close()