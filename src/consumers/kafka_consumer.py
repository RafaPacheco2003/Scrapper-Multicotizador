import json
import logging
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaError
from src.core.database import SessionLocal
from src.repositories.quotation_repository import QuotationRepository
from src.services.quotation_service import QuotationService

TOPIC = "quotations-created"
BROKER = "localhost:9092"
GROUP_ID = "fastapi-quotation-group"

logger = logging.getLogger(__name__)


def start_consumer():
    try:
        logger.info(f"Conectando a Kafka en {BROKER}...")

        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=[BROKER],
            group_id=GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )

        logger.info(f"Kafka consumer conectado a {BROKER}")
        logger.info(f"Topic: {TOPIC} | Group: {GROUP_ID}")

        for message in consumer:
            event = message.value
            logger.info(f"Evento recibido: {event}")
            process_event(event)         
    except (NoBrokersAvailable, KafkaError, Exception) as e:
        logger.error(f"Error en Kafka consumer: {str(e)}")


def process_event(event: dict):
    quotation_id= event.get("quotationId")
    
    if quotation_id:
        db = SessionLocal()
        
        repository = QuotationRepository(db)
        service = QuotationService(repository)
        quotation = service.get_quotation_by_id(quotation_id)
        
        if quotation:
            logger.info(f" Cotizacion: ")
            logger.info(f"      - ID: {quotation.quotation_id}")
            logger.info(f"      - Marca: {quotation.branch_name}")
            logger.info(f"      - Modelo: {quotation.model_name}")
            logger.info(f"      - Año: {quotation.year}")
            logger.info(f"      - Descripción: {quotation.description}")
            
        else:
            logger.warning("Cotizacion no encontrada desde la BD")
        
    else:
        logger.warning("No se recibio el id de la cotizacion por el evento de kafka")
