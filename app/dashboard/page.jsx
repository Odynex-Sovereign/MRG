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

    ws.onerror = (error) => console.error("Simulation grid socket failure:", error);
    ws.onclose = () => setStreamActive(false);

    return () => {
      ws.close();
    };
  }, [streamActive]);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', background: '#0f172a', color: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ marginBottom: '2rem', borderBottom: '1px solid #334155', paddingBottom: '1rem' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 'bold' }}>Simulation Telemetry Desk</h1>
        <p style={{ color: '#94a3b8' }}>Live interactive digital-twin executive composure metrics.</p>
      </header>

      <div style={{ marginBottom: '2rem' }}>
        <button 
          onClick={() => setStreamActive(!streamActive)} 
          style={{
            background: streamActive ? '#ef4444' : '#10b981',
            color: '#fff',
            border: 'none',
            padding: '0.75rem 1.5rem',
            borderRadius: '0.375rem',
            cursor: 'pointer',
            fontWeight: '600'
          }}
        >
          {streamActive ? 'Disconnect Grid Stream' : 'Initialize Live Simulation Stream'}
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <section style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '0.5rem' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: '#38bdf8' }}>Biometric & Performance Vectors</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ margin: '0.5rem 0' }}>Vocal Stress Index: <strong>{telemetry.vocal_stress_index}%</strong></li>
            <li style={{ margin: '0.5rem 0' }}>Preemption Compliance: <strong>{telemetry.tutsa_preemption_compliance}%</strong></li>
            <li style={{ margin: '0.5rem 0' }}>Prior Art Validation: <strong>{telemetry.prior_art_validation_score}</strong></li>
            <li style={{ margin: '0.5rem 0' }}>Generational Continuity Index: <strong>{telemetry.generational_continuity_index}%</strong></li>
          </ul>
        </section>

        <section style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '0.5rem' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: '#fbbf24' }}>Macroeconomic Parameters</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ margin: '0.5rem 0' }}>Brent Crude Pricing: <strong>${macroGrid.brent_crude_price_usd} USD</strong></li>
            <li style={{ margin: '0.5rem 0' }}>Global Shipping Lag: <strong>{macroGrid.global_shipping_delay_pct}%</strong></li>
            <li style={{ margin: '0.5rem 0' }}>Grid Stability Index: <strong>{macroGrid.grid_stability_index}%</strong></li>
          </ul>
        </section>
      </div>
    </div>
  );
}
