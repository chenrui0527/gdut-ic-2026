"""论文核心算法的复现：多阶段多臂老虎机 + 跨设计迁移（domain-specific 领域知识的代理实现）。

论文（FlowTune, IEEE TCAD 2023, Cunxi Yu）把"综合流程优化"建模成一个多阶段多臂老虎机：
流程分成若干阶段，每一阶段从若干候选配方里挑一个，整条流程跑完得到的结果（QoR，比如面积）
作为奖励反馈，用来更新被选中的那些臂；标题里的 domain-specific 强调"用领域知识指导搜索"。

本脚本做两件事：
1) run_bandit：复现多阶段老虎机循环（冷启动，每个设计从零开始学）；
2) run_transfer：实现"跨设计经验迁移"——把一个设计学到的臂统计作为下一个设计的先验，
   这正是论文"领域知识"思想的一个可运行代理实现（学到的东西不必每个设计重来一次）。
环境就是真实的 Yosys 综合，奖励就是真实跑出来的门数。
"""

import copy
import csv
import itertools
import json
import math
import random
from pathlib import Path

from run_synth import HERE, load_config, run_flow

ROUNDS = 30      # 每个设计跑多少轮
UCB_C = 1.2      # UCB 的探索系数，越大越爱试没试过的配方


def pick_arm(stats: list[dict], total: int, rng: random.Random) -> int:
    """UCB1：没试过的臂先试；否则按 平均奖励 + c*sqrt(ln N / n) 选。"""
    for index, stat in enumerate(stats):
        if stat["n"] == 0:
            return index
    best_index, best_score = 0, -1e9
    for index, stat in enumerate(stats):
        mean = stat["sum"] / stat["n"]
        bonus = UCB_C * math.sqrt(math.log(total + 1) / stat["n"])
        score = mean + bonus + rng.random() * 1e-6
        if score > best_score:
            best_index, best_score = index, score
    return best_index


def new_stats(stages: list[dict]) -> list[list[dict]]:
    return [[{"n": 0, "sum": 0.0} for _ in stage["arms"]] for stage in stages]


def play_rounds(design, stages, cfg, stats, baseline_cells, best_known, rounds, rng):
    """在给定的臂统计上跑若干轮（统计里可以带先验）。

    返回：每轮历史、找到的最好结果、以及"第几次评估第一次达到已知最优"。
    """
    history = []
    best = None
    evals = 0
    evals_to_best = None
    # 先验里已有的次数也要算进 UCB 的总次数，否则探索项会被高估
    total = sum(stat["n"] for stage in stats for stat in stage)

    for round_index in range(1, rounds + 1):
        chosen = [pick_arm(stats[s], total, rng) for s in range(len(stages))]
        arms = [stages[s]["arms"][chosen[s]] for s in range(len(stages))]
        result = run_flow(design, arms, cfg)
        if not result["ok"]:
            continue

        evals += 1
        total += 1
        reward = (baseline_cells - result["cells"]) / baseline_cells
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
        if evals_to_best is None and best_known is not None and result["cells"] <= best_known:
            evals_to_best = evals

    return {"history": history, "best": best, "evals": evals, "evals_to_best": evals_to_best}


def run_bandit(design, stages, cfg, baseline_cells, best_known, rounds, seed):
    """冷启动：每个设计的臂统计都从零开始（= 没有迁移任何经验）。"""
    rng = random.Random(seed)
    stats = new_stats(stages)
    outcome = play_rounds(design, stages, cfg, stats, baseline_cells, best_known, rounds, rng)
    return {
        "design": design["name"],
        "mode": "cold",
        "rounds": rounds,
        "baseline_cells": baseline_cells,
        "best": outcome["best"],
        "evals": outcome["evals"],
        "evals_to_best": outcome["evals_to_best"],
        "history": outcome["history"],
        "stages": [[{"arm": stages[s]["arms"][i], "n": st["n"], "mean_reward": (round(st["sum"] / st["n"], 4) if st["n"] else None)}
                    for i, st in enumerate(stats[s])] for s in range(len(stages))],
    }


def weaken(prior):
    """把累计经验压成"每个臂一条虚拟观测"（n=1，奖励取平均），避免先验过强导致负迁移。"""
    weak = []
    for stage in prior:
        weak.append([
            {"n": 1, "sum": stat["sum"] / stat["n"]} if stat["n"] else {"n": 0, "sum": 0.0}
            for stat in stage
        ])
    return weak


