// frontend/src/components/Navbar.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  return (
    <nav style={styles.nav}>
      <h2 style={styles.title}>Compiler as a Service</h2>
      <div>
        {token ? (
          <>
            <Link to="/execute" style={styles.link}>Execute</Link>
            <Link to="/history" style={styles.link}>History</Link>
            <button onClick={handleLogout} style={styles.button}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={styles.link}>Login</Link>
            <Link to="/register" style={styles.link}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    padding: '10px 20px',
    backgroundColor: '#282c34',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    color: 'white'
  },
  title: {
    margin: 0,
  },
  link: {
    marginRight: '15px',
    color: 'white',
    textDecoration: 'none',
  },
  button: {
    padding: '5px 10px',
    cursor: 'pointer',
  }
};

export default Navbar;

