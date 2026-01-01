# ModulusAI — Backend

This repository contains the **backend** for **ModulusAI**, an AI-powered academic planning platform for NUS students.

The backend is where most of the system’s intelligence lives: constraint solving, degree verification, personalization logic, and AI-driven recommendations. It is designed to be modular, auditable, and robust enough to support complex academic rules that span multiple semesters.

---

## What the backend does

- **User authentication & profiles**  
  Handles login, registration, and persistent academic profiles (degree, majors/minors, preferences, completed modules).

- **4-Year planning engine**  
  Validates long-term academic plans across 8 semesters, resolving prerequisite chains, preclusions, and temporal constraints.

- **Degree requirement classification & verification**  
  Automatically categorizes modules into NUS degree requirement buckets and verifies graduation compliance across credits, levels, and focus areas.

- **Semester timetable optimization**  
  Uses a constraint solver to generate clash-free timetables across lectures, tutorials, and labs.

- **AI-powered academic chatbot**  
  Provides personalized guidance by combining user context, planned modules, workload signals, and external data sources.

- **Sentiment analysis pipeline**  
  Scrapes large-scale Reddit discussions and aggregates sentiment using transformer-based NLP models.

---

## Tech Stack

- **Python**
- **Flask** (REST API)
- **PostgreSQL** (persistent storage)
- **Google OR-Tools** (constraint solving)
- **Groq API + LLaMA** (chatbot inference)
- **HuggingFace / RoBERTa** (sentiment analysis)
- **Docker** for containerized development and deployment

---

## Architecture Overview

- RESTful Flask API exposing planning, classification, chat, and optimization endpoints
- PostgreSQL as the source of truth for users, modules, timetables, and academic state
- Constraint-based solvers for timetable generation and feasibility checks
- NLP components integrated as services within the backend pipeline

The backend is intentionally stateless at the API layer, with all long-term state persisted in the database.

---

## Getting Started

### Environment setup

Create a `.env` file in the backend root:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=changethispassword
POSTGRES_DB=modulusai
SECRET_KEY=your_secret_key_here

GROQ_API_KEY=
REDDIT_ID=
REDDIT_SECRET=
```
## Running locally

### With Docker (recommended)

```bash
docker compose up --build
```
### The API will be available at:
```text
http://localhost:5000
```
Docker is recommended due to heavy dependencies such as OR-Tools and transformer models.
