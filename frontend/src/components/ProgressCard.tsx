import type { ProgressionStatus } from '../types';
import DifficultyBar from './DifficultyBar';

interface Props {
  progression: ProgressionStatus;
}

export default function ProgressCard({ progression }: Props) {
  return (
    <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
      <div className="card-header">
        <div>
          <h3 className="card-title">{progression.chain_name_pl || progression.chain_name}</h3>
        </div>
        <span style={{
          background: progression.can_progress ? 'var(--success)' : 'var(--gray-300)',
          color: 'white',
          padding: '0.25rem 0.75rem',
          borderRadius: '9999px',
          fontSize: '0.75rem',
          fontWeight: 500,
        }}>
          {progression.can_progress ? 'Można awansować!' : `${progression.current_level}/${progression.total_levels}`}
        </span>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <p style={{ fontWeight: 500 }}>{progression.current_exercise.name_pl || progression.current_exercise.name}</p>
        <p style={{ fontSize: '0.875rem', color: 'var(--gray-500)' }}>
          {progression.current_exercise.default_sets} serie × {progression.current_exercise.default_reps} powtórzeń
        </p>
      </div>

      <div className="progress-bar">
        <div
          className={`progress-fill ${progression.can_progress ? 'success' : ''}`}
          style={{ width: `${progression.progress_percentage}%` }}
        />
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem', fontSize: '0.875rem', color: 'var(--gray-500)' }}>
        <span>Serie: {progression.best_sets}/{progression.sets_to_progress}</span>
        <span>Powtórzenia: {progression.best_reps}/{progression.reps_to_progress}</span>
      </div>
    </div>
  );
}
