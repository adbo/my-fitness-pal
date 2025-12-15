"""Service for managing workouts."""

from datetime import datetime
from typing import Optional
import uuid

from ..models import Exercise, Workout, WorkoutExercise
from .progression_service import ProgressionService


class WorkoutService:
    """
    Service for creating and managing workouts.

    Integrates with ProgressionService to:
    - Create workouts with exercises at user's current progression level
    - Record workout results and update progressions
    """

    def __init__(self, progression_service: ProgressionService) -> None:
        self._progression_service = progression_service
        self._workouts: dict[str, Workout] = {}
        self._user_workouts: dict[str, list[str]] = {}

    def create_workout(
        self,
        name: str,
        user_id: str,
        exercises: Optional[list[Exercise]] = None,
        name_pl: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Workout:
        """Create a new workout."""
        workout = Workout(
            id=str(uuid.uuid4()),
            name=name,
            name_pl=name_pl,
            description=description,
        )

        if exercises:
            for exercise in exercises:
                workout.add_exercise(exercise)

        self._workouts[workout.id] = workout

        if user_id not in self._user_workouts:
            self._user_workouts[user_id] = []
        self._user_workouts[user_id].append(workout.id)

        return workout

    def create_progression_workout(
        self,
        name: str,
        user_id: str,
        chain_ids: list[str],
        name_pl: Optional[str] = None,
    ) -> Optional[Workout]:
        """
        Create a workout using exercises at user's current progression level.

        For each chain_id, adds the exercise the user is currently working on.
        """
        exercises = []

        for chain_id in chain_ids:
            exercise = self._progression_service.get_current_exercise(user_id, chain_id)
            if exercise:
                exercises.append(exercise)

        if not exercises:
            return None

        return self.create_workout(
            name=name,
            user_id=user_id,
            exercises=exercises,
            name_pl=name_pl,
            description="Workout based on your current progression levels",
        )

    def get_workout(self, workout_id: str) -> Optional[Workout]:
        """Get a workout by ID."""
        return self._workouts.get(workout_id)

    def get_user_workouts(self, user_id: str) -> list[Workout]:
        """Get all workouts for a user."""
        workout_ids = self._user_workouts.get(user_id, [])
        return [
            self._workouts[wid]
            for wid in workout_ids
            if wid in self._workouts
        ]

    def start_workout(self, workout_id: str) -> Optional[Workout]:
        """Start a workout session."""
        workout = self.get_workout(workout_id)
        if workout:
            workout.start()
        return workout

    def complete_exercise(
        self,
        workout_id: str,
        exercise_index: int,
        completed_sets: int,
        completed_reps: int,
        notes: Optional[str] = None,
    ) -> Optional[WorkoutExercise]:
        """Record completion of an exercise in a workout."""
        workout = self.get_workout(workout_id)
        if not workout or exercise_index >= len(workout.exercises):
            return None

        workout_exercise = workout.exercises[exercise_index]
        workout_exercise.completed_sets = completed_sets
        workout_exercise.completed_reps = completed_reps
        workout_exercise.notes = notes

        return workout_exercise

    def complete_workout(
        self,
        workout_id: str,
        user_id: str,
    ) -> tuple[Workout, list[tuple[str, bool, str]]]:
        """
        Complete a workout and record all results in progressions.

        Returns:
            Tuple of (workout, list of (chain_id, can_progress, message))
        """
        workout = self.get_workout(workout_id)
        if not workout:
            raise ValueError(f"Workout {workout_id} not found")

        workout.complete()

        progression_results = []

        for workout_exercise in workout.exercises:
            if not workout_exercise.is_completed:
                continue

            exercise = workout_exercise.exercise
            if not exercise.progression_chain_id:
                continue

            can_progress, message = self._progression_service.record_performance(
                user_id=user_id,
                chain_id=exercise.progression_chain_id,
                sets=workout_exercise.completed_sets or 0,
                reps=workout_exercise.completed_reps or 0,
            )

            progression_results.append(
                (exercise.progression_chain_id, can_progress, message)
            )

        return workout, progression_results

    def get_workout_history(
        self,
        user_id: str,
        completed_only: bool = True,
    ) -> list[Workout]:
        """Get workout history for a user."""
        workouts = self.get_user_workouts(user_id)
        if completed_only:
            workouts = [w for w in workouts if w.is_completed]
        return sorted(
            workouts,
            key=lambda w: w.completed_at or w.created_at,
            reverse=True,
        )
