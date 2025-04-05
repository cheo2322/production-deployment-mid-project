from kafka import KafkaConsumer
from prometheus_client import Counter, Histogram, start_http_server

# Update the Kafka topic to the movie log of your team
topic = 'recommendations'

start_http_server(8765)

# Metrics like Counter, Gauge, Histogram, Summaries
# Refer https://prometheus.io/docs/concepts/metric_types/ for details of each metric
# Define metrics to show request count. Request count is total number of requests made with a particular http status
REQUEST_COUNT = Counter(
    'request_count', 'Recommendation Request Count',
    ['http_status']
)

REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')


def main():
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id=topic,
        enable_auto_commit=True,
        auto_commit_interval_ms=1000
    )

    for message in consumer:
        try:
            event = message.value.decode('utf-8')
            values = event.split(',')
            if len(values) < 3:
                print(f"Not valid message: {event}")
                continue

            if 'rr' in values[2]:
                # Increment the request count metric for the appropiate HTTP status code.
                status = values[3].strip() if len(values) > 3 else 'unknown'
                REQUEST_COUNT.labels(http_status=status).inc()

                # Updating request latency histogram
                time_taken = float(values[-1].strip().split(" ")[0]) if len(values) > 4 else 0
                REQUEST_LATENCY.observe(time_taken / 1000)

                print(f"Processing: {values}")
        except Exception as e:
            print(f"Error procesando el mensaje: {e}")

if __name__ == "__main__":
    main()
