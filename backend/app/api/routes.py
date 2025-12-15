"""API routes for fitness tracking."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..services import ProgressionService, UserService
from ..schemas import (
    ProgressionChainSchema,
    ProgressionChainListSchema,
    ExerciseSchema,
    UserSchema,
    UserCreateSchema,
    ProgressionStatusSchema,
    RecordWorkoutSchema,
    WorkoutLogSchema,
)

router = APIRouter()


# =============================================================================
# Progression Chains
# =============================================================================

@router.get("/progressions", response_model=list[ProgressionChainListSchema])
def list_progressions(db: Session = Depends(get_db)):
    """Get all progression chains."""
    service = ProgressionService(db)
    chains = service.get_all_chains()
    return [
        ProgressionChainListSchema(
            id=c.id,
            name=c.name,
            name_pl=c.name_pl,
            description=c.description,
            total_levels=len(c.exercises),
        )
        for c in chains
    ]


@router.get("/progressions/{chain_id}", response_model=ProgressionChainSchema)
def get_progression(chain_id: str, db: Session = Depends(get_db)):
    """Get a progression chain with all exercises."""
    service = ProgressionService(db)
    chain = service.get_chain(chain_id)
    if not chain:
        raise HTTPException(status_code=404, detail="Progression chain not found")
    return chain


@router.get("/exercises/{exercise_id}", response_model=ExerciseSchema)
def get_exercise(exercise_id: str, db: Session = Depends(get_db)):
    """Get exercise details."""
    service = ProgressionService(db)
    exercise = service.get_exercise(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


# =============================================================================
# Users
# =============================================================================

@router.post("/users", response_model=UserSchema)
def create_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    """Create a new user or get existing."""
    service = UserService(db)
    user = service.get_or_create_user(user_data.username)
    return user


@router.get("/users/{username}", response_model=UserSchema)
def get_user(username: str, db: Session = Depends(get_db)):
    """Get user by username."""
    service = UserService(db)
    user = service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# =============================================================================
# User Progressions
# =============================================================================

@router.post("/users/{username}/progressions/{chain_id}/start")
def start_progression(username: str, chain_id: str, db: Session = Depends(get_db)):
    """Start a user on a progression chain."""
    user_service = UserService(db)
    user = user_service.get_or_create_user(username)

    prog_service = ProgressionService(db)
    progression = prog_service.start_chain(user.id, chain_id)

    if not progression:
        raise HTTPException(status_code=404, detail="Progression chain not found")

    return {"message": "Progression started", "chain_id": chain_id}


@router.get(
    "/users/{username}/progressions/{chain_id}",
    response_model=ProgressionStatusSchema
)
def get_user_progression_status(
    username: str,
    chain_id: str,
    db: Session = Depends(get_db)
):
    """Get user's detailed status in a progression chain."""
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prog_service = ProgressionService(db)

    # Auto-start if not started
    if not prog_service.get_user_progression(user.id, chain_id):
        prog_service.start_chain(user.id, chain_id)

    status = prog_service.get_progression_status(user.id, chain_id)
    if not status:
        raise HTTPException(status_code=404, detail="Progression not found")

    return status


@router.get("/users/{username}/progressions")
def get_all_user_progressions(username: str, db: Session = Depends(get_db)):
    """Get all progression statuses for a user."""
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prog_service = ProgressionService(db)
    chains = prog_service.get_all_chains()

    statuses = []
    for chain in chains:
        # Auto-start all chains
        if not prog_service.get_user_progression(user.id, chain.id):
            prog_service.start_chain(user.id, chain.id)

        status = prog_service.get_progression_status(user.id, chain.id)
        if status:
            statuses.append(status)

    return statuses


@router.post("/users/{username}/progressions/{chain_id}/record")
def record_workout(
    username: str,
    chain_id: str,
    workout: RecordWorkoutSchema,
    db: Session = Depends(get_db)
):
    """Record a workout for the current exercise in a progression."""
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prog_service = ProgressionService(db)

    # Auto-start if not started
    if not prog_service.get_user_progression(user.id, chain_id):
        prog_service.start_chain(user.id, chain_id)

    can_progress, message, progression = prog_service.record_workout(
        user.id, chain_id, workout.sets, workout.reps, workout.notes
    )

    if progression is None:
        raise HTTPException(status_code=400, detail=message)

    return {
        "message": message,
        "can_progress": can_progress,
        "best_reps": progression.best_reps,
        "best_sets": progression.best_sets,
    }


@router.post("/users/{username}/progressions/{chain_id}/advance")
def advance_progression(username: str, chain_id: str, db: Session = Depends(get_db)):
    """Progress to the next exercise in a chain."""
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prog_service = ProgressionService(db)
    success, message = prog_service.progress_user(user.id, chain_id)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message, "success": True}


@router.post("/users/{username}/progressions/{chain_id}/regress")
def regress_progression(username: str, chain_id: str, db: Session = Depends(get_db)):
    """Go back to the previous exercise in a chain."""
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prog_service = ProgressionService(db)
    success, message = prog_service.regress_user(user.id, chain_id)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message, "success": True}


# =============================================================================
# Workout History
# =============================================================================

@router.get("/users/{username}/history", response_model=list[WorkoutLogSchema])
def get_workout_history(
    username: str,
    chain_id: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """Get user's workout history."""
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    logs = user_service.get_workout_history(user.id, chain_id, limit)
    return logs
