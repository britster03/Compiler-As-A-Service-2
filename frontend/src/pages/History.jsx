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
    <div style={styles.container}>
      <h2>Execution History</h2>
      <div style={styles.historyContainer}>
        <ul style={styles.list}>
          {executions.map((exec) => (
            <li key={exec.id} onClick={() => handleSelect(exec)} style={styles.listItem}>
              <strong>{exec.language}</strong> - {new Date(exec.created_at).toLocaleString()}
            </li>
          ))}
        </ul>
        {selected && (
          <div style={styles.details}>
            <h3>Details</h3>
            <p><strong>Language:</strong> {selected.language}</p>
            <p><strong>Code:</strong></p>
            <pre style={styles.pre}>{selected.code}</pre>
            {selected.output && (
              <>
                <p><strong>Output:</strong></p>
                <pre style={styles.pre}>{selected.output}</pre>
              </>
            )}
            {selected.error && (
              <>
                <p><strong>Error:</strong></p>
                <pre style={styles.pre}>{selected.error}</pre>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '900px',
    margin: '20px auto',
    textAlign: 'left',
  },
  historyContainer: {
    display: 'flex',
  },
  list: {
    listStyle: 'none',
    padding: 0,
    width: '30%',
    borderRight: '1px solid #ccc',
    maxHeight: '600px',
    overflowY: 'scroll',
  },
  listItem: {
    padding: '10px',
    cursor: 'pointer',
    borderBottom: '1px solid #eee',
  },
  details: {
    padding: '10px',
    width: '70%',
  },
  pre: {
    backgroundColor: '#f0f0f0',
    padding: '10px',
    overflowX: 'auto',
  }
};

export default History;

