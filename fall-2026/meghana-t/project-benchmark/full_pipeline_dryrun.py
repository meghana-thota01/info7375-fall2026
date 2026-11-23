"""
INTEGRATION DRY-RUN — chains every real piece of the pipeline together in
sequence: table -> prompt -> [model call would go here] -> checks -> label
-> findings table.

This is explicitly a DRY RUN. The "model response" below is a hand-written
placeholder standing in for where a real API response would go — it is
clearly labeled as such everywhere. No real API call has been made, since
both accounts remain intentionally unfunded (see FRICTIONAL.md). This script
proves the PIPELINE MECHANICS work end-to-end; it reports no benchmark
results, real or implied.
"""
import json
from prompt_contract import build_prompt
from automated_checks import check_schema_valid, check_cited_figures_exist, check_percentage_tolerance
from derive_label import derive_label
from findings_report import build_findings_table, print_findings_table

print("="*70)
print("DRY RUN — demonstrates pipeline mechanics only. NOT real benchmark data.")
print("No API call has been made. Both model accounts are unfunded by choice.")
print("="*70)

with open("tables/real_tables.json") as f:
    tables = json.load(f)

table = tables[0]  # first table

print(f"\nSTEP 1 — Table selected: {table['table_id']} ({table['domain']}, years {table['years_compared']})")

print("\nSTEP 2 — Prompt that WOULD be sent to a real model:")
prompt = build_prompt(table)
print(prompt[:300] + "...\n[truncated for display]")

print("\nSTEP 3 — [PLACEHOLDER] where a real API response would arrive.")
print("         Using a hand-written stand-in response, clearly marked as such:")
driver = table["ground_truth"]["true_driver"]
true_pct = table["ground_truth"]["true_percentage_change"]
driver_row = next(r for r in table["rows"] if r[table["columns"][0]] == driver)
PLACEHOLDER_response_not_real_api_output = {
    "insight_sentence": f"{driver} was the main driver of the change this period.",
    "claimed_driver": driver,
    "claimed_percentage": true_pct,
    "cited_figures": [driver_row[table["columns"][1]], driver_row[table["columns"][2]]]
}
print(json.dumps(PLACEHOLDER_response_not_real_api_output, indent=2))

print("\nSTEP 4 — Running the 3 automated checks on this placeholder response:")
schema_ok, schema_msg = check_schema_valid(PLACEHOLDER_response_not_real_api_output)
citations_ok, citations_msg = check_cited_figures_exist(PLACEHOLDER_response_not_real_api_output, table)
tolerance_ok, tolerance_msg = check_percentage_tolerance(PLACEHOLDER_response_not_real_api_output, table)
print(f"  Schema: {schema_ok} ({schema_msg})")
print(f"  Citations: {citations_ok} ({citations_msg})")
print(f"  Tolerance: {tolerance_ok} ({tolerance_msg})")

print("\nSTEP 5 — [PLACEHOLDER] where real human hand-labeling would happen.")
print("         Using placeholder labels matching the stand-in response (it names the correct driver):")
q1_correct_driver_PLACEHOLDER = True
q2_caveat_PLACEHOLDER = True if table["small_base"] else None

print("\nSTEP 6 — Deriving the final label via the precedence order:")
result = derive_label(PLACEHOLDER_response_not_real_api_output, table,
                       q1_correct_driver_PLACEHOLDER, q2_caveat_PLACEHOLDER)
print(json.dumps(result, indent=2))

print("\nSTEP 7 — Feeding this one result into the findings-table aggregator:")
one_result_for_aggregator = {"model_name": "PLACEHOLDER_not_a_real_model_call", **result}
findings = build_findings_table([one_result_for_aggregator])
print_findings_table(findings)

print("\n" + "="*70)
print("DRY RUN COMPLETE. Every stage of the pipeline ran successfully end to end.")
print("Nothing above is a real benchmark result — Steps 3 and 5 are explicitly")
print("placeholders standing in for a real API call and real human labeling,")
print("neither of which has happened yet.")
print("="*70)
