"""Pydantic schemas for exercises and progressions."""

from typing import Optional
from pydantic import BaseModel


class ExerciseSchema(BaseModel):
    """Schema for exercise data."""

    id: str
    name: str
    name_pl: Optional[str] = None
    description: Optional[str] = None
    difficulty: int
    chain_id: Optional[str] = None
    progression_order: int
    default_sets: int
    default_reps: int
    default_hold_seconds: Optional[int] = None
    muscle_groups: list[str] = []
    tips: list[str] = []
    common_mistakes: list[str] = []

    class Config:
        from_attributes = True


class ProgressionChainSchema(BaseModel):
    """Schema for progression chain with exercises."""

    id: str
    name: str
    name_pl: Optional[str] = None
    description: Optional[str] = None
    exercises: list[ExerciseSchema] = []

    class Config:
        from_attributes = True


class ProgressionChainListSchema(BaseModel):
    """Schema for progression chain list (without exercises)."""

    id: str
    name: str
    name_pl: Optional[str] = None
    description: Optional[str] = None
    total_levels: int

    class Config:
        from_attributes = True
