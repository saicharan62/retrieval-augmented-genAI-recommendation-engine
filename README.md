# SHL Assessment Recommendation Engine

A minimal, deterministic GenAI-based assessment recommendation system
built using semantic search over the SHL product catalog.

## Features
- Scrapes SHL Individual Test Solutions
- Semantic search using embeddings + FAISS
- Balanced recommendations across skill and behavior tests
- FastAPI-based REST API

## API Endpoints
- GET /health
- POST /recommend

## Setup
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
