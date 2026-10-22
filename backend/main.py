from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware # <-- NEW IMPORT
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

# --- NEW: ALLOW CROSS-ORIGIN REQUESTS (CORS) ---
# This lets your Vercel frontend safely talk to your Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        # Maps room_code -> {player_name: WebSocket}
        self.active_rooms: Dict[str, Dict[str, WebSocket]] = {}
        self.room_state: Dict[str, dict] = {} 
        self.turn_info: Dict[str, dict] = {} 

    async def connect(self, websocket: WebSocket, room_code: str, player_name: str):
        await websocket.accept()
        if room_code not in self.active_rooms:
            self.active_rooms[room_code] = {}
        self.active_rooms[room_code][player_name] = websocket

    def disconnect(self, room_code: str, player_name: str):
        if room_code in self.active_rooms and player_name in self.active_rooms[room_code]:
            del self.active_rooms[room_code][player_name]
            if not self.active_rooms[room_code]:
                del self.active_rooms[room_code]
                self.room_state.pop(room_code, None)
                self.turn_info.pop(room_code, None)

    async def broadcast_to_room(self, message: dict, room_code: str):
        if room_code in self.active_rooms:
            for connection in list(self.active_rooms[room_code].values()):
                try:
                    await connection.send_json(message)
                except Exception:
                    pass
                    
    async def send_personal(self, message: dict, room_code: str, player_name: str):
        if room_code in self.active_rooms and player_name in self.active_rooms[room_code]:
            try:
                await self.active_rooms[room_code][player_name].send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# --- NEW: PEEK AT AVAILABLE AVATARS ENDPOINT ---
@app.get("/api/avatars/{room_code}")
async def get_taken_avatars(room_code: str):
    room_code = room_code.upper()
    avatar_key = f"{room_code}_avatars"
    taken = []
    if avatar_key in manager.room_state:
        taken = list(manager.room_state[avatar_key].values())
    return {"taken": taken}

@app.get("/")
async def root():
    return {"message": "Server is running. I'm not gonna say no names, but it's looking good!"}

@app.websocket("/ws/{room_code}/{player_name}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, player_name: str):
    await manager.connect(websocket, room_code, player_name)
    
    join_msg = {"type": "system", "message": f"{player_name} has joined the room."}
    await manager.broadcast_to_room(join_msg, room_code)
    
    turn_data = manager.turn_info.get(room_code)
    if turn_data:
        await manager.send_personal({
            "type": "turn_started",
            "actor": turn_data["actor"],
            "card": turn_data["card"],
            "action_type": turn_data["action_type"]
        }, room_code, player_name)
        
        if turn_data.get("status") == "active":
            await manager.send_personal({"type": "actor_ready"}, room_code, player_name)
    
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            
            if parsed_data.get("action") == "set_avatar":
                chosen_avatar = parsed_data.get("avatar", "👤")
                
                avatar_key = f"{room_code}_avatars"
                if avatar_key not in manager.room_state:
                    manager.room_state[avatar_key] = {}
                    
                taken = [av for p, av in manager.room_state[avatar_key].items() if p != player_name]
                
                if chosen_avatar in taken:
                    all_avs = ['😎', '🤠', '👽', '👻', '🤖', '👑', '🔥', '💎']
                    avail = [a for a in all_avs if a not in taken]
                    chosen_avatar = avail[0] if avail else "👤"
                    
                manager.room_state[avatar_key][player_name] = chosen_avatar
                
                await manager.send_personal({"type": "avatar_assigned", "avatar": chosen_avatar}, room_code, player_name)
                
                await manager.broadcast_to_room({
                    "type": "player_joined",
                    "name": player_name,
                    "avatar": chosen_avatar
                }, room_code)

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
                            
                            manager.turn_info[room_code] = {
                                "actor": actor_name,
                                "card": card_data,
                                "action_type": action_type,
                                "status": "prep"
                            }
                            
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
                if room_code in manager.turn_info:
                    manager.turn_info[room_code]["status"] = "active"
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
                manager.turn_info.pop(room_code, None) 
                await manager.broadcast_to_room({"type": "round_over"}, room_code)
                
    except WebSocketDisconnect:
        manager.disconnect(room_code, player_name)
        leave_msg = {"type": "system", "message": f"{player_name} has left."}
        await manager.broadcast_to_room(leave_msg, room_code)