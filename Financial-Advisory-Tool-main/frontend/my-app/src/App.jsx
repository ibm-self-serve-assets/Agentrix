import React, { useState, useRef } from 'react';
import { TextArea, Button } from '@carbon/react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './App.css';

function AiToolPage() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  // Create a ref to store the AbortController
  const abortControllerRef = useRef(null);

  const fetchReport = async (text) => {
    setLoading(true);
    setOutput('');
    // Create a new AbortController for this request
    abortControllerRef.current = new AbortController();
    try {
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: text,
        signal: abortControllerRef.current.signal, // Attach the signal here
      });
      if (!response.ok) {
        throw new Error('API error');
      }
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      let accumulated = '';
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        if (value) {
          const chunk = decoder.decode(value);
          accumulated += chunk;
          setOutput(accumulated);
        }
        done = doneReading;
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        // Fetch was aborted, do not show error
        setOutput('');
      } else {
        setOutput('**Error:** Unable to fetch report.');
      }
    }
    setLoading(false);
  };

  const handleResultClick = () => {
    if (input.trim()) fetchReport(input);
  };

  const handleReset = () => {
    // Abort the ongoing fetch if any
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setInput('');
    setOutput('');
    setLoading(false);
  };


  return (
    <div
      style={{
        minHeight: '100vh',
        width: '100vw',
        backgroundImage: 'url("/image.png")',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center center',
        backgroundSize: 'cover',
        backgroundAttachment: 'fixed', // This keeps the image fixed
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        color: '#000',
        position: 'relative',
  }}
>
      {/* Title at the top */}
      <h1 style={{
        marginTop: 160,
        marginBottom: 20,
        fontWeight: 700,
        fontSize: 70,
        textAlign: 'center',
        width: '100%',
        color: '#fff',
        textShadow: '0 2px 8px #000',
        zIndex: 2,
      }}>
        Financial Advisory Tool
      </h1>
      {/* Main content */}
      <div
        style={{
          position: 'relative',
          zIndex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          width: '100%',
          maxWidth: 1200,
          margin: '0 auto',
          padding: 32,
        }}
      >
        <div style={{ width: '100%' }}>
          <TextArea
            id="ai-tool-input"
            placeholder={
    "Hello, I'm Priya from Mumbai. My monthly income is 1.8 Lacs and my expenses are about 70K. I'm interested in building wealth over the next 10 years and can take moderate risks. Please suggest a good investment plan.\n\n" +
    "Hi, I'm Rajesh, a 40-year-old from Delhi. I earn 3 Lacs per month and spend about 1.2 Lacs. I want to save for my children's education and my retirement. I prefer safe and tax-saving investments."
  }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={!!output}
            style={{
              width: '100%',
              minHeight: 180,
              marginBottom: 20,
              fontSize: 18,
              background: 'rgba(255,255,255,0.85)',
              color: '#000',
              border: 'none',
              borderRadius: 12,
              boxShadow: '0 4px 16px #0002',
              resize: 'vertical',
              padding: '28px 28px',
              boxSizing: 'border-box'
            }}
          />
          <div style={{
            display: 'flex',
            gap: 12,
            justifyContent: 'center',
            width: '100%',
            marginTop: 8,
          }}>
            {!output && (
              <Button kind="primary" onClick={handleResultClick} disabled={loading || !input.trim()}>
                Generate Report
              </Button>
            )}
            {output && (
              <>
                <Button kind="primary" disabled>
                  Generate Report
                </Button>
                <Button kind="secondary" onClick={handleReset}>
                  Reset
                </Button>
              </>
            )}
          </div>
        </div>
        {/* No loading message block here */}
        {output && (
          <div
            className="markdown-body"
            style={{
              marginTop: 32,
              background: 'rgba(255,255,255,0.95)',
              padding: 32,
              borderRadius: 12,
              width: '100%',
              maxWidth: 1200,
              color: '#000',
              overflowX: 'auto',
              boxSizing: 'border-box'
            }}
          >
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {output}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}

export default AiToolPage;
