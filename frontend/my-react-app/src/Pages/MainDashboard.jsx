import React from 'react';
import { useNavigate } from 'react-router-dom';
import './MainDashboard.css';

const MainDashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="dashboard-wrapper">
      <header className="dashboard-header">
        <h1>OptiReturn</h1>
        <p>AI-Powered Reverse Logistics for Smarter Returns</p>
      </header>

      <div className="dashboard-container">
        <div className="about-section">
          <p>
            OptiReturn is an intelligent reverse logistics platform that helps e-commerce businesses reduce costs,
            detect returns, and maximize resale profits — all powered by AI.
          </p>
        </div>

        <div className="feature-buttons">
          <button className="feature-btn" onClick={() => navigate('/predict')}>
            📦 Return Prediction
          </button>
          <button className="feature-btn" onClick={() => navigate('/resale')}>
            💰 Resale Estimation
          </button>
        </div>
      </div>
    </div>
  );
};

export default MainDashboard;