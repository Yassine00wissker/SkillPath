"""
Seed script to populate the database with sample data.
Run: python seed_db.py
"""
import asyncio
import sys
from app.config.database import AsyncSessionLocal, engine, Base
from app.models import User, Admin, Category, Formation, Parcours
from app.core.security import get_password_hash


async def seed_database():
    """Seed the database with sample data."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        try:
            # Create categories
            categories_data = [
                {"nom": "Développement Web"},
                {"nom": "Développement Mobile"},
                {"nom": "Data Science"},
                {"nom": "Cybersécurité"},
                {"nom": "Design"},
            ]

            categories = []
            for cat_data in categories_data:
                category = Category(**cat_data)
                session.add(category)
                categories.append(category)

            await session.flush()

            # Create formations
            formations_data = [
                {
                    "titre": "Introduction à Python",
                    "description": "Apprenez les bases de Python",
                    "video": "https://example.com/python-intro.mp4",
                    "category_id": categories[0].id,
                },
                {
                    "titre": "FastAPI : Créer des APIs Modernes",
                    "description": "Maîtrisez FastAPI pour créer des APIs RESTful",
                    "video": "https://example.com/fastapi-tutorial.mp4",
                    "category_id": categories[0].id,
                },
                {
                    "titre": "React : Développement Frontend",
                    "description": "Découvrez React pour créer des interfaces",
                    "video": "https://example.com/react-course.mp4",
                    "category_id": categories[0].id,
                },
                {
                    "titre": "Data Science avec Python",
                    "description": "Analysez des données avec pandas et numpy",
                    "video": "https://example.com/data-science.mp4",
                    "category_id": categories[2].id,
                },
                {
                    "titre": "Sécurité Web : OWASP Top 10",
                    "description": "Comprenez les vulnérabilités web",
                    "video": "https://example.com/owasp-security.mp4",
                    "category_id": categories[3].id,
                },
            ]

            formations = []
            for form_data in formations_data:
                formation = Formation(**form_data)
                session.add(formation)
                formations.append(formation)

            await session.flush()

            # Create parcours
            parcours_data = [
                {
                    "titre": "Développeur Full Stack Python",
                    "description": "Parcours complet pour devenir développeur full stack",
                    "listedeformations": [formations[0].id, formations[1].id, formations[2].id],
                },
                {
                    "titre": "Data Scientist",
                    "description": "Formation complète en data science",
                    "listedeformations": [formations[3].id],
                },
            ]

            for parc_data in parcours_data:
                parcours = Parcours(**parc_data)
                session.add(parcours)

            # Create sample users
            users_data = [
                {
                    "nom": "Martin",
                    "prenom": "Sophie",
                    "email": "sophie.martin@email.com",
                    "competence": ["python", "fastapi", "sql"],
                    "interests": ["web development", "backend"],
                    "password": get_password_hash("password123"),
                    "role": "user",
                },
                {
                    "nom": "Bernard",
                    "prenom": "Pierre",
                    "email": "pierre.bernard@email.com",
                    "competence": ["javascript", "react"],
                    "interests": ["frontend", "ui/ux"],
                    "password": get_password_hash("password123"),
                    "role": "content_creator",  # Content creator can manage formations
                },
            ]

            for user_data in users_data:
                user = User(
                    nom=user_data["nom"],
                    prenom=user_data["prenom"],
                    email=user_data["email"],
                    competence=user_data["competence"],
                    interests=user_data["interests"],
                    password=user_data["password"],
                    role=user_data.get("role", "user")
                )
                session.add(user)

            # Create admin
            admin = Admin(
                nom="Admin",
                prenom="System",
                email="admin@skillpath.com",
                password=get_password_hash("admin123"),
            )
            session.add(admin)

            await session.commit()
            print("✅ Database seeded successfully!")
            print("\nSample credentials:")
            print("  User: sophie.martin@email.com / password123")
            print("  Content Creator: pierre.bernard@email.com / password123")
            print("  Admin: admin@skillpath.com / admin123")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding database: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_database())

