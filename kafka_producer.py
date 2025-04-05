from kafka import KafkaProducer

# Configurar el productor de Kafka apuntando al broker
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Envía un mensaje al tema "movielogN"
topic = 'recommendations'
message = b'1,1,rr, 200, 0.123456789'
producer.send(topic, value=message)

# Cierra el productor
producer.close()

print(f"Mensaje enviado al tema '{topic}': {message.decode('utf-8')}")