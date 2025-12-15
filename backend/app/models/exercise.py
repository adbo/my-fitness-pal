"""Exercise and progression chain database models."""

import enum
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship

from ..db.database import Base


class MuscleGroup(str, enum.Enum):
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


class DifficultyLevel(int, enum.Enum):
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


class ProgressionChain(Base):
    """A chain of exercises from easiest to hardest."""

    __tablename__ = "progression_chains"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    name_pl = Column(String(100))
    description = Column(Text)

    exercises = relationship(
        "Exercise",
        back_populates="chain",
        order_by="Exercise.progression_order"
    )


class Exercise(Base):
    """Single exercise with progression info."""

    __tablename__ = "exercises"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    name_pl = Column(String(100))
    description = Column(Text)
    difficulty = Column(Integer, default=1)

    # Progression
    chain_id = Column(String(50), ForeignKey("progression_chains.id"))
    progression_order = Column(Integer, default=0)

    # Exercise parameters
    default_sets = Column(Integer, default=3)
    default_reps = Column(Integer, default=10)
    default_hold_seconds = Column(Integer, nullable=True)

    # JSON fields for lists
    muscle_groups = Column(JSON, default=list)
    tips = Column(JSON, default=list)
    common_mistakes = Column(JSON, default=list)

    chain = relationship("ProgressionChain", back_populates="exercises")
