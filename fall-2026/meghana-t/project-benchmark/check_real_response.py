"""Check the first REAL model response against the real pipeline."""
import json
from automated_checks import check_schema_valid, check_cited_figures_exist, check_percentage_tolerance
from derive_label import derive_label

tables = json.load(open("tables/real_tables.json"))
table = next(t for t in tables if t["table_id"] == "region_01")

real_response = {
    "insight_sentence": "Overall sales decreased by 4.26% from 2023 to 2024, primarily driven by the South region where sales fell from 103,845.84 to 71,359.98.",
    "claimed_driver": "South",
    "claimed_percentage": -4.26,
    "cited_figures": [103845.84, 71359.98]
}

print("=== REAL model: Gemini (gemini-flash-latest), REAL table: region_01 ===\n")
print("Ground truth:", table["ground_truth"])
print("\nModel response:", json.dumps(real_response, indent=2))

schema_ok, schema_msg = check_schema_valid(real_response)
cit_ok, cit_msg = check_cited_figures_exist(real_response, table)
tol_ok, tol_msg = check_percentage_tolerance(real_response, table)

print(f"\nSchema: {schema_ok} ({schema_msg})")
print(f"Citations: {cit_ok} ({cit_msg})")
print(f"Tolerance: {tol_ok} ({tol_msg})")

# For the label, we (the human) judge: did it name the correct driver? YES (South matches ground truth)
result = derive_label(real_response, table, q1_correct_driver=True, q2_small_base_caveat=None)
print(f"\nFinal derived label: {result['final_label']}")
