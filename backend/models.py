from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String)
    forbidden_words_str = Column(String)
    difficulty_level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    deck = Column(String, default="For The Culture") 
    # --- NEW: The hint to help the actor! ---
    hint = Column(String, nullable=True)