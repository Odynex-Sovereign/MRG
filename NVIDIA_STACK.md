# NVIDIA Tech Stack Integration Guide for MRG

MRG is designed around the following NVIDIA technologies. Full production fidelity requires NVIDIA hardware and official SDKs.

## 1. NVIDIA NIM (Nemotron-4) — Micro-Cognitive Tier
- **Role**: Sub-50 ms conversational adversarial / coaching loop.
- **Integration**: OpenAI-compatible HTTP API (already implemented in `services/micro_tactical/nemotron_orchestrator.py`).
- **Setup**:
  1. Obtain an API key from https://build.nvidia.com or your private NIM deployment.
  2. Set `NVIDIA_NIM_API_KEY=nvapi-...`
  3. Optional: `NVIDIA_NIM_BASE_URL` and `NVIDIA_NIM_MODEL`.
- **Local NIM**: You can self-host Nemotron via NVIDIA NIM containers on DGX / HGX / compatible GPUs.

## 2. NVIDIA Riva — Speech (TTS / ASR / Vocal Stress)
- **Role**: Real-time vocal stress extraction + high-fidelity TTS for adversarial personas.
- **Current state**: Stub in `services/sensory/riva_tts.py` (returns PCM placeholder).
- **Production path**:
  - Install NVIDIA Riva Skills (Docker) on a GPU node.
  - Point the broker at the Riva gRPC endpoint.
  - Recommended models: `en-US-Neural` voices + custom stress classifiers.

## 3. NVIDIA Audio2Face
- **Role**: Sub-100 ms audio → blendshape mapping for digital-twin avatars.
- **Current state**: RPC stub in `services/sensory/audio2face_rpc.py` returns synthetic blendshape matrices.
- **Production path**:
  - Deploy Audio2Face (Omniverse / UE5 / custom) with gRPC or REST bridge.
  - Feed live audio frames; receive ARKit / OpenUSD-compatible blendshapes.
  - Config template lives in `config/openusd_avatar_v2.json`.

## 4. NVIDIA Omniverse + OpenUSD
- **Role**: Pixel-streamed 3D crisis environments (boardrooms, TOC, flight decks, etc.).
- **Current state**: Trigger payloads only (expression profiles + intensity).
- **Production path**:
  - Omniverse Nucleus + Kit / USD Composer scenes.
  - Livepeer or custom WebRTC/WebSocket pixel streaming for edge distribution.
  - Recommended: Isaac Sim for scenario authoring when physical AI digital twins are required.

## 5. Recommended Hardware Profiles
| Tier | Hardware | Use |
|------|----------|-----|
| Edge / Demo | RTX 4090 / Jetson AGX Orin | Local Audio2Face + NIM |
| Production | DGX H100 / HGX B200 | Full multi-agent + Omniverse |
| Cloud | NVIDIA Cloud Functions / DGX Cloud | Elastic NIM + Riva |

## 6. Environment Variables (NVIDIA related)
```
NVIDIA_NIM_API_KEY=nvapi-...
NVIDIA_NIM_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_NIM_MODEL=nvidia/nemotron-4-340b-instruct
# Optional local Riva / A2F
RIVA_SERVER=localhost:50051
AUDIO2FACE_ENDPOINT=localhost:50052
```

## 7. Fallback Behaviour
All NVIDIA and DeepSeek clients degrade gracefully to sandbox mode when keys are absent. The WebSocket pipeline and telemetry computation remain fully functional for local testing and demos.
