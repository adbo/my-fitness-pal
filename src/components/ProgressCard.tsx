import type { ProgressionStatus } from '../types';
import { SETS_TO_PROGRESS, REPS_TO_PROGRESS } from '../types';

interface Props {
  status: ProgressionStatus;
}

export default function ProgressCard({ status }: Props) {
  const currentLevel = status.progress.current_order + 1;
  const totalLevels = status.chain.exercises.length;

  return (
    <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
      <div className="card-header">
        <div>
          <h3 className="card-title">{status.chain.name_pl || status.chain.name}</h3>
        </div>
        <span style={{
          background: status.can_progress ? 'var(--success)' : 'var(--gray-300)',
          color: 'white',
          padding: '0.25rem 0.75rem',
          borderRadius: '9999px',
          fontSize: '0.75rem',
          fontWeight: 500,
        }}>
          {status.can_progress ? 'Można awansować!' : `${currentLevel}/${totalLevels}`}
        </span>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <p style={{ fontWeight: 500 }}>{status.current_exercise.name_pl || status.current_exercise.name}</p>
        <p style={{ fontSize: '0.875rem', color: 'var(--gray-500)' }}>
          {status.current_exercise.default_sets} serie × {status.current_exercise.default_reps} powtórzeń
        </p>
      </div>

      <div className="progress-bar">
        <div
          className={`progress-fill ${status.can_progress ? 'success' : ''}`}
          style={{ width: `${status.progress_percentage}%` }}
        />
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem', fontSize: '0.875rem', color: 'var(--gray-500)' }}>
        <span>Serie: {status.progress.best_sets}/{SETS_TO_PROGRESS}</span>
        <span>Powtórzenia: {status.progress.best_reps}/{REPS_TO_PROGRESS}</span>
      </div>
    </div>
  );
}
