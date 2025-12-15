"""Service for managing exercise progressions."""

from typing import Optional

from ..models import Exercise, ProgressionChain, UserProgression


class ProgressionService:
    """
    Service for managing exercise progression chains and user progress.

    Handles:
    - Loading and managing progression chains
    - Tracking user progress through chains
    - Recommending when to progress/regress
    - Getting appropriate exercises for user's level
    """

    def __init__(self) -> None:
        self._chains: dict[str, ProgressionChain] = {}
        self._user_progressions: dict[str, dict[str, UserProgression]] = {}

    def register_chain(self, chain: ProgressionChain) -> None:
        """Register a progression chain."""
        self._chains[chain.id] = chain

        # Update exercise chain references
        for i, exercise in enumerate(chain.exercises):
            exercise.progression_chain_id = chain.id
            exercise.progression_order = i

    def get_chain(self, chain_id: str) -> Optional[ProgressionChain]:
        """Get a progression chain by ID."""
        return self._chains.get(chain_id)

    def get_all_chains(self) -> list[ProgressionChain]:
        """Get all registered progression chains."""
        return list(self._chains.values())

    def get_user_progression(
        self, user_id: str, chain_id: str
    ) -> Optional[UserProgression]:
        """Get user's progress in a specific chain."""
        user_progs = self._user_progressions.get(user_id, {})
        return user_progs.get(chain_id)

    def start_chain(self, user_id: str, chain_id: str) -> Optional[UserProgression]:
        """Start a user on a progression chain at the first exercise."""
        chain = self.get_chain(chain_id)
        if not chain:
            return None

        if user_id not in self._user_progressions:
            self._user_progressions[user_id] = {}

        progression = UserProgression(
            user_id=user_id,
            chain_id=chain_id,
            current_exercise_order=0,
        )
        self._user_progressions[user_id][chain_id] = progression
        return progression

    def get_current_exercise(
        self, user_id: str, chain_id: str
    ) -> Optional[Exercise]:
        """Get the current exercise for a user in a progression chain."""
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return None

        chain = self.get_chain(chain_id)
        if not chain:
            return None

        return chain.get_exercise_by_order(progression.current_exercise_order)

    def record_performance(
        self,
        user_id: str,
        chain_id: str,
        sets: int,
        reps: int,
    ) -> tuple[bool, str]:
        """
        Record a user's performance in their current exercise.

        Returns:
            Tuple of (can_progress, message)
        """
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return False, "User has not started this progression chain."

        chain = self.get_chain(chain_id)
        if not chain:
            return False, "Progression chain not found."

        current_exercise = chain.get_exercise_by_order(
            progression.current_exercise_order
        )
        if not current_exercise:
            return False, "Current exercise not found."

        unlocked = progression.record_workout(sets, reps)

        if unlocked:
            next_exercise = chain.get_next_exercise(current_exercise)
            if next_exercise:
                return True, (
                    f"Excellent! You've mastered {current_exercise.name}! "
                    f"You can now progress to: {next_exercise.name}"
                )
            else:
                return True, (
                    f"Amazing! You've completed the entire {chain.name}! "
                    f"You've mastered the hardest exercise: {current_exercise.name}"
                )

        reps_needed = max(0, progression.reps_to_progress - progression.best_reps)
        sets_needed = max(0, progression.sets_to_progress - progression.best_sets)

        return False, (
            f"Good workout! To progress from {current_exercise.name}, "
            f"you need: {reps_needed} more reps, {sets_needed} more sets."
        )

    def progress_user(self, user_id: str, chain_id: str) -> tuple[bool, str]:
        """
        Move user to the next exercise in the chain.

        Returns:
            Tuple of (success, message)
        """
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return False, "User has not started this progression chain."

        chain = self.get_chain(chain_id)
        if not chain:
            return False, "Progression chain not found."

        current = chain.get_exercise_by_order(progression.current_exercise_order)
        next_ex = chain.get_exercise_by_order(progression.current_exercise_order + 1)

        if not next_ex:
            return False, "Already at the highest level in this progression."

        if not progression.can_progress:
            return False, (
                f"Haven't met progression criteria yet. "
                f"Need {progression.reps_to_progress} reps for {progression.sets_to_progress} sets."
            )

        progression.progress_to_next()
        return True, f"Progressed from {current.name} to {next_ex.name}!"

    def regress_user(self, user_id: str, chain_id: str) -> tuple[bool, str]:
        """
        Move user back to the previous exercise in the chain.

        Returns:
            Tuple of (success, message)
        """
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return False, "User has not started this progression chain."

        chain = self.get_chain(chain_id)
        if not chain:
            return False, "Progression chain not found."

        if progression.current_exercise_order <= 0:
            return False, "Already at the easiest level in this progression."

        current = chain.get_exercise_by_order(progression.current_exercise_order)
        prev_ex = chain.get_exercise_by_order(progression.current_exercise_order - 1)

        progression.regress_to_previous()
        return True, f"Regressed from {current.name} to {prev_ex.name}."

    def get_progression_status(self, user_id: str, chain_id: str) -> Optional[dict]:
        """Get detailed progression status for a user in a chain."""
        progression = self.get_user_progression(user_id, chain_id)
        if not progression:
            return None

        chain = self.get_chain(chain_id)
        if not chain:
            return None

        current = chain.get_exercise_by_order(progression.current_exercise_order)
        next_ex = chain.get_next_exercise(current) if current else None
        prev_ex = chain.get_previous_exercise(current) if current else None

        return {
            "chain_name": chain.name,
            "current_exercise": current,
            "next_exercise": next_ex,
            "previous_exercise": prev_ex,
            "current_level": progression.current_exercise_order + 1,
            "total_levels": chain.total_levels,
            "best_reps": progression.best_reps,
            "best_sets": progression.best_sets,
            "reps_to_progress": progression.reps_to_progress,
            "sets_to_progress": progression.sets_to_progress,
            "can_progress": progression.can_progress,
            "total_workouts_at_level": progression.total_workouts_at_level,
        }
