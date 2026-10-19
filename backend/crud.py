from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
import models

def get_random_card(db: Session, category_name: str = None) -> dict:
    query = db.query(models.Card).filter(models.Card.is_active == True)
    
    if category_name:
        query = query.filter(models.Card.category == category_name)
        
    random_card = query.order_by(func.random()).first()
    
    if not random_card:
        return None

    return {
        "id": random_card.id,
        "title": random_card.title,
        "category": random_card.category,
        "forbidden_words": random_card.forbidden_words
    }