"""论文核心算法的复现：多阶段多臂老虎机（multistage multi-armed bandit）。

论文（FlowTune, IEEE TCAD 2023）把"综合流程优化"建模成一个多阶段的多臂老虎机问题：
流程分成若干阶段，每一阶段从若干候选配方里挑一个，整条流程跑完得到的结果（QoR，比如面积）
作为奖励反馈，用来更新被选中的那些臂。本脚本用 UCB1 实现这个循环，环境就是 Yosys 真实综合。
"""

import csv
import json
import math
import random
from pathlib import Path

from run_synth import HERE, load_config, run_flow

ROUNDS = 30          # 每个设计跑多少轮
UCB_C = 1.2          # UCB 里的探索系数，越大越爱试没试过的配方


def pick_arm(stats: dict, total: int, rng: random.Random) -> int:
    """UCB1：没试过的臂先试；否则按 平均奖励 + c*sqrt(ln N / n) 选。"""
    for index, stat in enumerate(stats):
        if stat["n"] == 0:
            return index
    best_index, best_score = 0, -1e9
    for index, stat in enumerate(stats):
        mean = stat["sum"] / stat["n"]
        bonus = UCB_C * math.sqrt(math.log(total + 1) / stat["n"])
        score = mean + bonus + rng.random() * 1e-6   # 微小扰动避免平局总选同一个
        if score > best_score:
            best_index, best_score = index, score
    return best_index


def run_bandit(design: dict, stages: list[dict], cfg: dict, baseline_cells: int, rounds: int, seed: int) -> dict:
    rng = random.Random(seed)
    stats = [[{"n": 0, "sum": 0.0} for _ in stage["arms"]] for stage in stages]
    history = []
    best = None
    total = 0

    for round_index in range(1, rounds + 1):
        chosen = [pick_arm(stats[s], total, rng) for s in range(len(stages))]
        arms = [stages[s]["arms"][chosen[s]] for s in range(len(stages))]
        result = run_flow(design, arms, cfg)
        if not result["ok"]:
            continue

        # 奖励 = 相对默认流程（三个阶段都用第一个配方）省下来的门数比例
        reward = (baseline_cells - result["cells"]) / baseline_cells
        total += 1
        for stage_index, arm_index in enumerate(chosen):
            stats[stage_index][arm_index]["n"] += 1
            stats[stage_index][arm_index]["sum"] += reward

        history.append(
            {
                "round": round_index,
                "cells": result["cells"],
                "depth": result["depth"],
                "reward": round(reward, 4),
                "arms": arms,
                "seconds": result["seconds"],
            }
        )
        if best is None or result["cells"] < best["cells"]:
            best = {"round": round_index, "cells": result["cells"], "depth": result["depth"], "arms": arms}

    return {
        "design": design["name"],
        "rounds": rounds,
        "baseline_cells": baseline_cells,
        "best": best,
        "history": history,
        "stage_means": [
            [
                {
                    "arm": stages[s]["arms"][i],
                    "n": stat["n"],
                    "mean_reward": round(stat["sum"] / stat["n"], 4) if stat["n"] else None,
                }
                for i, stat in enumerate(stats[s])
            ]
            for s in range(len(stages))
        ],
    }


def evaluate_fixed(design: dict, stages: list[dict], cfg: dict) -> dict:
    """把所有配方组合穷举一遍，作为"标准答案"（组合数不大时可行）。"""
    import itertools

    best = None
    tried = 0
    for combo in itertools.product(*[stage["arms"] for stage in stages]):
        result = run_flow(design, list(combo), cfg)
        tried += 1
        if not result["ok"]:
            continue
        if best is None or result["cells"] < best["cells"]:
            best = {"cells": result["cells"], "depth": result["depth"], "arms": list(combo)}
    return {"tried": tried, "best": best}


def main() -> None:
    cfg = load_config()
    stages = cfg["stages"]
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    summary = []

    for design in cfg["designs"]:
        default_arms = [stage["arms"][0] for stage in stages]
        baseline = run_flow(design, default_arms, cfg)
        print(f"[{design['name']}] 默认流程门数 = {baseline['cells']}")

        bandit = run_bandit(design, stages, cfg, baseline["cells"], ROUNDS, seed=7)
        full = evaluate_fixed(design, stages, cfg)

        print(
            f"[{design['name']}] 老虎机 {ROUNDS} 轮找到最好: {bandit['best']['cells']} 门"
            f"（第 {bandit['best']['round']} 轮）；穷举全部 {full['tried']} 种组合的最好:"
            f" {full['best']['cells']} 门"
        )
        print(f"[{design['name']}] 最优配方: {' | '.join(bandit['best']['arms'])}")

        summary.append(
            {
                "design": design["name"],
                "baseline_cells": baseline["cells"],
                "bandit_best_cells": bandit["best"]["cells"],
                "bandit_best_round": bandit["best"]["round"],
                "full_search_best_cells": full["best"]["cells"],
                "combinations": full["tried"],
                "bandit": bandit,
                "full_search": full,
            }
        )

        with (out_dir / f"{design['name']}_history.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["round", "cells", "depth", "reward", "seconds", "arms"])
            writer.writeheader()
            for row in bandit["history"]:
                writer.writerow({**row, "arms": " | ".join(row["arms"])})

    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("结果已写入 results/summary.json 与 results/*_history.csv")


if __name__ == "__main__":
    main()
