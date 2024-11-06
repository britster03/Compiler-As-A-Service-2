// frontend/src/pages/Login.jsx
import React, { useState } from 'react';
import api from '../services/api';
import { useNavigate, Link } from 'react-router-dom';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/login', { email, password });
      localStorage.setItem('access_token', response.data.access_token);
      navigate('/execute');
    } catch (err) {
      setError(err.response.data.error || 'Login failed.');
    }
  };

  return (
    <div style={styles.container}>
      <h2>Login</h2>
      {error && <p style={styles.error}>{error}</p>}
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={styles.input}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={styles.input}
        />
        <button type="submit" style={styles.button}>Login</button>
      </form>
      <p>Don't have an account? <Link to="/register">Register here.</Link></p>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '400px',
    margin: '50px auto',
    textAlign: 'center',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    marginTop: '20px',
  },
  input: {
    padding: '10px',
    margin: '10px 0',
    fontSize: '16px',
  },
  button: {
    padding: '10px',
    backgroundColor: '#61dafb',
    border: 'none',
    cursor: 'pointer',
    fontSize: '16px',
  },
  error: {
    color: 'red',
  }
};

export default Login;

