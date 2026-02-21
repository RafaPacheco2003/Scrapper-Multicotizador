from psycopg2 import Date


class QuotationCreatedEvent:
    quotation_id: str
    occurredAt: Date
