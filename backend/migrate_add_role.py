"""
Migration script to add role column to users table.
Run: python migrate_add_role.py
"""
import asyncio
from app.config.database import AsyncSessionLocal, engine
from sqlalchemy import text


async def migrate():
    """Add role column to users table if it doesn't exist."""
    async with engine.begin() as conn:
        try:
            # Check if column exists
            result = await conn.execute(
                text("""
                    SELECT COUNT(*) as count 
                    FROM information_schema.COLUMNS 
                    WHERE TABLE_SCHEMA = 'skillpath' 
                    AND TABLE_NAME = 'users' 
                    AND COLUMN_NAME = 'role'
                """)
            )
            row = result.fetchone()
            
            if row and row[0] == 0:
                # Column doesn't exist, add it
                print("Adding 'role' column to users table...")
                await conn.execute(
                    text("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user' AFTER password")
                )
                # Update existing users
                await conn.execute(
                    text("UPDATE users SET role = 'user' WHERE role IS NULL OR role = ''")
                )
                await conn.commit()
                print("Migration completed successfully!")
            else:
                print("'role' column already exists. Migration not needed.")
        except Exception as e:
            print(f"Migration error: {e}")
            await conn.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(migrate())

