from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from mrg.core.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing user handle.")
    return {"access_token": create_access_token(data={"sub": form_data.username}), "token_type": "bearer"}
