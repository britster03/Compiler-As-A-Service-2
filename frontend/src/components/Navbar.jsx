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
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-xl font-bold">CaaS</Link>
        <div>
          {token ? (
            <>
              <Link to="/execute" className="text-gray-300 hover:text-white px-3">Execute</Link>
              <Link to="/history" className="text-gray-300 hover:text-white px-3">History</Link>
              <button onClick={handleLogout} className="text-gray-300 hover:text-white px-3">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-gray-300 hover:text-white px-3">Login</Link>
              <Link to="/register" className="text-gray-300 hover:text-white px-3">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
