from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate, hashed_password: str) -> User:
        db_user = User(   # 1. Создаем объект-модель для SQLAlchemy
            email=user_data.email,
            hashed_password=hashed_password
        )
        # 2. Добавляем в сессию (черновик)
        db.add(db_user)
        
        # 3. Сохраняем в базу (SQL: COMMIT)
        db.commit()
        
        # 4. Обновляем объект, чтобы получить сгенерированный базой id
        db.refresh(db_user)
        
        # 5. Возвращаем созданного пользователя
        return db_user

    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Ищет пользователя в базе данных по его email."""
        return db.query(User).filter(User.email == email).first()