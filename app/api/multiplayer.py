from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from services.multiplayer_auth import MultiplayerSessionManager

router = APIRouter(prefix="/api/multiplayer", tags=["Multiplayer Engine"])

class CreateLobbyRequest(BaseModel):
    owner_id: str
    is_public: bool

class JoinLobbyRequest(BaseModel):
    guest_id: str
    room_pin: str
    room_id: str

def get_multiplayer_manager() -> MultiplayerSessionManager:
    from app import db_client
    return MultiplayerSessionManager(db_client=db_client)

@router.post("/create-lobby")
async def create_shared_sandbox(
    payload: CreateLobbyRequest,
    manager: MultiplayerSessionManager = Depends(get_multiplayer_manager)
):
    return await manager.provision_coop_lobby(owner_id=payload.owner_id, public=payload.is_public)

@router.post("/join-lobby")
async def join_shared_sandbox(
    payload: JoinLobbyRequest,
    manager: MultiplayerSessionManager = Depends(get_multiplayer_manager)
):
    authorized = await manager.authorize_guest_entry(
        guest_id=payload.guest_id,
        input_pin=payload.room_pin,
        target_room_id=payload.room_id
    )
    if authorized:
        return {"status": "authenticated", "route": f"/ws/simulation/coop?room={payload.room_id}"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session code or lobby is full.")
