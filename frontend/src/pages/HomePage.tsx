import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api';
import type { ProgressionStatus } from '../types';
import ProgressCard from '../components/ProgressCard';

interface Props {
  username: string;
}

export default function HomePage({ username }: Props) {
  const [progressions, setProgressions] = useState<ProgressionStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProgressions();
  }, [username]);

  async function loadProgressions() {
    try {
      setLoading(true);
      const data = await api.getUserProgressions(username);
      setProgressions(data);
    } catch (err) {
      setError('Nie udało się załadować danych');
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
        {progressions.map((prog) => (
          <Link
            key={prog.chain_id}
            to={`/progression/${prog.chain_id}`}
            style={{ textDecoration: 'none', color: 'inherit' }}
          >
            <ProgressCard progression={prog} />
          </Link>
        ))}
      </div>
    </div>
  );
}
