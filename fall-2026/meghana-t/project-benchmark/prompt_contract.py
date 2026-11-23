"""
The fixed prompt contract: turns any table into the exact prompt sent to
both models, and defines the required JSON response schema.
"""
import json

def build_prompt(table):
    cols = table["columns"]
    dim_col, prior_col, current_col = cols[0], cols[1], cols[2]

    table_text = f"{dim_col} | {prior_col} | {current_col}\n"
    table_text += "-" * len(table_text) + "\n"
    for row in table["rows"]:
        table_text += f"{row[dim_col]} | {row[prior_col]} | {row[current_col]}\n"

    prompt = f"""You are analyzing a business dashboard table. Write ONE insight sentence explaining the main driver of change, following this exact JSON format:

{{
  "insight_sentence": "<one sentence, plain English>",
  "claimed_driver": "<the single {dim_col} value most responsible for the overall change>",
  "claimed_percentage": <the overall percentage change across all rows, as a number>,
  "cited_figures": [<the specific numbers from the table you are citing as evidence>]
}}

Table:
{table_text}

Respond with ONLY the JSON object, no other text."""
    return prompt

def build_response_schema():
    return {
        "type": "object",
        "required": ["insight_sentence", "claimed_driver", "claimed_percentage", "cited_figures"],
        "properties": {
            "insight_sentence": {"type": "string"},
            "claimed_driver": {"type": "string"},
            "claimed_percentage": {"type": "number"},
            "cited_figures": {"type": "array", "items": {"type": "number"}}
        }
    }

if __name__ == "__main__":
    with open("tables/all_tables.json") as f:
        tables = json.load(f)

    example = next(t for t in tables if t["table_id"] == "sales_01")
    print("=== Example prompt that would be sent to each model ===\n")
    print(build_prompt(example))
    print("\n=== Required response schema ===\n")
    print(json.dumps(build_response_schema(), indent=2))
