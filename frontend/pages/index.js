import { useState } from 'react';

export default function Home() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [level, setLevel] = useState('beginner');
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(false);

  const explainCode = async () => {
    if (!code.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language, level })
      });
      
      const result = await response.json();
      setExplanation(result);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>AI Code Explainer</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your code here..."
          style={{ width: '100%', height: '200px', padding: '10px' }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>
        
        <select value={level} onChange={(e) => setLevel(e.target.value)} style={{ marginLeft: '10px' }}>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="expert">Expert</option>
        </select>
        
        <button onClick={explainCode} disabled={loading} style={{ marginLeft: '10px', padding: '10px 20px' }}>
          {loading ? 'Explaining...' : 'Explain Code'}
        </button>
      </div>

      {explanation && (
        <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '5px' }}>
          <h2>Explanation</h2>
          <p><strong>Summary:</strong> {explanation.summary}</p>
          
          <h3>Walkthrough</h3>
          <ul>
            {explanation.walkthrough.map((step, i) => <li key={i}>{step}</li>)}
          </ul>
          
          <h3>Key Concepts</h3>
          <ul>
            {explanation.concepts.map((concept, i) => <li key={i}>{concept}</li>)}
          </ul>
          
          {explanation.gotchas.length > 0 && (
            <>
              <h3>Gotchas</h3>
              <ul>
                {explanation.gotchas.map((gotcha, i) => <li key={i}>{gotcha}</li>)}
              </ul>
            </>
          )}
          
          {explanation.improvements.length > 0 && (
            <>
              <h3>Improvements</h3>
              <ul>
                {explanation.improvements.map((improvement, i) => <li key={i}>{improvement}</li>)}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}