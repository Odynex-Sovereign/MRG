"use client";

import React, { useState, useEffect } from 'react';

export default function SimulationDashboard() {
  const [streamActive, setStreamActive] = useState(false);
  const [telemetry, setTelemetry] = useState({
    vocal_stress_index: 0,
    tutsa_preemption_compliance: 100,
    prior_art_validation_score: 100,
    generational_continuity_index: 100,
  });

  const [macroGrid, setMacroGrid] = useState({
    brent_crude_price_usd: 84.5,
    global_shipping_delay_pct: 22,
    grid_stability_index: 95,
  });

  useEffect(() => {
    if (!streamActive) return undefined;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/api/simulation/stream`;
    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.telemetry) setTelemetry(prev => ({ ...prev, ...data.telemetry }));
        if (data.macroGrid) setMacroGrid(prev => ({ ...prev, ...data.macroGrid }));
      } catch (err) {
        console.error("Failed parsing telemetry payload:", err);
      }
    };

    return () => ws.close();
  }, [streamActive]);

  return (
    <div style={{ padding: '2rem', background: '#0f172a', color: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ marginBottom: '2rem', borderBottom: '1px solid #334155' }}>
        <h1>Simulation Telemetry Desk</h1>
      </header>
      <button onClick={() => setStreamActive(!streamActive)} style={{ background: streamActive ? '#ef4444' : '#10b981', color: '#fff', padding: '0.75rem 1.5rem', border: 'none', borderRadius: '0.375rem', cursor: 'pointer' }}>
        {streamActive ? 'Disconnect Grid Stream' : 'Initialize Live Simulation Stream'}
      </button>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '2rem' }}>
        <section style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '0.5rem' }}>
          <h3>Biometric & Performance Vectors</h3>
          <p>Vocal Stress Index: {telemetry.vocal_stress_index}%</p>
          <p>Grid Stability Index: {macroGrid.grid_stability_index}%</p>
        </section>
      </div>
    </div>
  );
}
