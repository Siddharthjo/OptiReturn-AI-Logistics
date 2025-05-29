import { Routes, Route } from 'react-router-dom';
import Signup from './components/LoginSignup/Signup.jsx';
import Login from './components/LoginSignup/Login.jsx';
import MainDashboard from './Pages/MainDashboard.jsx';
import Predict from './pages/Predict.jsx';
import ResalePredict from './Pages/ResalePredict.jsx';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<MainDashboard />} />
      <Route path="/predict" element={<Predict />} />
      <Route path="/resale" element={<ResalePredict />} />
    </Routes>
  );
}

export default App;