"""
The three automated checks from the Methods/Appendix. No human judgment —
these run the same way every time, on any response.
"""
import json

def check_schema_valid(response):
    """Check 1: response has all required fields with correct types."""
    required = {
        "insight_sentence": str,
        "claimed_driver": str,
        "claimed_percentage": (int, float),
        "cited_figures": list
    }
    for field, expected_type in required.items():
        if field not in response:
            return False, f"missing field: {field}"
        if not isinstance(response[field], expected_type):
            return False, f"wrong type for {field}: expected {expected_type}, got {type(response[field])}"
    return True, "valid"

def check_cited_figures_exist(response, table):
    """Check 2: every cited figure actually appears in the table."""
    all_table_numbers = set()
    for row in table["rows"]:
        for col in table["columns"][1:]:  # skip the dimension column
            all_table_numbers.add(row[col])

    cited = response.get("cited_figures", [])
    missing = [f for f in cited if f not in all_table_numbers]
    if missing:
        return False, f"cited figures not found in table: {missing}"
    return True, "all cited figures verified in table"

def check_percentage_tolerance(response, table):
    """Check 3: claimed percentage within 1 point of recomputed true value."""
    true_pct = table["ground_truth"]["true_percentage_change"]
    claimed_pct = response.get("claimed_percentage")
    if claimed_pct is None:
        return False, "no claimed_percentage to check"
    diff = abs(claimed_pct - true_pct)
    if diff <= 1.0:
        return True, f"within tolerance (claimed={claimed_pct}, true={true_pct}, diff={diff:.2f})"
    return False, f"outside tolerance (claimed={claimed_pct}, true={true_pct}, diff={diff:.2f})"


if __name__ == "__main__":
    with open("tables/real_tables.json") as f:
        tables = json.load(f)
    table = next(t for t in tables if t["table_id"] == "region_01")

    print("=== Test 1: a CORRECT example response ===")
    driver_name = table["ground_truth"]["true_driver"]
    true_pct = table["ground_truth"]["true_percentage_change"]
    driver_row = next(r for r in table["rows"] if r[table["columns"][0]] == driver_name)
    good_response = {
        "insight_sentence": f"{driver_name} was the main driver of change.",
        "claimed_driver": driver_name,
        "claimed_percentage": true_pct,
        "cited_figures": [driver_row[table["columns"][1]], driver_row[table["columns"][2]]]
    }
    print("Schema:", check_schema_valid(good_response))
    print("Citations:", check_cited_figures_exist(good_response, table))
    print("Tolerance:", check_percentage_tolerance(good_response, table))

    print("\n=== Test 2: a WRONG example response (fails all 3 checks) ===")
    bad_response = {
        "insight_sentence": "Revenue grew substantially, driven by the East region.",
        "claimed_driver": "East",
        "claimed_percentage": 15.0,
        "cited_figures": [999999]
    }
    print("Schema:", check_schema_valid(bad_response))
    print("Citations:", check_cited_figures_exist(bad_response, table))
    print("Tolerance:", check_percentage_tolerance(bad_response, table))

    print("\n=== Test 3: a SCHEMA-INVALID example (missing field) ===")
    broken_response = {
        "claimed_driver": "South",
        "claimed_percentage": 0.3
    }
    print("Schema:", check_schema_valid(broken_response))
