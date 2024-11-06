// frontend/src/pages/Execute.jsx

import React, { useState } from 'react';
import Editor from '../components/Editor';
import api from '../services/api';

function Execute() {
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');

  const handleExecute = async () => {
    try {
      const response = await api.post('/execute/', { language, code });
      setOutput(response.data.output || '');
      setError(response.data.error || '');
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Execution failed.';
      setError(errorMsg);
      setOutput('');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Execute Code</h2>
      <div className="mb-4">
        <label className="block text-gray-700 mb-2">Language:</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded"
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          {/* Add more languages as needed */}
        </select>
      </div>
      <Editor language={language} code={code} onChange={setCode} />
      <button
        onClick={handleExecute}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Run
      </button>
      {output && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h3 className="font-bold">Output:</h3>
          <pre className="whitespace-pre-wrap">{output}</pre>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 bg-red-100 rounded">
          <h3 className="font-bold text-red-700">Error:</h3>
          <pre className="whitespace-pre-wrap text-red-700">{error}</pre>
        </div>
      )}
    </div>
  );
}

export default Execute;
