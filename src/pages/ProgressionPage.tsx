import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProgression } from '../data/exercises';
import {
  getUserProgress,
  recordWorkout,
  advanceProgress,
  regressProgress,
  getProgressionStatus,
} from '../firebase/progressService';
import type { ProgressionStatus } from '../types';
import { SETS_TO_PROGRESS, REPS_TO_PROGRESS } from '../types';
import ExerciseList from '../components/ExerciseList';
import WorkoutForm from '../components/WorkoutForm';
import ExerciseDetails from '../components/ExerciseDetails';

interface Props {
  userId: string;
}

export default function ProgressionPage({ userId }: Props) {
  const { chainId } = useParams<{ chainId: string }>();
  const [status, setStatus] = useState<ProgressionStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'info' } | null>(null);

  useEffect(() => {
    if (chainId) {
      loadData();
    }
  }, [chainId, userId]);

  async function loadData() {
    if (!chainId) return;

    try {
      setLoading(true);
      const chain = getProgression(chainId);
      if (!chain) {
        setLoading(false);
        return;
      }

      const progress = await getUserProgress(userId, chainId);
      setStatus(getProgressionStatus(chain, progress));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRecordWorkout(sets: number, reps: number) {
    if (!chainId) return;

    try {
      const result = await recordWorkout(userId, chainId, sets, reps);
      setMessage({ text: result.message, type: result.canProgress ? 'success' : 'info' });
      await loadData();
    } catch (err) {
      console.error(err);
    }
  }

  async function handleProgress() {
    if (!chainId) return;

    try {
      const result = await advanceProgress(userId, chainId);
      if (result.success) {
        setMessage({ text: result.message, type: 'success' });
        await loadData();
      } else {
        setMessage({ text: result.message, type: 'info' });
      }
    } catch (err: any) {
      setMessage({ text: err.message, type: 'info' });
    }
  }

  async function handleRegress() {
    if (!chainId) return;

    try {
      const result = await regressProgress(userId, chainId);
      if (result.success) {
        setMessage({ text: result.message, type: 'info' });
        await loadData();
      } else {
        setMessage({ text: result.message, type: 'info' });
      }
    } catch (err: any) {
      setMessage({ text: err.message, type: 'info' });
    }
  }

  if (loading) {
    return <div className="card">Ładowanie...</div>;
  }

  if (!status) {
    return <div className="card">Nie znaleziono progresji</div>;
  }

  const currentLevel = status.progress.current_order + 1;
  const totalLevels = status.chain.exercises.length;

  return (
    <div>
      <Link to="/" className="back-link">
        ← Powrót do listy
      </Link>

      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">{status.chain.name_pl || status.chain.name}</h2>
            <p style={{ color: 'var(--gray-500)' }}>{status.chain.description}</p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div className="stat-value">{currentLevel}/{totalLevels}</div>
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
            <div className="stat-value">{status.progress.best_sets}</div>
            <div className="stat-label">Najlepsze serie (cel: {SETS_TO_PROGRESS})</div>
          </div>
          <div className="stat">
            <div className="stat-value">{status.progress.best_reps}</div>
            <div className="stat-label">Najlepsze powtórzenia (cel: {REPS_TO_PROGRESS})</div>
          </div>
          <div className="stat">
            <div className="stat-value">{status.progress.workouts_at_level}</div>
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
            disabled={currentLevel <= 1}
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
            exercises={status.chain.exercises}
            currentOrder={status.progress.current_order}
          />
        </div>
      </div>
    </div>
  );
}
