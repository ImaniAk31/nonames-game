import random
from typing import List, Dict
from pydantic import BaseModel
from thefuzz import fuzz

class Player(BaseModel):
    id: int
    nickname: str
    score: int = 0

class GameRoom:
    def __init__(self, room_code: str):
        self.room_code = room_code
        self.players: Dict[int, Player] = {}
        self.turn_queue: List[int] = []
        
        self.active_actor_id: int = None
        self.current_card: dict = None
        self.current_turn_answers: Dict[int, str] = {}
        self.correct_guessers: List[int] = []

    def add_player(self, player_id: int, nickname: str):
        self.players[player_id] = Player(id=player_id, nickname=nickname)

    def start_new_round(self):
        self.turn_queue = list(self.players.keys())
        random.shuffle(self.turn_queue)

    def next_turn(self, new_card: dict) -> dict:
        if not self.turn_queue:
            return {"status": "round_over"}

        self.active_actor_id = self.turn_queue.pop(0)
        self.current_card = new_card
        self.current_turn_answers = {}
        self.correct_guessers = []

        return {
            "status": "turn_started",
            "actor_id": self.active_actor_id,
            "card": self.current_card
        }

    def process_guess(self, player_id: int, guess: str) -> dict:
        if player_id == self.active_actor_id:
            return {"error": "The actor cannot guess!"}

        self.current_turn_answers[player_id] = guess
        
        correct_title = self.current_card["title"].lower()
        match_score = fuzz.ratio(correct_title, guess.lower())
        is_correct = match_score > 85 

        if is_correct and player_id not in self.correct_guessers:
            self.correct_guessers.append(player_id)
            self.players[player_id].score += 5 

        total_guessers = len(self.players) - 1
        all_answers_in = len(self.current_turn_answers) >= total_guessers

        return {
            "is_correct": is_correct,
            "all_answers_in": all_answers_in,
            "match_score": match_score 
        }