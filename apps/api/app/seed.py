from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import Role

async def seed_initial_data(db: AsyncSession):
    """Seed system roles if missing. No hardcoded farmer crops or scans."""
    roles = ["Farmer", "Expert", "Admin"]
    for role_name in roles:
        r_check = await db.execute(select(Role).where(Role.name == role_name))
        if not r_check.scalars().first():
            db.add(Role(name=role_name, description=f"{role_name} user role"))

    await db.commit()
