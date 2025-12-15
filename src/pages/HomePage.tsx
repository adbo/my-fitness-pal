import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PROGRESSIONS } from '../data/exercises';
import { getAllUserProgress, getProgressionStatus } from '../firebase/progressService';
import type { ProgressionStatus } from '../types';
import ProgressCard from '../components/ProgressCard';

interface Props {
  userId: string;
}

export default function HomePage({ userId }: Props) {
  const [statuses, setStatuses] = useState<ProgressionStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProgressions();
  }, [userId]);

  async function loadProgressions() {
    try {
      setLoading(true);
      const progressList = await getAllUserProgress(userId);

      const statusList = PROGRESSIONS.map((chain, index) => {
        return getProgressionStatus(chain, progressList[index]);
      });

      setStatuses(statusList);
    } catch (err) {
      setError('Nie udało się załadować danych. Sprawdź konfigurację Firebase.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="card">Ładowanie...</div>;
  }

  if (error) {
    return <div className="card message">{error}</div>;
  }

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem' }}>Twoje Progresje</h2>

      <div className="grid grid-2">
        {statuses.map((status) => (
          <Link
            key={status.chain.id}
            to={`/progression/${status.chain.id}`}
            style={{ textDecoration: 'none', color: 'inherit' }}
          >
            <ProgressCard status={status} />
          </Link>
        ))}
      </div>
    </div>
  );
}
