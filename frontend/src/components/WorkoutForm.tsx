import { useState } from 'react';

interface Props {
  onSubmit: (sets: number, reps: number) => void;
  defaultSets: number;
  defaultReps: number;
}

export default function WorkoutForm({ onSubmit, defaultSets, defaultReps }: Props) {
  const [sets, setSets] = useState(defaultSets);
  const [reps, setReps] = useState(defaultReps);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit(sets, reps);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="workout-form">
      <div className="form-group">
        <label htmlFor="sets">Serie</label>
        <input
          id="sets"
          type="number"
          className="input"
          value={sets}
          onChange={(e) => setSets(parseInt(e.target.value) || 0)}
          min="1"
          max="10"
          style={{ width: '100px' }}
        />
      </div>

      <div className="form-group">
        <label htmlFor="reps">Powtórzenia</label>
        <input
          id="reps"
          type="number"
          className="input"
          value={reps}
          onChange={(e) => setReps(parseInt(e.target.value) || 0)}
          min="1"
          max="100"
          style={{ width: '100px' }}
        />
      </div>

      <button
        type="submit"
        className="btn btn-primary"
        disabled={submitting}
      >
        {submitting ? 'Zapisywanie...' : 'Zapisz trening'}
      </button>
    </form>
  );
}
