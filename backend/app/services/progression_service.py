"""Service for managing exercise progressions."""

from typing import Optional
from sqlalchemy.orm import Session

from ..models import Exercise, ProgressionChain, UserProgression, WorkoutLog
from ..schemas import ProgressionStatusSchema, ExerciseSchema


class ProgressionService:
    """Service for progression chain operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all_chains(self) -> list[ProgressionChain]:
        """Get all progression chains."""
        return self.db.query(ProgressionChain).all()

    def get_chain(self, chain_id: str) -> Optional[ProgressionChain]:
        """Get a progression chain by ID."""
        return self.db.query(ProgressionChain).filter(
            ProgressionChain.id == chain_id
        ).first()

    def get_exercise(self, exercise_id: str) -> Optional[Exercise]:
        """Get an exercise by ID."""
        return self.db.query(Exercise).filter(Exercise.id == exercise_id).first()

    def get_exercise_by_order(
        self, chain_id: str, order: int
    ) -> Optional[Exercise]:
        """Get exercise at specific position in chain."""
        return self.db.query(Exercise).filter(
            Exercise.chain_id == chain_id,
            Exercise.progression_order == order
        ).first()

    def get_user_progression(
        self, user_id: int, chain_id: str
    ) -> Optional[UserProgression]:
        """Get user's progress in a chain."""
        return self.db.query(UserProgression).filter(
            UserProgression.user_id == user_id,
            UserProgression.chain_id == chain_id
        ).first()

    def start_chain(self, user_id: int, chain_id: str) -> Optional[UserProgression]:
        """Start a user on a progression chain."""
        chain = self.get_chain(chain_id)
        if not chain:
            return None

        # Check if already started
        existing = self.get_user_progression(user_id, chain_id)
        if existing:
            return existing

        progression = UserProgression(
            user_id=user_id,
            chain_id=chain_id,
            current_exercise_order=0,
        )
        self.db.add(progression)
        self.db.commit()
        self.db.refresh(progression)
        return progression

    def get_current_exercise(
        self, user_id: int, chain_id: str
    ) -> Optional[Exercise]:
        """Get user's current exercise in a chain."""
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return None
        return self.get_exercise_by_order(chain_id, progression.current_exercise_order)

    def record_workout(
        self,
        user_id: int,
        chain_id: str,
        sets: int,
        reps: int,
        notes: Optional[str] = None,
    ) -> tuple[bool, str, Optional[UserProgression]]:
        """
        Record a workout and update progression.

        Returns: (can_progress, message, updated_progression)
        """
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return False, "Progression not started", None

        current_exercise = self.get_exercise_by_order(
            chain_id, progression.current_exercise_order
        )
        if not current_exercise:
            return False, "Exercise not found", None

        # Log the workout
        log = WorkoutLog(
            user_id=user_id,
            exercise_id=current_exercise.id,
            chain_id=chain_id,
            sets=sets,
            reps=reps,
            notes=notes,
        )
        self.db.add(log)

        # Update progression stats
        progression.total_workouts_at_level += 1
        if reps > progression.best_reps:
            progression.best_reps = reps
        if sets > progression.best_sets:
            progression.best_sets = sets

        from datetime import datetime
        progression.last_workout_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(progression)

        # Check if can progress
        if progression.can_progress:
            next_ex = self.get_exercise_by_order(
                chain_id, progression.current_exercise_order + 1
            )
            if next_ex:
                message = f"Gratulacje! Możesz przejść do: {next_ex.name_pl or next_ex.name}"
            else:
                message = f"Brawo! Ukończyłeś całą progresję!"
            return True, message, progression

        reps_needed = max(0, progression.reps_to_progress - progression.best_reps)
        sets_needed = max(0, progression.sets_to_progress - progression.best_sets)
        message = f"Dobry trening! Do progresji potrzebujesz jeszcze: {reps_needed} powtórzeń, {sets_needed} serii."
        return False, message, progression

    def progress_user(self, user_id: int, chain_id: str) -> tuple[bool, str]:
        """Move user to next exercise."""
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return False, "Progresja nie została rozpoczęta"

        if not progression.can_progress:
            return False, "Nie spełniono kryteriów progresji"

        next_ex = self.get_exercise_by_order(
            chain_id, progression.current_exercise_order + 1
        )
        if not next_ex:
            return False, "Jesteś już na najwyższym poziomie"

        current_ex = self.get_exercise_by_order(
            chain_id, progression.current_exercise_order
        )

        progression.current_exercise_order += 1
        progression.best_reps = 0
        progression.best_sets = 0
        progression.total_workouts_at_level = 0

        self.db.commit()

        return True, f"Przeszedłeś z {current_ex.name_pl or current_ex.name} do {next_ex.name_pl or next_ex.name}!"

    def regress_user(self, user_id: int, chain_id: str) -> tuple[bool, str]:
        """Move user to previous exercise."""
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return False, "Progresja nie została rozpoczęta"

        if progression.current_exercise_order <= 0:
            return False, "Jesteś już na najniższym poziomie"

        current_ex = self.get_exercise_by_order(
            chain_id, progression.current_exercise_order
        )
        prev_ex = self.get_exercise_by_order(
            chain_id, progression.current_exercise_order - 1
        )

        progression.current_exercise_order -= 1
        progression.best_reps = 0
        progression.best_sets = 0
        progression.total_workouts_at_level = 0

        self.db.commit()

        return True, f"Wróciłeś z {current_ex.name_pl or current_ex.name} do {prev_ex.name_pl or prev_ex.name}"

    def get_progression_status(
        self, user_id: int, chain_id: str
    ) -> Optional[ProgressionStatusSchema]:
        """Get detailed progression status."""
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return None

        chain = self.get_chain(chain_id)
        if not chain:
            return None

        current = self.get_exercise_by_order(chain_id, progression.current_exercise_order)
        next_ex = self.get_exercise_by_order(chain_id, progression.current_exercise_order + 1)
        prev_ex = self.get_exercise_by_order(chain_id, progression.current_exercise_order - 1) if progression.current_exercise_order > 0 else None

        total_levels = len(chain.exercises)
        current_level = progression.current_exercise_order + 1
        progress_pct = (current_level / total_levels) * 100 if total_levels > 0 else 0

        return ProgressionStatusSchema(
            chain_id=chain.id,
            chain_name=chain.name,
            chain_name_pl=chain.name_pl,
            current_level=current_level,
            total_levels=total_levels,
            current_exercise=ExerciseSchema.model_validate(current),
            next_exercise=ExerciseSchema.model_validate(next_ex) if next_ex else None,
            previous_exercise=ExerciseSchema.model_validate(prev_ex) if prev_ex else None,
            best_reps=progression.best_reps,
            best_sets=progression.best_sets,
            reps_to_progress=progression.reps_to_progress,
            sets_to_progress=progression.sets_to_progress,
            can_progress=progression.can_progress,
            total_workouts_at_level=progression.total_workouts_at_level,
            progress_percentage=progress_pct,
        )
