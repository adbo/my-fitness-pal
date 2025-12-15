"""Pydantic schemas for users and progress tracking."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from .exercise import ExerciseSchema


class UserCreateSchema(BaseModel):
    """Schema for creating a user."""
    username: str


class UserSchema(BaseModel):
    """Schema for user data."""
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserProgressionSchema(BaseModel):
    """Schema for user progression data."""

    id: int
    user_id: int
    chain_id: str
    current_exercise_order: int
    best_reps: int
    best_sets: int
    total_workouts_at_level: int
    reps_to_progress: int
    sets_to_progress: int
    can_progress: bool
    started_at: datetime
    last_workout_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProgressionStatusSchema(BaseModel):
    """Detailed progression status."""

    chain_id: str
    chain_name: str
    chain_name_pl: Optional[str] = None
    current_level: int
    total_levels: int
    current_exercise: ExerciseSchema
    next_exercise: Optional[ExerciseSchema] = None
    previous_exercise: Optional[ExerciseSchema] = None
    best_reps: int
    best_sets: int
    reps_to_progress: int
    sets_to_progress: int
    can_progress: bool
    total_workouts_at_level: int
    progress_percentage: float


class RecordWorkoutSchema(BaseModel):
    """Schema for recording a workout."""
    sets: int
    reps: int
    notes: Optional[str] = None


class WorkoutLogSchema(BaseModel):
    """Schema for workout log entry."""

    id: int
    user_id: int
    exercise_id: str
    chain_id: str
    sets: int
    reps: int
    notes: Optional[str] = None
    created_at: datetime
    exercise: Optional[ExerciseSchema] = None

    class Config:
        from_attributes = True
