# MRG: The Integrated Simulation Suite

[![License: MPL 2.0](https://shields.io)](LICENSE)
[![NVIDIA Stack](https://shields.io)](NVIDIA_STACK.md)
[![Built with FastAPI](https://shields.io)](https://tiangolo.com)

**MRG** is an enterprise-grade, planet-scale crisis simulation grid powered by the NVIDIA Omniverse stack and DeepSeek-V3. It replaces linear training models with high-stakes, interactive digital twins that test executive composure, tactical decision-making, and compliance defense under intense conversational stress.
## 🚀 Key Features

*   **Sub-100ms Response Pipeline:** Containerized microservice orchestration ensures natural human-to-digital interactions with no structural conversational lag.
*   **Emotionally Nuanced Audio Synthesis:** Real-time translation and voice generation capable of mimicking physical strain, interruptions, and aggressive tonal shifts.
*   **Automated Micro-Expressions:** High-fidelity 3D meshes respond directly to vocal cadence, rendering subtle tells like sneers and physiological stress behaviors.
*   **Omnichannel Pixel Streaming:** Powered by WebRTC to deliver real-time rendering directly to lightweight laptops, rugged industrial tablets, or remote field devices.

## 🏗️ Architecture & NVIDIA Core Integration

MRG abstracts the complexity of advanced conversational AI and graphics delivery into a synchronized infrastructure:
┌─────────────────┐       ┌────────────────────────┐       ┌─────────────────────────┐
│   NVIDIA ACE    │ ───►  │    NVIDIA Riva ASR     │ ───►  │   Audio2Face/Gesture    │
│ (NIMs Pipeline) │       │ (ASR/TTS Translation)  │       │  (3D Mesh Mesh-Mapping) │
└─────────────────┘       └────────────────────────┘       └─────────────────────────┘
│
┌─────────────────┐       ┌────────────────────────┐                    ▼
│  Field Devices  │ ◄───  │  NVIDIA GDN Streaming  │ ◄──────────────────┘
│ (WebRTC Clients)│       │  (Centralized Cloud)   │
└─────────────────┘       └────────────────────────┘
1.  **NVIDIA ACE & Inference Microservices (NIMs):** Low-latency routing and model pipeline deployment.
2.  **NVIDIA Riva ASR/TTS:** Real-time verbal inference matched with emotionally dynamic voice synthesis.
3.  **NVIDIA Audio2Face & Audio2Gesture:** Automated procedural animation mapped directly onto skeletal meshes.
4.  **NVIDIA Graphics Delivery Network (GDN):** Centralized cloud streaming layer minimizing hardware dependencies on client endpoints.
## 🏢 Sector Verticals & Simulation Personas

MRG includes pre-configured, production-tested vertical scenarios assessing unique telemetry targets:

### 1. Corporate & Executive Governance
*   **Persona:** Victoria Vance (The Activist Investor)
*   **Scenario:** Boardroom crisis involving real-time hostile data breach response.
*   **Core Telemetry:** Logic Consistency, Strategic Evasion, Vocal Gravitas.

### 2. Political & Media Relations
*   **Persona:** Marcus Brody (The Hostile Journalist)
*   **Scenario:** Press room triage with live, high-pressure television grilling.
*   **Core Telemetry:** News Bridging Success, Filler Word Reduction, Composure.

### 3. Healthcare & De-Escalation
*   **Persona:** Clinical Adversary (The Volatile Patient Relative)
*   **Scenario:** Emergency room corridor de-escalation under workflow disruption.
*   **Core Telemetry:** Vocal Calm %, De-escalation Efficiency, Empathy Synchronization.

### 4. Veterinary Medicine & Management
*   **Persona:** Grieving Client
*   **Scenario:** High-friction financial boundaries and triage choices during critical care.
*   **Core Telemetry:** Financial Boundary Firmness, Empathy Index.

### 5. Advanced Manufacturing & Automotive
*   **Persona:** Dieter Brand (The Plant Floor Superintendent)
*   **Scenario:** Middle Georgia Megasite Just-In-Time (JIT) line stoppage.
*   **Core Telemetry:** Line Strength Rating, JIT Logistics Alignment, Compliance Override Resistance.

## 💾 Quick Start & Production Setup

The backend tracks simulation states, real-time performance telemetry, and post-session analysis using a relational schema structure (`users`, `simulation_sessions`, `session_metrics`, `viral_scorecards`).

### Prerequisites
*   Python 3.10+
*   PostgreSQL 14+
*   Docker & Docker Compose

### Installation

1. Clone the repository and configure your environment variable file:
   ```bash
   git clone https://github.com
   cd MRG
   cp .env.example .env
   ```

2. Boot up the local infrastructure environment:
   ```bash
   docker-compose up -d
   ```

3. Install production and runtime dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📄 License & Legal Compliance

Distributed under the [MPL-2.0 License](LICENSE). 
