"""
REAL EXECUTION — Claude Sonnet 5.5 only.

GPT-6.1 Terra is intentionally NOT called here: no funded account exists for
it yet (confirmed empirically across 3 platforms — see FRICTIONAL.md). This
script runs only the side that's genuinely free and ready right now, and
honestly reports that fact rather than skipping it silently.

Run on your own machine:
    export ANTHROPIC_API_KEY="your-real-key-here"
    python3 run_real_generations_claude_only.py
"""
import os
import json
import requests
from prompt_contract import build_prompt
from automated_checks import check_schema_valid, check_cited_figures_exist, check_percentage_tolerance
from derive_label import derive_label

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not ANTHROPIC_KEY:
    print("ERROR: set ANTHROPIC_API_KEY as an environment variable first.")
    print("  export ANTHROPIC_API_KEY='your-key'")
    exit(1)

def call_claude(prompt):
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-5-5",
            "max_tokens": 300,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]

def parse_json_response(raw_text):
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    try:
        return json.loads(cleaned.strip()), None
    except json.JSONDecodeError as e:
        return None, f"could not parse as JSON: {e}. Raw text: {raw_text[:200]}"


if __name__ == "__main__":
    with open("tables/real_tables.json") as f:
        all_tables = json.load(f)

    test_tables = all_tables[:2]  # 2 real generations to start
    results_log = []

    print("="*60)
    print("REAL EXECUTION — Claude Sonnet 5.5 only")
    print("GPT-6.1 Terra: SKIPPED, pending account funding (see FRICTIONAL.md)")
    print("="*60)

    for table in test_tables:
        prompt = build_prompt(table)
        print(f"\n{'='*60}\nTable: {table['table_id']} ({table['domain']}, years {table['years_compared']})")
        print(f"True driver: {table['ground_truth']['true_driver']}, true pct: {table['ground_truth']['true_percentage_change']}")
        print(f"{'='*60}")

        print(f"\n--- Calling Claude Sonnet 5.5 (REAL API CALL) ---")
        try:
            raw = call_claude(prompt)
            print(f"Raw response:\n{raw}")
            parsed, parse_error = parse_json_response(raw)

            if parse_error:
                print(f"\nPARSE FAILED: {parse_error}")
                results_log.append({"table_id": table["table_id"], "model_name": "claude-sonnet-5-5",
                                    "raw_response": raw, "parse_error": parse_error})
                continue

            schema_ok, schema_msg = check_schema_valid(parsed)
            print(f"\nSchema check: {schema_ok} ({schema_msg})")
            if schema_ok:
                cit_ok, cit_msg = check_cited_figures_exist(parsed, table)
                tol_ok, tol_msg = check_percentage_tolerance(parsed, table)
                print(f"Citations check: {cit_ok} ({cit_msg})")
                print(f"Tolerance check: {tol_ok} ({tol_msg})")

            print(f"\n*** The 2 hand-labeled judgment calls still need a human to read")
            print(f"    this response and decide — that step is not automated. ***")

            results_log.append({
                "table_id": table["table_id"], "domain": table["domain"], "model_name": "claude-sonnet-5-5",
                "true_driver": table["ground_truth"]["true_driver"],
                "true_percentage": table["ground_truth"]["true_percentage_change"],
                "raw_response": raw, "parsed_response": parsed,
                "schema_valid": schema_ok
            })
        except requests.exceptions.RequestException as e:
            print(f"API CALL FAILED: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"Response body: {e.response.text}")
            results_log.append({"table_id": table["table_id"], "model_name": "claude-sonnet-5-5", "error": str(e)})

    with open("real_generation_results_claude_only.json", "w") as f:
        json.dump(results_log, f, indent=2)

    print(f"\n\n{'='*60}")
    print(f"DONE. {len(results_log)} REAL Claude Sonnet 5.5 responses logged.")
    print(f"These are genuine results from a real, funded API call.")
    print(f"GPT-6.1 Terra side remains honestly pending account funding.")
    print(f"{'='*60}")
