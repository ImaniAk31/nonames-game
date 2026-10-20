from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import random
from thefuzz import fuzz

from database import SessionLocal
import crud
from seed import seed_database

# Auto-seed the database on startup!
seed_database()

app = FastAPI(title="I'm Not Gonna Say No Names API")

class ConnectionManager:
    def __init__(self):
        self.active_rooms: Dict[str, List[WebSocket]] = {}
        self.room_state: Dict[str, dict] = {} 

    async def connect(self, websocket: WebSocket, room_code: str):
        await websocket.accept()
        if room_code not in self.active_rooms:
            self.active_rooms[room_code] = []
        self.active_rooms[room_code].append(websocket)

    def disconnect(self, websocket: WebSocket, room_code: str):
        if room_code in self.active_rooms:
            self.active_rooms[room_code].remove(websocket)
            if not self.active_rooms[room_code]:
                del self.active_rooms[room_code]
                if room_code in self.room_state:
                    del self.room_state[room_code]

    async def broadcast_to_room(self, message: dict, room_code: str):
        if room_code in self.active_rooms:
            for connection in self.active_rooms[room_code]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Server is running. I'm not gonna say no names, but it's looking good!"}

@app.websocket("/ws/{room_code}/{player_name}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, player_name: str):
    await manager.connect(websocket, room_code)
    
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            
            # --- NEW: CATCH THE AVATAR AND BROADCAST TO TV ---
            if parsed_data.get("action") == "set_avatar":
                chosen_avatar = parsed_data.get("avatar", "👤")
                await manager.broadcast_to_room({
                    "type": "player_joined",
                    "name": player_name,
                    "avatar": chosen_avatar
                }, room_code)

            # --- START GAME LOGIC ---
            elif parsed_data.get("action") == "start_game":
                players_list = parsed_data.get("players", [])
                if players_list:
                    actor_name = random.choice(players_list)
                    db = SessionLocal()
                    try:
                        card_data = crud.get_random_card(db)
                        if card_data:
                            manager.room_state[room_code] = card_data
                            
                            act_out_categories = [
                                "Viral Moment", "Viral Legend", "Hip-Hop Moment", 
                                "Award Show Chaos", "Iconic Music Video", "Viral Dance"
                            ]
                            
                            if card_data["category"] in act_out_categories:
                                action_type = "ACT IT OUT!"
                            else:
                                action_type = "TELL A STORY!"
                            
                            turn_msg = {
                                "type": "turn_started",
                                "actor": actor_name,
                                "card": card_data,
                                "action_type": action_type
                            }
                            await manager.broadcast_to_room(turn_msg, room_code)
                    finally:
                        db.close()

            elif parsed_data.get("action") == "actor_ready":
                await manager.broadcast_to_room({"type": "actor_ready"}, room_code)

            elif parsed_data.get("action") == "submit_guess":
                guess = parsed_data.get("guess", "")
                player_guessing = parsed_data.get("player", "")
                active_card = manager.room_state.get(room_code)
                
                if active_card:
                    correct_title = active_card["title"].lower()
                    match_score = fuzz.ratio(correct_title, guess.lower())
                    
                    if match_score > 85:
                        success_msg = {
                            "type": "correct_guess",
                            "player": player_guessing
                        }
                        await manager.broadcast_to_room(success_msg, room_code)
                        
            elif parsed_data.get("action") == "end_round":
                await manager.broadcast_to_room({"type": "round_over"}, room_code)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_code)
        leave_msg = {"type": "system", "message": f"{player_name} has left."}
        await manager.broadcast_to_room(leave_msg, room_code)