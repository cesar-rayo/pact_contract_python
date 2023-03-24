from pact import Broker

# pact_broker_url = 'http://localhost:9292'
# pact_broker_token = 'your-pact-broker-token'
# pact_broker_version = '1.0.0'
# pact_files = ['path/to/pact/file.json']
# Broker(broker_token="")

broker = Broker(broker_base_url="http://localhost:9292")
broker.publish(
    consumer_name="shopping-cart-service",
    version="2.0",
    pact_dir="./contracts",
    branch="development",
    consumer_tags=["development", "test"]
)
