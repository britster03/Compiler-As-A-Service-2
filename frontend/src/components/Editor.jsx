// frontend/src/components/Editor.jsx
import React from 'react';
import MonacoEditor from 'react-monaco-editor';

function Editor({ language, code, onChange }) {
  const options = {
    selectOnLineNumbers: true,
    automaticLayout: true,
  };

  return (
    <MonacoEditor
      width="800"
      height="600"
      language={language}
      theme="vs-dark"
      value={code}
      options={options}
      onChange={onChange}
    />
  );
}

export default Editor;

