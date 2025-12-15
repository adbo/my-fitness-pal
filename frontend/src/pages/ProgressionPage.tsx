import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api';
import type { ProgressionStatus, ProgressionChain } from '../types';
import ExerciseList from '../components/ExerciseList';
import WorkoutForm from '../components/WorkoutForm';
import ExerciseDetails from '../components/ExerciseDetails';

interface Props {
  username: string;
}

export default function ProgressionPage({ username }: Props) {
  const { chainId } = useParams<{ chainId: string }>();
  const [status, setStatus] = useState<ProgressionStatus | null>(null);
  const [chain, setChain] = useState<ProgressionChain | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'info' } | null>(null);

  useEffect(() => {
    if (chainId) {
      loadData();
    }
  }, [chainId, username]);

  async function loadData() {
    try {
      setLoading(true);
      const [statusData, chainData] = await Promise.all([
        api.getUserProgression(username, chainId!),
        api.getProgression(chainId!),
      ]);
      setStatus(statusData);
      setChain(chainData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRecordWorkout(sets: number, reps: number) {
    if (!chainId) return;

    try {
      const result = await api.recordWorkout(username, chainId, sets, reps);
      setMessage({ text: result.message, type: result.can_progress ? 'success' : 'info' });
      await loadData();
    } catch (err) {
      console.error(err);
    }
  }

  async function handleProgress() {
    if (!chainId) return;

    try {
      const result = await api.advanceProgression(username, chainId);
      setMessage({ text: result.message, type: 'success' });
      await loadData();
    } catch (err: any) {
      setMessage({ text: err.message, type: 'info' });
    }
  }

  async function handleRegress() {
    if (!chainId) return;

    try {
      const result = await api.regressProgression(username, chainId);
      setMessage({ text: result.message, type: 'info' });
      await loadData();
    } catch (err: any) {
      setMessage({ text: err.message, type: 'info' });
    }
  }

  if (loading) {
    return <div className="card">Ładowanie...</div>;
  }

  if (!status || !chain) {
    return <div className="card">Nie znaleziono progresji</div>;
  }

  return (
    <div>
      <Link to="/" className="back-link">
        ← Powrót do listy
      </Link>

      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">{chain.name_pl || chain.name}</h2>
            <p style={{ color: 'var(--gray-500)' }}>{chain.description}</p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div className="stat-value">{status.current_level}/{status.total_levels}</div>
            <div className="stat-label">Poziom</div>
          </div>
        </div>

        <div className="progress-bar" style={{ marginBottom: '1.5rem' }}>
          <div
            className={`progress-fill ${status.can_progress ? 'success' : ''}`}
            style={{ width: `${status.progress_percentage}%` }}
          />
        </div>

        {message && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}

        <div className="stats" style={{ marginBottom: '1.5rem' }}>
          <div className="stat">
            <div className="stat-value">{status.best_sets}</div>
            <div className="stat-label">Najlepsze serie (cel: {status.sets_to_progress})</div>
          </div>
          <div className="stat">
            <div className="stat-value">{status.best_reps}</div>
            <div className="stat-label">Najlepsze powtórzenia (cel: {status.reps_to_progress})</div>
          </div>
          <div className="stat">
            <div className="stat-value">{status.total_workouts_at_level}</div>
            <div className="stat-label">Treningów na tym poziomie</div>
          </div>
        </div>

        <WorkoutForm
          onSubmit={handleRecordWorkout}
          defaultSets={status.current_exercise.default_sets}
          defaultReps={status.current_exercise.default_reps}
        />

        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
          <button
            className="btn btn-success"
            onClick={handleProgress}
            disabled={!status.can_progress}
          >
            Przejdź dalej
          </button>
          <button
            className="btn btn-outline"
            onClick={handleRegress}
            disabled={status.current_level <= 1}
          >
            Cofnij się
          </button>
        </div>
      </div>

      <div className="grid grid-2" style={{ marginTop: '1rem' }}>
        <div className="card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>
            Aktualne ćwiczenie
          </h3>
          <ExerciseDetails exercise={status.current_exercise} />
        </div>

        <div className="card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>
            Wszystkie poziomy
          </h3>
          <ExerciseList
            exercises={chain.exercises}
            currentOrder={status.current_level - 1}
          />
        </div>
      </div>
    </div>
  );
}
