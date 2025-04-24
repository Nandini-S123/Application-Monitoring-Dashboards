from confluent_kafka import Producer
import random
import time
import json

producer_conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(producer_conf)

endpoints = ["/users", "/products", "/checkout", "/login", "/orders", "/cart", "/payments", "/reviews", "/profile", "/search"]
statuses = ["success", "error"]
error_types = [None, "404 Not Found", "500 Internal Server Error", "402 Payment Required", "503 Service Unavailable"]
methods = ["GET", "POST", "PUT"]

def simulate_request():
    endpoint = random.choice(endpoints)
    status = random.choice(statuses)
    error_type = random.choice(error_types) if status == "error" else None
    response_time = random.randint(100, 500)
    method = random.choice(methods)
    
    data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "endpoint": endpoint,
        "status": status,
        "response_time": response_time,
        "error_type": error_type,
        "method": method
    }
    
    producer.produce('logs', json.dumps(data).encode('utf-8'))
    producer.flush()
    print(f"Produced log: {data}")

for _ in range(100):  # Increased to 100 requests
    simulate_request()
    time.sleep(random.uniform(0.5, 2))  # Random delay between 0.5-2 seconds