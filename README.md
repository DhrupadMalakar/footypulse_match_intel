# FootyPulse: Match Intelligence from Fan Conversations

FootyPulse transforms raw fan comments and simple match statistics into a structured, story-driven match intelligence report.  
It is built as an offline, reproducible, multi-agent project suitable for Kaggle capstone work, GitHub portfolios, and learning agent architecture.

---

## 1. Project Overview

Watching a football match is easy.  
Understanding **why** it felt the way it did is hard.

FootyPulse attempts to answer:

- What was the *crowd mood*?
- Who was the *standout player*?
- What were fans talking about?
- How do simple statistics combine with sentiment?

This project uses:
- Sample Reddit-style fan comments (offline JSON)
- Sample match statistics
- A multi-agent pipeline
- Memory + metrics + observability
- Markdown report generation

Everything runs fully **offline**, requires **no API keys**, and is designed to be Kaggle-friendly.

---

## 2. Architecture

FootyPulse uses a 5-agent pipeline:

1. **Reddit Data Fetch Agent**  
   Loads sample Reddit-style comments (JSON).

2. **Sentiment Analysis Agent**  
   Scores each comment (positive, negative, neutral).

3. **Player Impact Agent**  
   Combines goals + assists + cards + fan sentiment.

4. **Match Summary Agent**  
   Generates a short English summary of match mood.

5. **Report Generator Agent**  
   Produces a Markdown intelligence report.

Supporting modules:
- **Memory System** (long-term + session)
- **Metrics** (counts: runs, players scored, etc.)
- **Logging** (full pipeline logs for debugging)

---

## 3. Pipeline Diagram

```mermaid
flowchart LR
    A[Sample Reddit JSON] --> B[Reddit Data Agent]
    A2[Match Stats JSON] --> C[Player Impact Agent]
    B --> D[Sentiment Analysis Agent]
    D --> C
    C --> E[Match Summary Agent]
    E --> F[Report Generator]

    subgraph Memory
      M1[Long Term Memory]
      M2[Session Memory]
    end

    subgraph Observability
      O1[Logs]
      O2[Metrics]
    end
    
    B --> M1
    D --> M1
    C --> M1
    E --> M1
    B --> M2
    D --> M2
    C --> M2
    E --> M2
    B --> O1
    D --> O1
    C --> O1
    E --> O1
    B --> O2
    D --> O2
    C --> O2
    E --> O2


4. Sample Output
A demo run produces:
# FootyPulse Match Intelligence Report

Fan mood was overall positive based on 5 comments.
Standout player: Alex Smith (Red FC) with impact score 9.
The full Markdown report is saved to:
outputs/reports/demo_match_report.md
5. File Structure
footypulse_match_intel/
│
├── agent_main.py
├── requirements.txt
├── logs/
├── metrics/
├── memory_store/
├── outputs/
├── data/
│   ├── sample_reddit_thread.json
│   └── sample_match_stats.json
└── src/
    ├── agents/
    ├── tools/
    ├── models/
    ├── memory/
    └── observability/
6. How to Run (Offline)
1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
2. Install dependencies
pip install -r requirements.txt
3. Run the demo pipeline
python agent_main.py --demo
Outputs generated:
outputs/reports/demo_match_report.md
logs/app.log
metrics/counters.json
memory_store/long_term_memory.json

7. What This Project Demonstrates
Multi-Agent systems
Pipeline architecture
Data processing
Sentiment scoring
Player impact scoring
Memory and metrics tracking
Markdown report generation
Reproducible offline ML-style project
Great for Kaggle, GitHub portfolios, and interviews.
8. Future Work
Planned upgrades:
Live Reddit scraping
OpenAI-powered sentiment model
Player form tracking
Web UI (Streamlit / FastAPI)
Cloud deployment (Cloud Run)
Real match datasets
9. License
MIT License.