def run_transfer(designs, stages, cfg, baselines, best_known, rounds, seed, weak_prior=True):
    """迁移：按顺序处理设计，把前面所有设计积累的臂统计当作下一个设计的先验。

    weak_prior=True 时把先验压缩成一条虚拟观测（n=1），只做"轻推一把"，
    避免前一个设计的偏好过强、反而把新设计带偏（负迁移）。
    """
    rng = random.Random(seed)
    prior = new_stats(stages)      # 跨设计累积的经验
    results = []
    for design in designs:
        stats = weaken(prior) if weak_prior else copy.deepcopy(prior)
        outcome = play_rounds(
            design, stages, cfg, stats, baselines[design["name"]], best_known[design["name"]], rounds, rng
        )
        # 把本设计这一轮的统计并回先验，供后面的设计使用
        for s in range(len(stages)):
            for a in range(len(stages[s]["arms"])):
                prior[s][a]["n"] += stats[s][a]["n"]
                prior[s][a]["sum"] += stats[s][a]["sum"]
        results.append(
            {
                "design": design["name"],
                "mode": "transfer",
                "rounds": rounds,
                "baseline_cells": baselines[design["name"]],
                "best": outcome["best"],
                "evals": outcome["evals"],
                "evals_to_best": outcome["evals_to_best"],
                "history": outcome["history"],
            }
        )
    return results, prior


def evaluate_fixed(design, stages, cfg):
    """穷举所有配方组合，得到"标准答案"（组合数不大时才可行）。"""
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
    designs = cfg["designs"]
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)

    baselines = {}
    best_known = {}
    exhaustive = {}
    for design in designs:
        default_arms = [stage["arms"][0] for stage in stages]
        baselines[design["name"]] = run_flow(design, default_arms, cfg)["cells"]
        full = evaluate_fixed(design, stages, cfg)
        exhaustive[design["name"]] = full
        best_known[design["name"]] = full["best"]["cells"]
        print(
            f"[{design['name']}] 默认 {baselines[design['name']]} 门；"
            f"穷举 {full['tried']} 种组合的最优 = {full['best']['cells']} 门"
        )

    # 多个随机种子重复，避免"一次运行碰巧命中"的结论
    SEEDS = list(range(1, 11))
    names = [d["name"] for d in designs]
    modes = ("cold", "transfer_weak", "transfer_strong")
    collected = {mode: {n: [] for n in names} for mode in modes}
    representative = {}

    for seed in SEEDS:
        cold = [run_bandit(d, stages, cfg, baselines[d["name"]], best_known[d["name"]], ROUNDS, seed=seed) for d in designs]
        weak, _ = run_transfer(designs, stages, cfg, baselines, best_known, ROUNDS, seed=seed, weak_prior=True)
        strong, prior = run_transfer(designs, stages, cfg, baselines, best_known, ROUNDS, seed=seed, weak_prior=False)
        for record in cold:
            collected["cold"][record["design"]].append(record["evals_to_best"])
        for record in weak:
            collected["transfer_weak"][record["design"]].append(record["evals_to_best"])
        for record in strong:
            collected["transfer_strong"][record["design"]].append(record["evals_to_best"])
        if seed == 7:
            representative = {"cold": cold, "transfer_weak": weak, "transfer_strong": strong}
        print(f"  seed {seed} 完成")

    def summarize(values):
        """没命中的记成 ROUNDS+1（超过预算），再报中位数、平均和命中率。"""
        filled = sorted(v if v is not None else ROUNDS + 1 for v in values)
        hits = sum(1 for v in values if v is not None)
        return {
            "median": filled[len(filled) // 2],
            "mean": round(sum(filled) / len(filled), 2),
            "min": filled[0],
            "max": filled[-1],
            "hit_rate": f"{hits}/{len(values)}",
        }

    print("\n设计          默认门数  穷举最优   冷启动中位数  弱迁移中位数  强迁移中位数")
    for name in names:
        summary_row = {mode: summarize(collected[mode][name]) for mode in modes}
        print(
            f"{name:<13} {baselines[name]:>6} {best_known[name]:>8} "
            f"{summary_row['cold']['median']:>13} {summary_row['transfer_weak']['median']:>13} "
            f"{summary_row['transfer_strong']['median']:>13}"
        )

    print("\n命中率（10 个种子中多少次在预算内找到穷举最优）")
    for name in names:
        row = {mode: summarize(collected[mode][name]) for mode in modes}
        print(
            f"{name:<13} 冷启动 {row['cold']['hit_rate']:>6}   弱迁移 {row['transfer_weak']['hit_rate']:>6}   "
            f"强迁移 {row['transfer_strong']['hit_rate']:>6}"
        )

    for mode, records in representative.items():
        for record in records:
            path = out_dir / f"{record['design']}_{mode}_history.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["round", "cells", "depth", "reward", "seconds", "arms"])
                writer.writeheader()
                for row in record["history"]:
                    writer.writerow({**row, "arms": " | ".join(row["arms"])})

    summary = {
        "rounds_per_design": ROUNDS,
        "ucb_c": UCB_C,
        "seeds": SEEDS,
        "designs": names,
        "stages": [{"name": s["name"], "arms": s["arms"]} for s in stages],
        "baseline_cells": baselines,
        "exhaustive_best_cells": best_known,
        "evals_to_best": {
            mode: {name: summarize(collected[mode][name]) for name in names} for mode in modes
        },
        "final_prior_stats": [[{"arm": stages[s]["arms"][i], "n": st["n"],
                                "mean_reward": (round(st["sum"] / st["n"], 4) if st["n"] else None)}
                               for i, st in enumerate(prior[s])] for s in range(len(stages))],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n结果已写入 results/summary.json 与 results/*_history.csv")


if __name__ == "__main__":
    main()
