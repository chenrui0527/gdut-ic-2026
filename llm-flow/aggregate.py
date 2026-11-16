#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: aggregate.py <download-dir> <output-dir>")

    download_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    for path in sorted(download_dir.rglob("summary.json")):
        summaries.append(json.loads(path.read_text(encoding="utf-8")))

    summaries.sort(key=lambda item: item["design"])
    lines = [
        "# LLM-Guided ABC Flow Search",
        "",
        "| Design | Baseline lev | LLM best lev | FlowTune t=1 lev | LLM and | FlowTune and | Equivalent | Best commands |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]

    for summary in summaries:
        best_repeat = min(
            summary["repeat_results"],
            key=lambda item: (
                item["best"]["metrics"]["levels"],
                item["best"]["metrics"]["and_gates"],
            ),
        )
        best = best_repeat["best"]
        reference = summary["flowtune_t1"]
        equivalent = all(
            item["verification"]["equivalent"]
            for item in summary["repeat_results"]
        )
        lines.append(
            f"| {summary['design']} "
            f"| {summary['fixed_baseline']['metrics']['levels']} "
            f"| {best['metrics']['levels']} "
            f"| {reference['levels']} "
            f"| {best['metrics']['and_gates']} "
            f"| {reference['and_gates']} "
            f"| {equivalent} "
            f"| `{'; '.join(best['commands'])}` |"
        )

    (output_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (output_dir / "summary.json").write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
