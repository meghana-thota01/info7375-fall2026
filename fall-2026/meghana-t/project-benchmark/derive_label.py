"""
Derives the final report-level label for one generation, using the precedence
order from the Appendix:
Contract violation -> Wrong driver -> Wrong number -> Misleading small base -> Correct

Also reports each of the 5 underlying checks individually, so precedence
doesn't mask true prevalence (per the Methods section).
"""
from automated_checks import check_schema_valid, check_cited_figures_exist, check_percentage_tolerance

def derive_label(response, table, q1_correct_driver, q2_small_base_caveat):
    """
    response: the model's JSON output
    table: the table dict (with ground_truth)
    q1_correct_driver: human label, True/False — did it name the right driver?
    q2_small_base_caveat: human label, True/False/None — did it flag the small base?
                          (None if this table isn't a small-base table)
    """
    schema_ok, schema_msg = check_schema_valid(response)

    # Per the Appendix: an empty/null claimed_driver is a FAILED DRIVER CHECK,
    # not a schema violation. The field is present (schema passes), just
    # uninformative. We only run citation/tolerance checks if schema passed.
    if schema_ok:
        citations_ok, citations_msg = check_cited_figures_exist(response, table)
        tolerance_ok, tolerance_msg = check_percentage_tolerance(response, table)
    else:
        citations_ok, citations_msg = None, "skipped (schema invalid)"
        tolerance_ok, tolerance_msg = None, "skipped (schema invalid)"

    checks = {
        "schema_valid": schema_ok,
        "citations_exist": citations_ok,
        "percentage_in_tolerance": tolerance_ok,
        "correct_driver": q1_correct_driver,
        "small_base_caveat_present": q2_small_base_caveat,
    }

    # Precedence order determines the single final label
    if not schema_ok:
        final_label = "Contract violation"
    elif citations_ok is False:
        final_label = "Contract violation"  # bad citation = contract violation per Appendix
    elif q1_correct_driver is False:
        final_label = "Wrong driver"
    elif tolerance_ok is False:
        final_label = "Wrong number"
    elif table["small_base"] and q2_small_base_caveat is False:
        final_label = "Misleading small base"
    else:
        final_label = "Correct"

    return {
        "table_id": table["table_id"],
        "final_label": final_label,
        "checks": checks,
        "messages": {
            "schema": schema_msg,
            "citations": citations_msg,
            "tolerance": tolerance_msg
        }
    }


if __name__ == "__main__":
    import json
    with open("tables/real_tables.json") as f:
        tables = json.load(f)
    table = next(t for t in tables if t["table_id"] == "region_02")  # this is a small-base table

    print("=== Test 1: fully correct response, with caveat present ===")
    driver_name = table["ground_truth"]["true_driver"]
    true_pct = table["ground_truth"]["true_percentage_change"]
    driver_row = next(r for r in table["rows"] if r[table["columns"][0]] == driver_name)
    good = {"insight_sentence": f"{driver_name} was the main driver, from a small base.", "claimed_driver": driver_name,
            "claimed_percentage": true_pct, "cited_figures": [driver_row[table["columns"][1]], driver_row[table["columns"][2]]]}
    result = derive_label(good, table, q1_correct_driver=True, q2_small_base_caveat=True)
    print(json.dumps(result, indent=2))
    assert result["final_label"] == "Correct"

    print("\n=== Test 2: correct driver and number, but NO caveat on a small-base table ===")
    no_caveat = {"insight_sentence": f"{driver_name} grew the most.", "claimed_driver": driver_name,
                 "claimed_percentage": true_pct, "cited_figures": [driver_row[table["columns"][1]], driver_row[table["columns"][2]]]}
    result = derive_label(no_caveat, table, q1_correct_driver=True, q2_small_base_caveat=False)
    print(json.dumps(result, indent=2))
    assert result["final_label"] == "Misleading small base"

    print("\n=== Test 3: EDGE CASE — empty claimed_driver (named explicitly in the Appendix) ===")
    empty_driver = {"insight_sentence": "Revenue changed slightly.", "claimed_driver": "",
                    "claimed_percentage": true_pct, "cited_figures": [driver_row[table["columns"][1]], driver_row[table["columns"][2]]]}
    result = derive_label(empty_driver, table, q1_correct_driver=False, q2_small_base_caveat=None)
    print(json.dumps(result, indent=2))
    assert result["checks"]["schema_valid"] is True, "empty string must still PASS schema (it's present, just uninformative)"
    assert result["final_label"] == "Wrong driver", "empty driver should be scored as Wrong driver, not Contract violation"

    print("\n=== Test 4: schema violation (missing field entirely) ===")
    broken = {"claimed_driver": driver_name, "claimed_percentage": true_pct}
    result = derive_label(broken, table, q1_correct_driver=None, q2_small_base_caveat=None)
    print(json.dumps(result, indent=2))
    assert result["final_label"] == "Contract violation"

    print("\nAll 4 test cases passed, including the Appendix's named empty-driver edge case.")
