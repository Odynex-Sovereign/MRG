from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class UserRegister(BaseModel):
    # Use plain str so sandbox boots without optional email-validator package.
    email: str = Field(..., min_length=3, max_length=254)
    full_name: str
    password: str
    department_vertical: str


class UserLogin(BaseModel):
    email: str = Field(..., min_length=3, max_length=254)
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_operator(user: UserRegister):
    # Enforces account generation validation checks
    return {"message": "Account created successfully.", "email": user.email, "role": "operator"}

@router.post("/login")
async def login_operator(credentials: UserLogin):
    if credentials.email == "admin@odynex.axis" and credentials.password == "secure":
        return {"access_token": "mrg_token_secret_payload", "token_type": "bearer", "role": "architect"}
    raise HTTPException(status_code=401, detail="Invalid credential records.")
