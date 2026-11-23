"""
Aggregated findings from the 6 REAL generations run so far (3 Gemini, 3 Claude),
all checked against real ground truth from the actual Superstore data.
This is genuine benchmark progress, not a placeholder demonstration.
"""
import json
from derive_label import derive_label
from findings_report import build_findings_table, print_findings_table

tables = json.load(open("tables/real_tables.json"))
t_region01 = next(t for t in tables if t["table_id"] == "region_01")
t_category01 = next(t for t in tables if t["table_id"] == "category_01")
t_region02 = next(t for t in tables if t["table_id"] == "region_02")

results = []

# Gemini's 3 real responses
gemini_region01 = {"insight_sentence": "Overall sales decreased by 4.26% from 2023 to 2024, primarily driven by the South region where sales fell from 103,845.84 to 71,359.98.",
    "claimed_driver": "South", "claimed_percentage": -4.26, "cited_figures": [103845.84, 71359.98]}
r = derive_label(gemini_region01, t_region01, q1_correct_driver=True, q2_small_base_caveat=None)
results.append({"model_name": "gemini-flash-latest", **r})

gemini_category01 = {"insight_sentence": "Overall sales decreased by 4.26% from 2023 to 2024, primarily driven by Office Supplies where sales fell from 154,013.97 to 137,670.22.",
    "claimed_driver": "Office Supplies", "claimed_percentage": -4.26, "cited_figures": [154013.97, 137670.22]}
r = derive_label(gemini_category01, t_category01, q1_correct_driver=True, q2_small_base_caveat=None)
results.append({"model_name": "gemini-flash-latest", **r})

gemini_region02 = {"insight_sentence": "Overall profit increased by 20.0% from 2023 to 2024, primarily driven by the Central region where profit surged from 539.55 to 11,716.80.",
    "claimed_driver": "Central", "claimed_percentage": 20.0, "cited_figures": [539.55, 11716.8]}
r = derive_label(gemini_region02, t_region02, q1_correct_driver=True, q2_small_base_caveat=False)
results.append({"model_name": "gemini-flash-latest", **r})

# Claude's 3 real responses
claude_region01 = {"insight_sentence": "Total sales fell 4.26% from 494,040.20 to 472,993.03, driven mainly by South, which dropped 32,485.86 (from 103,845.84 to 71,359.98, about 31.3%), more than offsetting East's 21,631.59 gain.",
    "claimed_driver": "South", "claimed_percentage": -4.26, "cited_figures": [494040.20, 472993.03, 103845.84, 71359.98, 32485.86, 21631.59]}
r = derive_label(claude_region01, t_region01, q1_correct_driver=True, q2_small_base_caveat=None)
results.append({"model_name": "claude-sonnet-5-5", **r})

claude_category01 = {"insight_sentence": "Total sales fell 4.26% from 494,040.21 to 472,993.04, driven mainly by Office Supplies, which dropped 16,343.75 (from 154,013.97 to 137,670.22, about 10.6%), with Technology also declining 14,908.91 while Furniture grew 10,205.49.",
    "claimed_driver": "Office Supplies", "claimed_percentage": -4.26, "cited_figures": [494040.21, 472993.04, 154013.97, 137670.22, 16343.75, 14908.91, 10205.49]}
r = derive_label(claude_category01, t_category01, q1_correct_driver=True, q2_small_base_caveat=None)
results.append({"model_name": "claude-sonnet-5-5", **r})

claude_region02 = {"insight_sentence": "Total profit rose 20.00% from 51,684.29 to 62,020.96, driven mainly by Central, which jumped 11,177.25 (from 539.55 to 11,716.80), more than offsetting South's 3,560.53 decline.",
    "claimed_driver": "Central", "claimed_percentage": 20.0, "cited_figures": [51684.29, 62020.96, 539.55, 11716.8, 11177.25, 3560.53]}
r = derive_label(claude_region02, t_region02, q1_correct_driver=True, q2_small_base_caveat=None)
results.append({"model_name": "claude-sonnet-5-5", **r})

with open("real_findings_partial.json", "w") as f:
    json.dump(results, f, indent=2)

print("=== REAL FINDINGS (6 of 36 generations run so far) ===\n")
findings = build_findings_table(results)
print_findings_table(findings)
print("\nThese are genuine results from real model calls, checked against real Superstore data.")
print("Not all 36 generations have been run yet — this is partial, honest progress.")
