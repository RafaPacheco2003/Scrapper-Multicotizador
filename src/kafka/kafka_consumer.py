import json
import logging
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaError

TOPIC = "quotations-created"
BROKER = "localhost:9092"
GROUP_ID = "fastapi-quotation-group"

logger = logging.getLogger(__name__)

def start_consumer():
    retry_count = 0
    max_retries = 5
    retry_delay = 5
    
    while retry_count < max_retries:
        try:
            logger.info(f"Conectando a Kafka en {BROKER}...")
            
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=[BROKER],
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id=GROUP_ID,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                api_version=(2, 5)
            )
            
            logger.info(f"✅ Kafka consumer conectado a {BROKER}")
            logger.info(f"📡 Topic: {TOPIC} | Group: {GROUP_ID}")
            
            for message in consumer:
                event = message.value
                logger.info(f"🔥 EVENTO desde {message.topic} [Partition {message.partition} | Offset {message.offset}]")
                logger.info(f"   {event}")
                
        except NoBrokersAvailable:
            retry_count += 1
            if retry_count < max_retries:
                logger.warning(f"⚠️  Kafka no disponible. Reintento {retry_count}/{max_retries} en {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                logger.error(f"❌ No se pudo conectar después de {max_retries} intentos")
                break
                
        except KafkaError as e:
            logger.error(f"❌ Error Kafka: {str(e)}")
            break
                
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}")
            break
