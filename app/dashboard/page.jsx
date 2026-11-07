"use client";

import React, { useState, useEffect } from 'react';

export default function SimulationDashboard() {
  const [streamActive, setStreamActive] = useState(false);
  const [telemetry, setTelemetry] = useState({ vocal_stress_index: 0 });

  useEffect(() => {
    if (!streamActive) return undefined;
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/api/simulation/stream`);
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.telemetry) setTelemetry({ vocal_stress_index: data.telemetry.vocal_stress_index });
    };
    return () => ws.close();
  }, [streamActive]);

  return (
    <div style={{ padding: '2rem', background: '#0f172a', color: '#f8fafc', minHeight: '100vh' }}>
      <h1>Simulation Telemetry Desk</h1>
      <button onClick={() => setStreamActive(!streamActive)} style={{ background: streamActive ? '#ef4444' : '#10b981', color: '#fff', padding: '0.75rem 1.5rem', border: 'none', borderRadius: '0.375rem', cursor: 'pointer' }}>
        {streamActive ? 'Disconnect Grid' : 'Connect Grid'}
      </button>
      <div style={{ marginTop: '2rem', background: '#1e293b', padding: '1rem', borderRadius: '0.5rem', maxWidth: '300px' }}>
        <h3>Metrics Core</h3>
        <p>Vocal Stress Index: {telemetry.vocal_stress_index}%</p>
      </div>
    </div>
  );
}
