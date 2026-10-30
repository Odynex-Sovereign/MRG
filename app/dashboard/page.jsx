"use client";

import React, { useState, useEffect } from 'react';

export default function SimulationDashboard() {
  const [streamActive, setStreamActive] = useState(false);
  const [telemetry, setTelemetry] = useState({
    vocal_stress_index: 0,
    tutsa_preemption_compliance: 100,
    prior_art_validation_score: 100,
    generational_continuity_index: 100
  });
  const [macroGrid, setMacroGrid] = useState({
    brent_crude_price_usd: 84.50,
    global_shipping_delay_pct: 22,
    grid_stability_index: 95
  });

  useEffect(() => {
    let ws;
    if (streamActive) {
      ws = new WebSocket("ws://localhost:8000/ws/simulation");
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.telemetry) setTelemetry(prev => ({ ...prev, ...data.telemetry }));
        if (data.macro_economic_grid) setMacroGrid(data.macro_economic_grid);
      };
      
      // Simulate real-time client traffic loop
      const interval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(json.dumps({
            user_id: "dashboard_ui_node",
            session_id: "live_session_01",
            vertical: "Asset-Defense",
            vocal_pitch_variance: Math.random() * 20,
            vocal_energy: Math.random() * 100,
            response_latency_ms: Math.floor(Math.random() * 150),
            user_raw_text: "Enforcing transpacific asset defense protocol safeguards."
          }));
        }
      }, 500);

      return () => {
        clearInterval(interval);
        ws.close();
      };
    }
  }, [streamActive]);

  return (
    <div style={{ backgroundColor: '#0a0f1d', color: '#ffffff', minHeight: '100vh', padding: '2rem', fontFamily: 'sans-serif' }}>
      <header style={{ borderBottom: '1px solid #1f293d', paddingBottom: '1rem', marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 'bold', color: '#00ffcc' }}>ODYNEX AXIS LOGISTICS</h1>
          <p style={{ color: '#9ca3af', fontSize: '0.875rem' }}>MRG Planetary Telemetry Control & Asset Shield</p>
        </div>
        <button 
          onClick={() => setStreamActive(!streamActive)}
          style={{ backgroundColor: streamActive ? '#ef4444' : '#10b981', color: '#fff', border: 'none', padding: '0.75rem 1.5rem', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}
        >
          {streamActive ? "DISCONNECT GRID" : "INITIALIZE SIMULATION CORE"}
        </button>
      </header>

      <main style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        {/* Left Column: Local Biometric Metrics */}
        <section style={{ backgroundColor: '#111827', border: '1px solid #1f293d', padding: '1.5rem', borderRadius: '8px' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', color: '#38bdf8' }}>Institutional Compliance Telemetry</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                <span>Vocal Stress Index</span>
                <span style={{ color: telemetry.vocal_stress_index > 60 ? '#ef4444' : '#00ffcc' }}>{telemetry.vocal_stress_index}%</span>
              </div>
              <div style={{ width: '100%', backgroundColor: '#1f293d', height: '8px', borderRadius: '4px' }}>
                <div style={{ width: `${telemetry.vocal_stress_index}%`, backgroundColor: telemetry.vocal_stress_index > 60 ? '#ef4444' : '#00ffcc', height: '100%', borderRadius: '4px', transition: 'width 0.3s ease' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                <span>TUTSA Preemption Compliance</span>
                <span>{telemetry.tutsa_preemption_compliance}%</span>
              </div>
              <div style={{ width: '100%', backgroundColor: '#1f293d', height: '8px', borderRadius: '4px' }}>
                <div style={{ width: `${telemetry.tutsa_preemption_compliance}%`, backgroundColor: '#38bdf8', height: '100%', borderRadius: '4px' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                <span>Prior Art Validation Score</span>
                <span>{telemetry.prior_art_validation_score}%</span>
              </div>
              <div style={{ width: '100%', backgroundColor: '#1f293d', height: '8px', borderRadius: '4px' }}>
                <div style={{ width: `${telemetry.prior_art_validation_score}%`, backgroundColor: '#a855f7', height: '100%', borderRadius: '4px' }}></div>
              </div>
            </div>
          </div>
        </section>

        {/* Right Column: Global Macro-Economic Grid Data */}
        <section style={{ backgroundColor: '#111827', border: '1px solid #1f293d', padding: '1.5rem', borderRadius: '8px' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', color: '#fbbf24' }}>Systemic Macro-Economic Feed</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div style={{ backgroundColor: '#1f293d', padding: '1rem', borderRadius: '6px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.875rem', color: '#9ca3af' }}>Brent Crude Price</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', marginTop: '0.5rem', color: '#fbbf24' }}>${macroGrid.brent_crude_price_usd.toFixed(2)}</div>
            </div>
            <div style={{ backgroundColor: '#1f293d', padding: '1rem', borderRadius: '6px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.875rem', color: '#9ca3af' }}>Global Shipping Delay</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', marginTop: '0.5rem', color: '#f87171' }}>{macroGrid.global_shipping_delay_pct}%</div>
            </div>
            <div style={{ backgroundColor: '#1f293d', padding: '1rem', borderRadius: '6px', textAlign: 'center', gridColumn: 'span 2' }}>
              <div style={{ fontSize: '0.875rem', color: '#9ca3af' }}>Global Grid Stability Index</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', marginTop: '0.5rem', color: '#10b981' }}>{macroGrid.grid_stability_index}%</div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
