"use client";

import React, { useState } from 'react';

export default function PricingPage() {
  const [loadingTier, setLoadingTier] = useState(null);
  const userId = "dashboard_ui_node"; // Derived dynamically from auth state in production

  const tiers = [
    {
      id: "academic",
      name: "Academic Core",
      price: "$19",
      period: "student / month",
      priceId: "price_1AcademicStudentTier2026",
      features: [
        "Higher-Ed & Youth Focus Modules",
        "Rhetorical Defense Tracking",
        "Peer Pressure Resistance Telemetry",
        "Automated PDF Performance Card Reports"
      ],
      buttonText: "Launch Student Pass",
      color: "#00ffcc"
    },
    {
      id: "enterprise",
      name: "Enterprise Crucible",
      price: "$4,500",
      period: "month (flat up to 50 seats)",
      priceId: "price_1EnterpriseCrucibleTier2026",
      features: [
        "Corporate, Military, & Geopolitical Portals",
        "TUTSA & WTO Compliance Registry Mapping",
        "Dedicated Fly.io High-Priority Micro-VM Routing",
        "Advanced Multi-Agent Coordination Analytics"
      ],
      buttonText: "Deploy Enterprise Grid",
      color: "#38bdf8"
    },
    {
      id: "developer",
      name: "Developer API Key",
      price: "$0.12",
      period: "simulation minute",
      priceId: "price_1DeveloperAPIUsageTier2026",
      features: [
        "Direct Programmatic Key Authentication",
        "Raw Audio2Face & Nemotron-4 NIM Stream Access",
        "Decentralized Video Egress Channels via Livepeer",
        "Custom OpenUSD Asset Pipeline Injection"
      ],
      buttonText: "Provision API Credentials",
      color: "#a855f7"
    }
  ];

  const handleSubscriptionInit = async (priceId, tierId) => {
    setLoadingTier(tierId);
    try {
      const response = await fetch("/api/billing/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, price_id: priceId })
      });
      const data = await response.json();
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        alert("Failed to initialize billing routing.");
      }
    } catch (err) {
      console.error("Billing interface exception:", err);
    } finally {
      setLoadingTier(null);
    }
  };

  return (
    <div style={{ backgroundColor: '#0a0f1d', color: '#ffffff', minHeight: '100vh', padding: '3rem 2rem', fontFamily: 'sans-serif' }}>
      <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#00ffcc', marginBottom: '0.5rem' }}>ODYNEX AXIS LOGISTICS LLC</h1>
        <p style={{ color: '#9ca3af', fontSize: '1.1rem' }}>Sovereign-Grade Simulation Grid Commercial Licensing</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
        {tiers.map((tier) => (
          <div key={tier.id} style={{ backgroundColor: '#111827', border: `1px solid #1f293d`, borderTop: `4px solid ${tier.color}`, padding: '2rem', borderRadius: '8px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ffffff', marginBottom: '1rem' }}>{tier.name}</h2>
              <div style={{ display: 'flex', alignItems: 'baseline', marginBottom: '2rem' }}>
                <span style={{ fontSize: '3rem', fontWeight: 'bold', color: tier.color }}>{tier.price}</span>
                <span style={{ color: '#9ca3af', marginLeft: '0.5rem', fontSize: '0.875rem' }}>/ {tier.period}</span>
              </div>
              <ul style={{ listStyleType: 'none', padding: 0, margin: '0 0 2rem 0', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {tier.features.map((feat, idx) => (
                  <li key={idx} style={{ color: '#d1d5db', fontSize: '0.9rem', display: 'flex', alignItems: 'center' }}>
                    <span style={{ color: tier.color, marginRight: '0.5rem', fontWeight: 'bold' }}>✓</span> {feat}
                  </li>
                ))}
              </ul>
            </div>
            <button
              onClick={() => handleSubscriptionInit(tier.priceId, tier.id)}
              disabled={loadingTier !== null}
              style={{ backgroundColor: tier.color, color: '#0a0f1d', border: 'none', width: '100%', padding: '1rem', borderRadius: '4px', fontWeight: 'bold', fontSize: '1rem', cursor: 'pointer', transition: 'opacity 0.2s' }}
            >
              {loadingTier === tier.id ? "PROVISIONING CHANNEL..." : tier.buttonText}
            </button>
          </div>
        ))}
      </div>
    </div>
);
}
