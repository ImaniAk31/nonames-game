from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models import Card

def get_random_card(db: Session, deck_name: str = "Any"):
    query = db.query(Card).filter(Card.is_active == True)
    
    # Filter by the deck chosen on the TV screen
    if deck_name != "Any":
        query = query.filter(Card.deck == deck_name)
        
    card = query.order_by(func.random()).first()
    
    if card:
        return {
            "id": card.id,
            "title": card.title,
            "category": card.category,
            "forbidden_words": [w.strip() for w in card.forbidden_words_str.split(',')],
            "deck": card.deck,
            "hint": card.hint # --- NEW: Passing the hint to the frontend! ---
        }
    return None