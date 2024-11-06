// frontend/src/components/Editor.jsx
import React from 'react';
import MonacoEditor from 'react-monaco-editor';

function Editor({ language, code, onChange }) {
  const options = {
    selectOnLineNumbers: true,
    automaticLayout: true,
    minimap: { enabled: false },
    fontSize: 14,
  };

  return (
    <div className="my-4">
      <MonacoEditor
        width="100%"
        height="500"
        language={language}
        theme="vs-dark"
        value={code}
        options={options}
        onChange={onChange}
      />
    </div>
  );
}

export default Editor;
