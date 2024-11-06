// frontend/src/pages/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const token = localStorage.getItem('access_token');

  return (
    <div style={styles.container}>
      <h1>Welcome to Compiler as a Service</h1>
      {token ? (
        <Link to="/execute" style={styles.button}>Start Coding</Link>
      ) : (
        <>
          <Link to="/login" style={styles.button}>Login</Link>
          <Link to="/register" style={styles.button}>Register</Link>
        </>
      )}
    </div>
  );
}

const styles = {
  container: {
    textAlign: 'center',
    marginTop: '50px',
  },
  button: {
    display: 'inline-block',
    margin: '10px',
    padding: '10px 20px',
    backgroundColor: '#61dafb',
    color: '#282c34',
    textDecoration: 'none',
    borderRadius: '5px',
  }
};

export default Home;

