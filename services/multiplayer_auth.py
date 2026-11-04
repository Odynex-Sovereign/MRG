import uuid
import secrets
import logging
from typing import Dict, Any, List
from pydantic import BaseModel

logger = logging.getLogger("mrg.services.multiplayer_auth")

class ActiveInstanceSession(BaseModel):
    session_id: str
    owner_id: str
    join_pin: str
    authorized_guests: List[str]
    is_public_lobby: bool
    max_players: int

class MultiplayerSessionManager:
    """
    Roblox-Style Mesh Layer: Controls secure, high-concurrency 
    multi-user authorization bounds for live collaborative simulations.
    """
    def __init__(self, db_client):
        self.db = db_client
        # In-memory rapid lookup registry for active session allocations
        self.active_rooms: Dict[str, ActiveInstanceSession] = {}

    async def provision_coop_lobby(self, owner_id: str, public: bool = False) -> Dict[str, Any]:
        """Spawns a unique session space and pins a numeric token required for guests to hop in."""
        session_id = f"room_{uuid.uuid4().hex[:8]}"
        numeric_join_pin = "".join(secrets.choice("0123456789") for _ in range(6))
        
        new_room = ActiveInstanceSession(
            session_id=session_id,
            owner_id=owner_id,
            join_pin=numeric_join_pin,
            authorized_guests=[],
            is_public_lobby=public,
            max_players=8 # Standard canvas constraint threshold
        )
        
        self.active_rooms[session_id] = new_room
        
        # Log active session lobby index into postgres cluster pool
        await self.db.execute(
            "INSERT INTO growth_loops (id, referrer_id, conversion_value, payout_settled) "
            "VALUES ($1, $2, 0, False)", session_id, owner_id
        )
        
        return {
            "session_id": session_id,
            "join_pin": numeric_join_pin,
            "websocket_endpoint": f"/ws/simulation/coop?room={session_id}"
        }

    async def authorize_guest_entry(self, guest_id: str, input_pin: str, target_room_id: str) -> bool:
        """Validates entry nonces. Deflects griefers and checks player caps before connecting web sockets."""
        room = self.active_rooms.get(target_room_id)
        if not room:
            logger.warning(f"[Multiplayer Denied] Target room {target_room_id} does not exist.")
            return False
            
        if room.join_pin != input_pin:
            logger.warning(f"[Multiplayer Denied] Invalid PIN submission for room {target_room_id}.")
            return False
            
        if len(room.authorized_guests) >= room.max_players:
            logger.warning(f"[Multiplayer Denied] Target room {target_room_id} has reached player capacity.")
            return False

        if guest_id not in room.authorized_guests:
            room.authorized_guests.append(guest_id)
            
        logger.info(f"[Multiplayer Join] Guest {guest_id} successfully connected into room {target_room_id}.")
        return True
