# Regional Ocean Modeling — Expert Conversations

A curated dataset of expert interviews on regional ocean model configuration, tuning, and evaluation. Five edited Q&A conversations with physical oceanographers, structured for use as a fine-tuning dataset for large language models.

**[→ Browse the transcripts online](https://aidanjanney.github.io/RegionalOceanModelingInterviews/)** *(update with your GitHub Pages URL)*

---

## Topics covered

| Transcript | Topic |
|---|---|
| T1 | Coral Triangle & Benguela Upwelling — Indonesian Throughflow, tidal mixing, bathymetric tuning |
| T3 | Northwest Atlantic Seasonal Forecasting — Gulf Stream, viscosity, BGC metrics |
| T4 | Black Sea, Arctic & Equatorial Pacific — vertical grids, mixing schemes, equatorial coupling |
| T5 | California Current System — upwelling, ecosystem modeling, hindcast validation |
| T6 | Northeast Pacific Fisheries & Coral Triangle BGC — Bering Sea cold pool, restratification |

## Repository structure

```
transcripts/          # Source Q&A transcripts (JSON, role-tagged)
data/
  merged_for_finetuning.jsonl   # All exchanges bundled for fine-tuning (auto-generated)
  metadata.json                 # Exchange counts and last-updated timestamp (auto-generated)
scripts/
  merge_to_jsonl.py   # Regenerates data/ from transcripts/
index.html            # GitHub Pages viewer site
```

## Dataset format

Each line in `merged_for_finetuning.jsonl` is a self-contained conversation exchange:

```json
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

Compatible with OpenAI fine-tuning and Anthropic's model training pipelines.

## Updating transcripts

Edit or add JSON files in `transcripts/`. On push to `main`, the GitHub Actions pipeline automatically:

1. Regenerates `data/merged_for_finetuning.jsonl` and `data/metadata.json`
2. Commits the updated data files
3. Redeploys the GitHub Pages site with the new exchange count

To run locally:

```bash
python3 scripts/merge_to_jsonl.py
```

## Enabling GitHub Pages

1. Go to **Settings → Pages**
2. Set **Source** to **GitHub Actions**
3. Push to `main` — the `deploy-pages` workflow handles the rest

## Contributors

| Contributor | Role |
|---|---|
| [Aidan Janney](https://github.com/aidanjanney) | Dataset curation, repository setup |
| [Claude](https://claude.ai) (Anthropic) | AI assistant — repository scaffolding, README, automation |

## Context

Produced at [NCAR](https://ncar.ucar.edu) as part of LLM testing work for earth system modeling applications.
