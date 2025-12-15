"""Service for user management."""

from typing import Optional
from sqlalchemy.orm import Session

from ..models import User, WorkoutLog


class UserService:
    """Service for user operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str) -> User:
        """Create a new user."""
        user = User(username=username)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_or_create_user(self, username: str) -> User:
        """Get existing user or create new one."""
        user = self.get_user_by_username(username)
        if not user:
            user = self.create_user(username)
        return user

    def get_workout_history(
        self,
        user_id: int,
        chain_id: Optional[str] = None,
        limit: int = 50
    ) -> list[WorkoutLog]:
        """Get user's workout history."""
        query = self.db.query(WorkoutLog).filter(WorkoutLog.user_id == user_id)

        if chain_id:
            query = query.filter(WorkoutLog.chain_id == chain_id)

        return query.order_by(WorkoutLog.created_at.desc()).limit(limit).all()
