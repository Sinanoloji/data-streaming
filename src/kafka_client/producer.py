from kafka import KafkaProducer
import json
import requests

def create_response_dict(url: str="https://randomuser.me/api/?results=1") -> dict:

    response = requests.get(url)
    data = response.json()
    results = data["results"][0]

    return results


def create_final_json(results: dict) -> dict:
    kafka_data = {}

    kafka_data["full_name"] = f"{results['name']['title']}. {results['name']['first']} {results['name']['last']}"
    kafka_data["gender"] = results["gender"]
    kafka_data["location"] = f"{results['location']['street']['number']}, {results['location']['street']['name']}"
    kafka_data["city"] = results['location']['city']
    kafka_data["country"] = results['location']['country']
    kafka_data["postcode"] = int(results['location']['postcode'])
    kafka_data["latitude"] = float(results['location']['coordinates']['latitude'])
    kafka_data["longitude"] = float(results['location']['coordinates']['longitude'])
    kafka_data["email"] = results["email"]

    return kafka_data

def produce_to_kafka():
    
    results = create_response_dict()
    data = create_final_json(results)

    producer = KafkaProducer(bootstrap_servers=['localhost:9094'])
    
    producer.send("mytopic",value=json.dumps(data).encode("utf8"))
    producer.flush()

if __name__ == "__main__":
    produce_to_kafka()