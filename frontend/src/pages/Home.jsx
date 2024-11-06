// frontend/src/pages/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const token = localStorage.getItem('access_token');

  return (
    <div className="container mx-auto text-center mt-10">
      <h1 className="text-4xl font-bold mb-6">Welcome to Compiler as a Service</h1>
      {token ? (
        <Link to="/execute" className="bg-blue-500 text-white px-6 py-3 rounded-md hover:bg-blue-600">
          Start Coding
        </Link>
      ) : (
        <div>
          <Link to="/login" className="bg-blue-500 text-white px-6 py-3 rounded-md hover:bg-blue-600 mr-4">
            Login
          </Link>
          <Link to="/register" className="bg-green-500 text-white px-6 py-3 rounded-md hover:bg-green-600">
            Register
          </Link>
        </div>
      )}
    </div>
  );
}

export default Home;
