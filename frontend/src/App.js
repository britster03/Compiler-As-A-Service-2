// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Execute from './pages/Execute';
import History from './pages/History';

function App() {
  return (
    <Router>
      <Navbar />
      <div style={styles.container}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/execute" element={<ProtectedRoute component={Execute} />} />
          <Route path="/history" element={<ProtectedRoute component={History} />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

// Protected Route Component
function ProtectedRoute({ component: Component }) {
  const token = localStorage.getItem('access_token');
  return token ? <Component /> : <Login />;
}

const styles = {
  container: {
    padding: '20px',
  }
};

export default App;
