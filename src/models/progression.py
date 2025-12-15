"""Progression chain and user progression tracking models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .exercise import Exercise


class ProgressionChain(BaseModel):
    """
    A chain of exercises from easiest to hardest.

    Users progress through the chain by mastering each exercise
    before moving to the next, harder variant.

    Example chain for push-ups:
    1. Wall Push-ups (easiest)
    2. Counter/Incline Push-ups
    3. Knee Push-ups
    4. Full Push-ups
    5. Diamond Push-ups
    6. Archer Push-ups
    7. One-arm Push-ups (hardest)
    """

    id: str = Field(..., description="Unique identifier for the chain")
    name: str = Field(..., description="Name of the progression (e.g., 'Push-up Progression')")
    name_pl: Optional[str] = Field(None, description="Polish name")
    description: str = Field(..., description="Description of the progression")
    exercises: list[Exercise] = Field(
        default_factory=list,
        description="Exercises in order from easiest to hardest"
    )

    def get_exercise_by_order(self, order: int) -> Optional[Exercise]:
        """Get exercise at specific position in the chain."""
        for exercise in self.exercises:
            if exercise.progression_order == order:
                return exercise
        return None

    def get_next_exercise(self, current_exercise: Exercise) -> Optional[Exercise]:
        """Get the next harder exercise in the progression."""
        return self.get_exercise_by_order(current_exercise.progression_order + 1)

    def get_previous_exercise(self, current_exercise: Exercise) -> Optional[Exercise]:
        """Get the previous easier exercise in the progression."""
        if current_exercise.progression_order <= 0:
            return None
        return self.get_exercise_by_order(current_exercise.progression_order - 1)

    def get_first_exercise(self) -> Optional[Exercise]:
        """Get the easiest exercise in the chain."""
        return self.get_exercise_by_order(0)

    def get_last_exercise(self) -> Optional[Exercise]:
        """Get the hardest exercise in the chain."""
        if not self.exercises:
            return None
        max_order = max(e.progression_order for e in self.exercises)
        return self.get_exercise_by_order(max_order)

    @property
    def total_levels(self) -> int:
        """Total number of exercises in the progression."""
        return len(self.exercises)

    def __str__(self) -> str:
        return f"{self.name} ({self.total_levels} levels)"


class UserProgression(BaseModel):
    """
    Tracks a user's progress in a specific progression chain.

    Records which exercise level they're currently at and their history.
    """

    user_id: str = Field(..., description="User identifier")
    chain_id: str = Field(..., description="Progression chain identifier")
    current_exercise_order: int = Field(
        default=0,
        ge=0,
        description="Current position in the progression chain"
    )

    # Progress tracking
    started_at: datetime = Field(default_factory=datetime.now)
    last_workout_at: Optional[datetime] = None

    # Performance at current level
    best_reps: int = Field(default=0, description="Best reps achieved at current level")
    best_sets: int = Field(default=0, description="Best sets achieved at current level")
    total_workouts_at_level: int = Field(
        default=0, description="Number of workouts at current level"
    )

    # Progression criteria
    reps_to_progress: int = Field(
        default=12, description="Reps needed to unlock next level"
    )
    sets_to_progress: int = Field(
        default=3, description="Sets needed to unlock next level"
    )

    @property
    def can_progress(self) -> bool:
        """Check if user has met criteria to progress to next exercise."""
        return (
            self.best_reps >= self.reps_to_progress and
            self.best_sets >= self.sets_to_progress
        )

    def record_workout(self, sets: int, reps: int) -> bool:
        """
        Record a workout performance.

        Returns True if this performance unlocks progression.
        """
        self.last_workout_at = datetime.now()
        self.total_workouts_at_level += 1

        if reps > self.best_reps:
            self.best_reps = reps
        if sets > self.best_sets:
            self.best_sets = sets

        return self.can_progress

    def progress_to_next(self) -> bool:
        """
        Move to the next exercise in the progression.

        Returns True if progression was successful.
        """
        if not self.can_progress:
            return False

        self.current_exercise_order += 1
        self.best_reps = 0
        self.best_sets = 0
        self.total_workouts_at_level = 0
        return True

    def regress_to_previous(self) -> bool:
        """
        Move back to the previous easier exercise.

        Returns True if regression was successful.
        """
        if self.current_exercise_order <= 0:
            return False

        self.current_exercise_order -= 1
        self.best_reps = 0
        self.best_sets = 0
        self.total_workouts_at_level = 0
        return True
