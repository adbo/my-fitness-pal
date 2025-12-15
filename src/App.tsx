import { Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ProgressionPage from './pages/ProgressionPage';

// Simple user ID - in production use Firebase Auth
const USER_ID = 'default_user';

function App() {
  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <Link to="/" style={{ textDecoration: 'none' }}>
            <h1>My Fitness Pal</h1>
          </Link>
        </div>
      </header>

      <main className="container">
        <Routes>
          <Route path="/" element={<HomePage userId={USER_ID} />} />
          <Route path="/progression/:chainId" element={<ProgressionPage userId={USER_ID} />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
