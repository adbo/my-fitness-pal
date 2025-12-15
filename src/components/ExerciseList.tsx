import type { Exercise } from '../types';
import DifficultyBar from './DifficultyBar';

interface Props {
  exercises: Exercise[];
  currentOrder: number;
}

export default function ExerciseList({ exercises, currentOrder }: Props) {
  return (
    <div className="exercise-list">
      {exercises.map((exercise, index) => {
        const isCurrent = index === currentOrder;
        const isCompleted = index < currentOrder;

        return (
          <div
            key={exercise.id}
            className={`exercise-item ${isCurrent ? 'current' : ''} ${isCompleted ? 'completed' : ''}`}
          >
            <div className="exercise-number">{index + 1}</div>
            <div className="exercise-info">
              <div className="exercise-name">
                {exercise.name_pl || exercise.name}
              </div>
              <div className="exercise-name-pl">
                {exercise.default_sets} × {exercise.default_reps}
                {exercise.default_hold_seconds && ` (${exercise.default_hold_seconds}s)`}
              </div>
            </div>
            <DifficultyBar difficulty={exercise.difficulty} />
          </div>
        );
      })}
    </div>
  );
}
