#!/usr/bin/env python3

import argparse
import concurrent.futures
import json
import subprocess
import time
from pathlib import Path


def run_recheck(abc, budget_root, summary_path, repeat_result, timeout):
    best = repeat_result["best"]
    candidate_name = Path(best["output"]).name
    candidate_path = summary_path.parent / f"repeat-{repeat_result['repeat']:02d}" / candidate_name
    original_path = summary_path.parent / "original" / "fir.orig.aig"
    started = time.perf_counter()
    result = subprocess.run(
        [
            abc,
            "-c",
            f"dsec -n -T 600 {original_path} {candidate_path}; quit",
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=summary_path.parent,
    )
    output = result.stdout + result.stderr
    return {
        "budget": int(budget_root.name),
        "repeat": repeat_result["repeat"],
        "candidate": candidate_name,
        "lev": best["metrics"]["levels"],
        "and": best["metrics"]["and_gates"],
        "equivalent": "Networks are equivalent" in output,
        "seconds": round(time.perf_counter() - started, 3),
        "output": output.strip(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--abc", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--timeout", type=float, default=900)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    jobs = []

    for budget_root in sorted(root.iterdir(), key=lambda path: path.name):
        if not budget_root.is_dir():
            continue
        for summary_path in sorted(budget_root.rglob("summary.json")):
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if summary.get("design") != "fir":
                continue
            for repeat_result in summary["repeat_results"]:
                if not repeat_result["verification"]["equivalent"]:
                    jobs.append((budget_root, summary_path, repeat_result))

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [
            pool.submit(
                run_recheck,
                args.abc,
                budget_root,
                summary_path,
                repeat_result,
                args.timeout,
            )
            for budget_root, summary_path, repeat_result in jobs
        ]
        results = [future.result() for future in futures]

    results.sort(key=lambda item: (item["budget"], item["repeat"]))
    root.mkdir(parents=True, exist_ok=True)
    (root / "fir_reverification.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# fir checkpoint equivalence recheck",
        "",
        "| Budget | Repeat | lev | and | Seconds | Equivalent |",
        "|---:|---:|---:|---:|---:|---|",
    ]
    for item in results:
        lines.append(
            f"| {item['budget']} | {item['repeat']} | {item['lev']} | "
            f"{item['and']} | {item['seconds']} | {item['equivalent']} |"
        )
    (root / "FIR_REVERIFICATION.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
