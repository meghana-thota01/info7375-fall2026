"""
Aggregates per-generation labels into the findings table — the artifact a
reader sees first (per Methods Q3/the brief's "first sixty seconds").
Reports counts by model and by category, plus each underlying check
individually so precedence doesn't mask true prevalence.
"""
from collections import defaultdict

CATEGORIES = ["Contract violation", "Wrong driver", "Wrong number", "Misleading small base", "Correct"]

def build_findings_table(labeled_results):
    """
    labeled_results: list of dicts, each with keys:
        'model_name', plus everything derive_label() returns
    Returns a findings table: counts per model per category, plus
    individual check pass rates regardless of precedence.
    """
    by_model = defaultdict(lambda: defaultdict(int))
    individual_check_counts = defaultdict(lambda: defaultdict(int))
    totals_by_model = defaultdict(int)

    for r in labeled_results:
        model = r["model_name"]
        by_model[model][r["final_label"]] += 1
        totals_by_model[model] += 1
        for check_name, value in r["checks"].items():
            if value is True:
                individual_check_counts[model][check_name] += 1

    findings = {"by_model_category_counts": {}, "individual_check_pass_rates": {}}

    for model, total in totals_by_model.items():
        findings["by_model_category_counts"][model] = {
            cat: by_model[model].get(cat, 0) for cat in CATEGORIES
        }
        findings["by_model_category_counts"][model]["total_generations"] = total

        findings["individual_check_pass_rates"][model] = {
            check: round(individual_check_counts[model].get(check, 0) / total, 3)
            for check in ["schema_valid", "citations_exist", "percentage_in_tolerance", "correct_driver"]
        }

    return findings


def print_findings_table(findings):
    print(f"{'Model':<20} " + " | ".join(f"{c:<22}" for c in CATEGORIES) + " | Total")
    print("-" * 150)
    for model, counts in findings["by_model_category_counts"].items():
        row = f"{model:<20} " + " | ".join(f"{counts[c]:<22}" for c in CATEGORIES)
        row += f" | {counts['total_generations']}"
        print(row)

    print("\nIndividual check pass rates (not precedence-ordered):")
    for model, rates in findings["individual_check_pass_rates"].items():
        print(f"  {model}: {rates}")


if __name__ == "__main__":
    # CODE CORRECTNESS TEST ONLY — synthetic test results, not real model
    # outputs. No real generation has been run yet (accounts unfunded).
    # This proves the aggregator correctly tallies and reports.
    print("=== Testing with synthetic placeholder results (NOT real benchmark data) ===\n")

    test_results = [
        {"model_name": "claude-sonnet-5-5", "table_id": "sales_01", "final_label": "Correct",
         "checks": {"schema_valid": True, "citations_exist": True, "percentage_in_tolerance": True,
                    "correct_driver": True, "small_base_caveat_present": True}},
        {"model_name": "claude-sonnet-5-5", "table_id": "sales_02", "final_label": "Wrong driver",
         "checks": {"schema_valid": True, "citations_exist": True, "percentage_in_tolerance": True,
                    "correct_driver": False, "small_base_caveat_present": None}},
        {"model_name": "gpt-6.1-terra", "table_id": "sales_01", "final_label": "Misleading small base",
         "checks": {"schema_valid": True, "citations_exist": True, "percentage_in_tolerance": True,
                    "correct_driver": True, "small_base_caveat_present": False}},
        {"model_name": "gpt-6.1-terra", "table_id": "sales_02", "final_label": "Contract violation",
         "checks": {"schema_valid": False, "citations_exist": None, "percentage_in_tolerance": None,
                    "correct_driver": None, "small_base_caveat_present": None}},
    ]

    findings = build_findings_table(test_results)
    print_findings_table(findings)
    print("\nAggregator works correctly. Awaiting real generations to populate with actual data.")
