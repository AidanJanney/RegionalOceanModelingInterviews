"""
Regenerates data/merged_for_finetuning.jsonl and data/metadata.json
from all JSON transcript files in transcripts/.

Run from the repo root:
    python scripts/merge_to_jsonl.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT    = Path(__file__).resolve().parent.parent
TRANSCRIPTS  = REPO_ROOT / "transcripts"
DATA_DIR     = REPO_ROOT / "data"
JSONL_OUT    = DATA_DIR / "merged_for_finetuning.jsonl"
METADATA_OUT = DATA_DIR / "metadata.json"

DATA_DIR.mkdir(exist_ok=True)

json_files = sorted(TRANSCRIPTS.glob("*.json"))
total_exchanges = 0

with open(JSONL_OUT, "w", encoding="utf-8") as outfile:
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as infile:
            try:
                data = json.load(infile)
            except json.JSONDecodeError as e:
                print(f"  ⚠  Skipping {json_file.name}: {e}")
                continue

        messages: list[dict] = []

        for item in data.get("messages", []):
            role    = item.get("role", "").lower()
            content = item.get("content", "").strip()

            if not content:
                continue

            normalized = "user" if role == "user" else "assistant"

            if not messages:
                if normalized == "user":
                    messages.append({"role": "user", "content": content})
            else:
                if messages[-1]["role"] == normalized:
                    messages[-1]["content"] += " " + content
                elif messages[-1]["role"] == "assistant" and normalized == "user":
                    if len(messages) > 1:
                        json.dump({"messages": messages}, outfile, ensure_ascii=False)
                        outfile.write("\n")
                        total_exchanges += 1
                    messages = [{"role": "user", "content": content}]
                else:
                    messages.append({"role": normalized, "content": content})

        if len(messages) > 1 and messages[-1]["role"] == "assistant":
            json.dump({"messages": messages}, outfile, ensure_ascii=False)
            outfile.write("\n")
            total_exchanges += 1

print(f"✅  {total_exchanges} exchanges from {len(json_files)} transcripts → {JSONL_OUT.relative_to(REPO_ROOT)}")

with open(METADATA_OUT, "w", encoding="utf-8") as f:
    json.dump({
        "transcriptCount": len(json_files),
        "totalExchanges": total_exchanges,
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
    }, f, indent=2)

print(f"✅  metadata → {METADATA_OUT.relative_to(REPO_ROOT)}")
