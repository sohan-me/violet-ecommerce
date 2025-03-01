import uuid

def generate_order_number():
    return uuid.uuid4().hex[:10].upper()