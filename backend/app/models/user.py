"""User and progress tracking models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from ..db.database import Base


class User(Base):
    """User account."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    progressions = relationship("UserProgression", back_populates="user")
    workout_logs = relationship("WorkoutLog", back_populates="user")


class UserProgression(Base):
    """User's progress in a specific progression chain."""

    __tablename__ = "user_progressions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chain_id = Column(String(50), ForeignKey("progression_chains.id"), nullable=False)

    current_exercise_order = Column(Integer, default=0)
    best_reps = Column(Integer, default=0)
    best_sets = Column(Integer, default=0)
    total_workouts_at_level = Column(Integer, default=0)

    # Progression criteria
    reps_to_progress = Column(Integer, default=12)
    sets_to_progress = Column(Integer, default=3)

    started_at = Column(DateTime, default=datetime.utcnow)
    last_workout_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="progressions")
    chain = relationship("ProgressionChain")

    @property
    def can_progress(self) -> bool:
        """Check if user can progress to next exercise."""
        return self.best_reps >= self.reps_to_progress and self.best_sets >= self.sets_to_progress


class WorkoutLog(Base):
    """Log of individual workout sessions."""

    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(String(50), ForeignKey("exercises.id"), nullable=False)
    chain_id = Column(String(50), ForeignKey("progression_chains.id"), nullable=False)

    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    notes = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workout_logs")
    exercise = relationship("Exercise")
