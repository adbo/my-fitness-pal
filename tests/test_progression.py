"""Tests for the progression system."""

import pytest
from src.models import Exercise, MuscleGroup, DifficultyLevel, ProgressionChain, UserProgression
from src.services import ProgressionService
from src.data import PUSH_UP_PROGRESSION, ALL_PROGRESSIONS


class TestExercise:
    """Tests for the Exercise model."""

    def test_exercise_creation(self) -> None:
        """Test creating an exercise."""
        exercise = Exercise(
            id="test_ex",
            name="Test Exercise",
            description="A test exercise",
            muscle_groups=[MuscleGroup.CHEST],
            difficulty=DifficultyLevel.BEGINNER,
        )
        assert exercise.id == "test_ex"
        assert exercise.name == "Test Exercise"
        assert exercise.difficulty == DifficultyLevel.BEGINNER

    def test_exercise_string_representation(self) -> None:
        """Test exercise __str__ method."""
        exercise = Exercise(
            id="test",
            name="Push-up",
            description="Test",
            muscle_groups=[MuscleGroup.CHEST],
            difficulty=DifficultyLevel.INTERMEDIATE,
        )
        assert "Push-up" in str(exercise)
        assert "5" in str(exercise)  # INTERMEDIATE = 5


class TestProgressionChain:
    """Tests for the ProgressionChain model."""

    def test_chain_creation(self) -> None:
        """Test creating a progression chain."""
        chain = ProgressionChain(
            id="test_chain",
            name="Test Chain",
            description="A test progression chain",
        )
        assert chain.id == "test_chain"
        assert chain.total_levels == 0

    def test_pushup_progression_has_exercises(self) -> None:
        """Test that push-up progression has exercises."""
        assert PUSH_UP_PROGRESSION.total_levels > 0
        assert PUSH_UP_PROGRESSION.exercises[0].name == "Wall Push-ups"

    def test_get_exercise_by_order(self) -> None:
        """Test getting exercise by order."""
        first = PUSH_UP_PROGRESSION.get_exercise_by_order(0)
        assert first is not None
        assert first.id == "pushup_wall"

    def test_get_next_exercise(self) -> None:
        """Test getting next exercise in progression."""
        first = PUSH_UP_PROGRESSION.get_first_exercise()
        second = PUSH_UP_PROGRESSION.get_next_exercise(first)
        assert second is not None
        assert second.progression_order == 1


class TestUserProgression:
    """Tests for UserProgression model."""

    def test_record_workout(self) -> None:
        """Test recording a workout."""
        progression = UserProgression(
            user_id="test",
            chain_id="pushup",
        )
        assert progression.best_reps == 0
        assert progression.best_sets == 0

        progression.record_workout(sets=3, reps=10)
        assert progression.best_reps == 10
        assert progression.best_sets == 3

    def test_can_progress(self) -> None:
        """Test progression criteria."""
        progression = UserProgression(
            user_id="test",
            chain_id="pushup",
            reps_to_progress=12,
            sets_to_progress=3,
        )
        assert not progression.can_progress

        progression.record_workout(sets=3, reps=12)
        assert progression.can_progress

    def test_progress_to_next(self) -> None:
        """Test progressing to next exercise."""
        progression = UserProgression(
            user_id="test",
            chain_id="pushup",
        )
        progression.record_workout(sets=3, reps=12)

        initial_order = progression.current_exercise_order
        success = progression.progress_to_next()

        assert success
        assert progression.current_exercise_order == initial_order + 1
        assert progression.best_reps == 0  # Reset after progression


class TestProgressionService:
    """Tests for ProgressionService."""

    def test_register_chain(self) -> None:
        """Test registering a progression chain."""
        service = ProgressionService()
        service.register_chain(PUSH_UP_PROGRESSION)

        chain = service.get_chain("pushup")
        assert chain is not None
        assert chain.name == "Push-up Progression"

    def test_start_chain(self) -> None:
        """Test starting a user on a chain."""
        service = ProgressionService()
        service.register_chain(PUSH_UP_PROGRESSION)

        progression = service.start_chain("user1", "pushup")
        assert progression is not None
        assert progression.current_exercise_order == 0

    def test_get_current_exercise(self) -> None:
        """Test getting current exercise for user."""
        service = ProgressionService()
        service.register_chain(PUSH_UP_PROGRESSION)
        service.start_chain("user1", "pushup")

        exercise = service.get_current_exercise("user1", "pushup")
        assert exercise is not None
        assert exercise.id == "pushup_wall"

    def test_record_performance_progression(self) -> None:
        """Test recording performance and unlocking progression."""
        service = ProgressionService()
        service.register_chain(PUSH_UP_PROGRESSION)
        service.start_chain("user1", "pushup")

        # Record performance that meets criteria
        can_progress, _ = service.record_performance("user1", "pushup", sets=3, reps=15)
        assert can_progress

    def test_progress_user(self) -> None:
        """Test progressing user to next exercise."""
        service = ProgressionService()
        service.register_chain(PUSH_UP_PROGRESSION)
        service.start_chain("user1", "pushup")
        service.record_performance("user1", "pushup", sets=3, reps=15)

        success, message = service.progress_user("user1", "pushup")
        assert success
        assert "Incline" in message

        # Verify new exercise
        exercise = service.get_current_exercise("user1", "pushup")
        assert exercise.id == "pushup_incline"


class TestAllProgressions:
    """Tests for all progression data."""

    def test_all_progressions_exist(self) -> None:
        """Test that all progressions are defined."""
        assert len(ALL_PROGRESSIONS) >= 6  # At least 6 progressions

    def test_all_progressions_have_exercises(self) -> None:
        """Test that all progressions have exercises."""
        for chain in ALL_PROGRESSIONS:
            assert chain.total_levels > 0, f"{chain.name} has no exercises"

    def test_exercise_ordering(self) -> None:
        """Test that exercises are properly ordered."""
        for chain in ALL_PROGRESSIONS:
            for i, exercise in enumerate(chain.exercises):
                assert exercise.progression_order == i, (
                    f"Exercise {exercise.name} has wrong order"
                )

    def test_polish_names_exist(self) -> None:
        """Test that Polish names are defined."""
        for chain in ALL_PROGRESSIONS:
            assert chain.name_pl, f"{chain.name} missing Polish name"
            for exercise in chain.exercises:
                assert exercise.name_pl, f"{exercise.name} missing Polish name"
