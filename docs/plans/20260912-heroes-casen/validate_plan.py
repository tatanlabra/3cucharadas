#!/usr/bin/env python3
"""Validate the planning package, not the implemented site or survey estimates."""
import copy
import fnmatch
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def validate(contract):
    tasks = {task["id"]: task for task in contract["tasks"]}
    require(len(tasks) == len(contract["tasks"]), "duplicate_task")
    ancestry = {}

    def visit(task_id, chain=()):
        require(task_id not in chain, "dependency_cycle")
        require(task_id in tasks, "missing_dependency")
        if task_id in ancestry:
            return ancestry[task_id]
        result = set()
        task = tasks[task_id]
        for dependency in task["depends_on"] + task.get("acceptance_depends_on", []):
            result.add(dependency)
            result.update(visit(dependency, chain + (task_id,)))
        ancestry[task_id] = result
        return result

    for task_id, task in tasks.items():
        require(bool(task["owner"] and task["provider"]), "missing_owner")
        require(task["status"] == "pending" and task["evidence"] is None, "unearned_done")
        require(contract["todo_state"][task_id] == "[ ]", "unearned_todo")
        visit(task_id)
        for criterion in task["acceptance"]:
            require(criterion["kind"] in ("shell", "manual_review"), "invalid_acceptance_kind")
            if criterion["kind"] == "shell":
                require(bool(criterion.get("command")) and not criterion["command"].startswith("read "), "prose_as_shell")
            else:
                require(bool(criterion.get("required_artifact_fields") and criterion.get("digest_check")) and "command" not in criterion, "invalid_manual_review")
        require((ROOT / "briefings" / f"{task_id}.md").is_file(), "missing_briefing")

    overlaps = []
    for index, left in enumerate(contract["tasks"]):
        for right in contract["tasks"][index + 1:]:
            shared = any(
                x == y or fnmatch.fnmatchcase(x, y) or fnmatch.fnmatchcase(y, x)
                for x in left["write_scope"] for y in right["write_scope"]
            )
            if shared:
                require(left["id"] in ancestry[right["id"]] or right["id"] in ancestry[left["id"]], "unordered_writer_collision")
                overlaps.append([left["id"], right["id"]])

    require(contract["limits"]["max_active_agents_including_root"] <= contract["limits"]["hard_session_ceiling"], "capacity_exceeded")
    require(contract["limits"]["external_publication"] is False, "publication_not_authorized")
    for phase in contract["phases"]:
        for key in ["objective", "inputs", "outputs", "invariants", "falsification", "rollback"]:
            require(bool(phase.get(key)), "phase_field_missing")

    e1 = tasks["E1"]["acceptance"]
    require(e1[0]["id"] == "AC-E0" and "jekyll build" in e1[0]["command"], "stale_build_risk")
    require("U1" in tasks["H1"].get("acceptance_depends_on", []), "mutable_checker_race")
    require(set(tasks["V1"]["depends_on"]) == {"D2", "V0"}, "unreviewed_figure_data")
    return {"task_count": len(tasks), "phase_count": len(contract["phases"]), "ordered_overlapping_scopes": overlaps}

def main():
    contract = json.loads((ROOT / "contract.json").read_text())
    positive = validate(contract)
    negative = []
    for case in ["dependency_cycle", "missing_owner", "unordered_writer_collision", "prose_as_shell", "stale_build_risk", "mutable_checker_race"]:
        broken = copy.deepcopy(contract)
        tasks = {task["id"]: task for task in broken["tasks"]}
        if case == "dependency_cycle":
            tasks["P0"]["depends_on"] = ["Q1"]
        elif case == "missing_owner":
            tasks["P0"]["owner"] = ""
        elif case == "unordered_writer_collision":
            tasks["D1"]["write_scope"].append("_includes/page__hero.html")
        elif case == "prose_as_shell":
            tasks["R1"]["acceptance"][0].update(kind="shell", command="read review findings")
        elif case == "stale_build_risk":
            tasks["E1"]["acceptance"] = tasks["E1"]["acceptance"][1:]
        else:
            tasks["H1"]["acceptance_depends_on"] = []
        try:
            validate(broken)
        except ValueError as exc:
            require(str(exc) == case, f"unexpected_negative_result:{case}:{exc}")
            negative.append({"case": case, "observed": "rejected", "reason": str(exc)})
        else:
            raise ValueError(f"negative_accepted:{case}")

    hashes = {}
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and path.suffix in {".json", ".md", ".py"} and path.name != "plan-validation.json":
            for line in path.read_text().splitlines():
                require(line == line.rstrip(), f"trailing_whitespace:{path.name}")
            hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    report = {
        "scope": "plan structure only; not implementation, security isolation, survey validity or optimality",
        "limitations": ["path-glob overlap check covers declared patterns, not arbitrary future paths", "manual review criteria require human or agent judgment", "pending-only checker is for this planning snapshot; execution must update state validation"],
        "positive": positive,
        "negative_controls": negative,
        "artifact_hashes": hashes,
        "product_checks": "not_run",
        "provider_reviews": {"astra": "completed", "claude": "not_run", "gemini": "not_run"}
    }
    (ROOT / "plan-validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"result": "PASS_PLAN_STRUCTURE", "tasks": positive["task_count"], "negative_controls_rejected": len(negative), "product_checks": "not_run"}))

if __name__ == "__main__":
    main()
