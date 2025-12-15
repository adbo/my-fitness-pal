import { Routes, Route, Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import HomePage from './pages/HomePage';
import ProgressionPage from './pages/ProgressionPage';

const USERNAME = 'default_user';

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
          <Route path="/" element={<HomePage username={USERNAME} />} />
          <Route path="/progression/:chainId" element={<ProgressionPage username={USERNAME} />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
