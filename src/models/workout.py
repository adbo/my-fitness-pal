"""Workout and workout exercise models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .exercise import Exercise


class WorkoutExercise(BaseModel):
    """An exercise within a workout with specific sets and reps."""

    exercise: Exercise
    planned_sets: int = Field(default=3, ge=1)
    planned_reps: int = Field(default=10, ge=1)

    # Actual performance (filled after workout)
    completed_sets: Optional[int] = None
    completed_reps: Optional[int] = None
    notes: Optional[str] = None

    @property
    def is_completed(self) -> bool:
        """Check if exercise has been performed."""
        return self.completed_sets is not None and self.completed_reps is not None

    @property
    def completion_percentage(self) -> float:
        """Calculate how well the exercise was completed vs planned."""
        if not self.is_completed:
            return 0.0

        planned_total = self.planned_sets * self.planned_reps
        completed_total = (self.completed_sets or 0) * (self.completed_reps or 0)

        if planned_total == 0:
            return 0.0
        return min(100.0, (completed_total / planned_total) * 100)


class Workout(BaseModel):
    """A complete workout session with multiple exercises."""

    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Workout name")
    name_pl: Optional[str] = Field(None, description="Polish name")
    description: Optional[str] = None

    exercises: list[WorkoutExercise] = Field(default_factory=list)

    # Timing
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    tags: list[str] = Field(default_factory=list)

    def add_exercise(
        self,
        exercise: Exercise,
        sets: Optional[int] = None,
        reps: Optional[int] = None
    ) -> WorkoutExercise:
        """Add an exercise to the workout."""
        workout_exercise = WorkoutExercise(
            exercise=exercise,
            planned_sets=sets or exercise.default_sets,
            planned_reps=reps or exercise.default_reps,
        )
        self.exercises.append(workout_exercise)
        return workout_exercise

    def start(self) -> None:
        """Mark workout as started."""
        self.started_at = datetime.now()

    def complete(self) -> None:
        """Mark workout as completed."""
        self.completed_at = datetime.now()

    @property
    def is_completed(self) -> bool:
        """Check if workout is completed."""
        return self.completed_at is not None

    @property
    def is_in_progress(self) -> bool:
        """Check if workout is currently in progress."""
        return self.started_at is not None and self.completed_at is None

    @property
    def duration_minutes(self) -> Optional[int]:
        """Get workout duration in minutes."""
        if not self.started_at or not self.completed_at:
            return None
        delta = self.completed_at - self.started_at
        return int(delta.total_seconds() / 60)

    @property
    def total_exercises(self) -> int:
        """Total number of exercises in workout."""
        return len(self.exercises)

    @property
    def completed_exercises(self) -> int:
        """Number of completed exercises."""
        return sum(1 for e in self.exercises if e.is_completed)

    @property
    def overall_completion_percentage(self) -> float:
        """Overall workout completion percentage."""
        if not self.exercises:
            return 0.0
        total = sum(e.completion_percentage for e in self.exercises)
        return total / len(self.exercises)
