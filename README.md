# Multi-Agent RAG Document QA App — LLaMA3 + GROQ + Kubernetes

[![Kubernetes](https://img.shields.io/badge/Kubernetes-Production%20Ready-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![GROQ API](https://img.shields.io/badge/GROQ-API-00D8FF?logo=graphql)](https://groq.com/)
[![LLaMA 3](https://img.shields.io/badge/LLaMA-3-8B008B)](https://meta.ai/llama/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://www.python.org/)

A scalable, containerized, multi-agent **Document Question Answering** application using **Retrieval-Augmented Generation (RAG)**. Powered by **LLaMA 3**, integrated with the **GROQ API**, and deployed on **Kubernetes** for high performance and orchestration.

---

## 🔍 Features

- 🤖 **Multi-agent architecture** for specialized task handling
- 📄 **RAG pipeline** for efficient document retrieval and contextual response generation
- ⚡ **GROQ API** acceleration for low-latency inference
- 🦙 **LLaMA 3 integration** for state-of-the-art natural language understanding
- ☸️ **Kubernetes deployment** for scalability, resilience, and automation
- 🚀 API-ready for integration into larger systems

---

## ⚙️ Prerequisites

- Kubernetes cluster (local with Minikube or remote)
- `kubectl` configured
- Python 3.10+
- GROQ API Key
- Helm (optional, for deployment)

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone git@github.com:aenodehi/Kuber_RAG_App.git
cd Kuber_RAG_App
```
### 2. Set up environment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```
### 3. Set your GROQ API Key
```bash
export GROQ_API_KEY=your_api_key_here
```
### 4. Deploy on Kubernetes
```bash
kubectl apply -f k8s/
```
## 🧠 Architecture Overview
┌────────────┐       ┌──────────────┐      ┌──────────────┐
│ User Query │ ───►  │ Retriever(s) │ ──►  │ GROQ + LLaMA │
└────────────┘       └─────┬────────┘      └────┬─────────┘
                           ▼                      ▼
                    🔍 Document Store       🧠 Answer Generator


