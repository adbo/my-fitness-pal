"""Exercise model with muscle groups and difficulty levels."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MuscleGroup(str, Enum):
    """Target muscle groups for exercises."""

    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    CORE = "core"
    QUADRICEPS = "quadriceps"
    HAMSTRINGS = "hamstrings"
    GLUTES = "glutes"
    CALVES = "calves"
    FULL_BODY = "full_body"


class DifficultyLevel(int, Enum):
    """Difficulty level from 1 (easiest) to 10 (hardest)."""

    BEGINNER = 1
    BEGINNER_PLUS = 2
    EASY = 3
    EASY_PLUS = 4
    INTERMEDIATE = 5
    INTERMEDIATE_PLUS = 6
    ADVANCED = 7
    ADVANCED_PLUS = 8
    EXPERT = 9
    MASTER = 10


class Exercise(BaseModel):
    """
    Represents a single exercise with its properties.

    Exercises can be part of a progression chain, where they link
    to easier (previous) and harder (next) variants.
    """

    id: str = Field(..., description="Unique identifier for the exercise")
    name: str = Field(..., description="Display name of the exercise")
    name_pl: Optional[str] = Field(None, description="Polish name of the exercise")
    description: str = Field(..., description="How to perform the exercise")
    muscle_groups: list[MuscleGroup] = Field(
        ..., description="Primary muscle groups targeted"
    )
    difficulty: DifficultyLevel = Field(
        ..., description="Difficulty level of the exercise"
    )

    # Progression links
    progression_chain_id: Optional[str] = Field(
        None, description="ID of the progression chain this exercise belongs to"
    )
    progression_order: int = Field(
        default=0, description="Order in the progression chain (0 = easiest)"
    )

    # Exercise parameters
    default_sets: int = Field(default=3, ge=1, le=10)
    default_reps: int = Field(default=10, ge=1, le=100)
    default_hold_seconds: Optional[int] = Field(
        None, description="For isometric exercises, hold time in seconds"
    )

    # Tips and notes
    tips: list[str] = Field(default_factory=list, description="Form tips")
    common_mistakes: list[str] = Field(
        default_factory=list, description="Common mistakes to avoid"
    )

    def __str__(self) -> str:
        return f"{self.name} (Level {self.difficulty.value})"

    def __repr__(self) -> str:
        return f"Exercise(id='{self.id}', name='{self.name}', difficulty={self.difficulty})"
