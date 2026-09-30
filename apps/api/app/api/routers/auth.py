from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token, oauth2_scheme, decode_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role_name=user_in.role_name or "Farmer",
        preferred_language=user_in.preferred_language or "en",
        phone_number=user_in.phone_number,
        location_name=user_in.location_name or "Tamil Nadu, India",
        latitude=user_in.latitude,
        longitude=user_in.longitude
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=user.id, role=user.role_name)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role_name": user.role_name,
            "preferred_language": user.preferred_language,
            "location_name": user.location_name
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalars().first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(subject=user.id, role=user.role_name)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role_name": user.role_name,
            "preferred_language": user.preferred_language,
            "location_name": user.location_name
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    if not token:
        # Return demo fallback user if unauthenticated in demo mode
        return {
            "id": "demo-farmer-id",
            "email": "farmer@agridoctor.ai",
            "full_name": "Ramanathan Farmers",
            "role_name": "Farmer",
            "preferred_language": "en",
            "phone_number": "+91 98765 43210",
            "location_name": "Coimbatore, Tamil Nadu",
            "latitude": 11.0168,
            "longitude": 76.9558
        }
    payload = decode_token(token)
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
