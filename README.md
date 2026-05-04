# Generic  Survey - Question Extraction & Template Builder

## Project purpose
- Convert a corpus of historical survey questions into a concise, reusable generic survey template.
- Provide an interactive Streamlit dashboard for exploration, filtering, visualization, and AI‑driven enrichment.
- Produce ready-to-use CSV templates for downstream survey administration and analytics.

## Key outcomes 
- A reproducible workflow that converts noisy historical questions into a structured generic template.
- Interactive dashboard with filters, ranking tables, visualizations (bar, pie, heatmap), and template editing.
- Automated AI-assisted generation of generic questions + multiple-choice options for rapid template enrichment.
- Exportable templates: updated CSVs ready for downstream tools (survey platforms, analyses).

## What I delivered (high-level)
- Data ingestion & ranking visualization with filtering by confidence and question matches.
- Template management: view, filter, and append generated questions to the canonical template.
- AI enrichment pipeline to produce generic questions and options from raw input questions.
- Dockerized deployment for reproducible demos.

## Quick links to important files and functions
- UI & orchestration: [dashboard.py](dashboard.py) — includes [`dashboard.update_callback`](dashboard.py) and many cached loaders: [`dashboard.load_generic_template`](dashboard.py), [`dashboard.load_refined_template`](dashboard.py), [`dashboard.load_updated_generic_template`](dashboard.py), [`dashboard.load_matched_questions`](dashboard.py), [`dashboard.load_ranking_data`](dashboard.py), [`dashboard.load_cluster_questions`](dashboard.py).
- AI generation & template updater: [survey_generator.py](survey_generator.py) — includes [`survey_generator.generate_survey_json`](survey_generator.py), [`survey_generator.generate_new_questions`](survey_generator.py), [`survey_generator.update_survey`](survey_generator.py).
- Config & environment: [.env](.env)
- Deployment: [Dockerfile](Dockerfile)
- Requirements: [requirements.txt](requirements.txt)
- Assets & I/O: [logo.webp](logo.webp), input directory [input/](input/), output templates and artifacts:
  - [output/GenericSurvey_combined.csv](output/GenericSurvey_combined.csv)
  - [output/clustered_questions.csv](output/clustered_questions.csv)
  - [output/matched_questions.csv](output/matched_questions.csv)
  - [output/ranking.csv](output/ranking.csv)
  - other generated CSVs in [output/](output/)

## Prerequisites
- Python 3.9+ (project built with Python 3.9 in Dockerfile).
- Install dependencies:
  - pip install -r [requirements.txt](requirements.txt)
- Optional: Local LLM or LLM endpoint for AI generation — configured in [survey_generator.py](survey_generator.py) via `GPT4ALL_API_URL` (also settable via [.env](.env) if you adapt the code).

### Run locally (quick)
1. Create virtual environment and install requirements:
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
    ```
2. Start dashboard:
    ```sh
    streamlit run dashboard.py
    ```
    
3. Open the browser at the address printed by Streamlit (default http://localhost:8501).

### Run via Docker
1. Build:
2. Run:
3. Visit http://localhost:8501

## Core workflows (what to try)

- Explore & filter ranking data:
    - Use the "Rank Table" tab in dashboard.py to filter by confidence, search historical and generic matches, and inspect top/middle/bottom matches. Ranking data is loaded from output/ranking.csv via dashboard.load_ranking_data.
- Visualize:
    - View confidence-level bar and pie charts and a similarity heatmap derived from output/clustered_questions.csv via dashboard.load_cluster_questions.
- Generate AI‑assisted generic questions:
    - In the "AI Generic Survey Enrichment" tab, paste/enter raw questions and click "Generate New Generic Question" — this calls survey_generator.generate_new_questions, which uses survey_generator.generate_survey_json to call a configured LLM endpoint.
    - Generated questions are displayed as a DataFrame and cached in session state for review.
- Append to template:
    - Click "Add To Template" for generated entries — this triggers dashboard.update_callback which calls survey_generator.update_survey to append to output/GenericSurvey_combined.csv. The template loader dashboard.load_generic_template is cached and can be cleared via the dashboard Refresh button.

## Practical considerations & recommended setup

- LLM endpoint: survey_generator.py uses GPT4ALL_API_URL. For production demos, point this to a stable model endpoint and protect credentials. The current code expects an accessible endpoint and returns JSON arrays of generated question objects.
- Data backups: The template CSV at output/GenericSurvey_combined.csv is overwritten when updated — version or backup before bulk changes.
- Reproducibility: Use the provided Dockerfile for consistent runtime environments.
- Resource considerations: Large similarity matrices and embeddings can be memory intensive — consider sampling for demos.

## Evaluation & success metrics (how to measure outcomes)

- Coverage: Percentage of historical questions mapped to a generic question (match rate).
- Redundancy reduction: Count of unique generic questions vs original question count.
- Human validation: Qualitative review of generated generic questions by domain experts — track acceptance rate of AI-suggested items added to the template.
- Template readiness: Number of fully populated multiple-choice options per generic question.

## How to extend

- Replace LLM backend: Update GPT4ALL_API_URL or refactor survey_generator.generate_survey_json to use another API (auth, rate-limits handling).
- Add multi-language support: Preprocess and tag input questions; request localized options from the LLM.
- Add unit tests: Introduce tests around JSON parsing in survey_generator.generate_survey_json and CSV outputs.

## Troubleshooting

- If Streamlit fails to start: verify dependencies in requirements.txt and port availability.
- If AI generation returns invalid JSON: check the logs printed by survey_generator.generate_survey_json for response text and adjust prompt or parsing regex.
- If updates don't appear: use the dashboard "Refresh" button to clear cached loaders — these are implemented via decorators like dashboard.load_generic_template.

## Files to review (quick)

- dashboard.py
- survey_generator.py
- Dockerfile
- requirements.txt
- .env
- Output artifacts in output/

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
