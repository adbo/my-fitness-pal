import type { Exercise } from '../types';
import DifficultyBar from './DifficultyBar';

interface Props {
  exercise: Exercise;
}

export default function ExerciseDetails({ exercise }: Props) {
  return (
    <div>
      <div style={{ marginBottom: '1rem' }}>
        <h4 style={{ marginBottom: '0.25rem' }}>{exercise.name_pl || exercise.name}</h4>
        {exercise.name_pl && (
          <p style={{ color: 'var(--gray-500)', fontSize: '0.875rem' }}>{exercise.name}</p>
        )}
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
          <span style={{ fontWeight: 500 }}>Trudność:</span>
          <DifficultyBar difficulty={exercise.difficulty} />
        </div>
        <p style={{ fontSize: '0.875rem', color: 'var(--gray-500)' }}>
          {exercise.default_sets} serie × {exercise.default_reps} powtórzeń
          {exercise.default_hold_seconds && ` (trzymaj ${exercise.default_hold_seconds}s)`}
        </p>
      </div>

      {exercise.description && (
        <div style={{ marginBottom: '1rem' }}>
          <h5 style={{ marginBottom: '0.5rem' }}>Opis</h5>
          <p style={{ fontSize: '0.875rem', color: 'var(--gray-700)' }}>{exercise.description}</p>
        </div>
      )}

      {exercise.muscle_groups.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <h5 style={{ marginBottom: '0.5rem' }}>Partie mięśniowe</h5>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {exercise.muscle_groups.map((muscle) => (
              <span
                key={muscle}
                style={{
                  background: 'var(--gray-200)',
                  padding: '0.25rem 0.75rem',
                  borderRadius: '9999px',
                  fontSize: '0.75rem',
                }}
              >
                {muscle}
              </span>
            ))}
          </div>
        </div>
      )}

      {exercise.tips.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <h5 style={{ marginBottom: '0.5rem' }}>Wskazówki</h5>
          <ul className="tips-list">
            {exercise.tips.map((tip, i) => (
              <li key={i}>{tip}</li>
            ))}
          </ul>
        </div>
      )}

      {exercise.common_mistakes.length > 0 && (
        <div>
          <h5 style={{ marginBottom: '0.5rem' }}>Typowe błędy</h5>
          <ul className="tips-list mistakes-list">
            {exercise.common_mistakes.map((mistake, i) => (
              <li key={i}>{mistake}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
