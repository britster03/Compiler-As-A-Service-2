// frontend/src/pages/History.jsx
import React, { useEffect, useState } from 'react';
import api from '../services/api';

function History() {
  const [executions, setExecutions] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get('/execute/history');
        setExecutions(response.data);
      } catch (err) {
        console.error('Failed to fetch history.');
      }
    };
    fetchHistory();
  }, []);

  const handleSelect = (exec) => {
    setSelected(exec);
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Execution History</h2>
      <div className="flex flex-col md:flex-row">
        <div className="md:w-1/3">
          <ul className="border border-gray-300 rounded">
            {executions.map((exec) => (
              <li
                key={exec.id}
                onClick={() => handleSelect(exec)}
                className="p-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100"
              >
                <span className="font-semibold">{exec.language}</span> - {new Date(exec.created_at).toLocaleString()}
              </li>
            ))}
          </ul>
        </div>
        <div className="md:w-2/3 md:pl-4 mt-4 md:mt-0">
          {selected ? (
            <div className="p-4 border border-gray-300 rounded">
              <h3 className="text-xl font-bold mb-2">Details</h3>
              <p><span className="font-semibold">Language:</span> {selected.language}</p>
              <p className="mt-2"><span className="font-semibold">Code:</span></p>
              <pre className="bg-gray-100 p-2 rounded overflow-auto">{selected.code}</pre>
              {selected.output && (
                <div className="mt-2">
                  <p className="font-semibold">Output:</p>
                  <pre className="bg-gray-100 p-2 rounded overflow-auto">{selected.output}</pre>
                </div>
              )}
              {selected.error && (
                <div className="mt-2">
                  <p className="font-semibold text-red-700">Error:</p>
                  <pre className="bg-red-100 p-2 rounded overflow-auto text-red-700">{selected.error}</pre>
                </div>
              )}
            </div>
          ) : (
            <p>Select an execution from the history to view details.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default History;
