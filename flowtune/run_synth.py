"""后端接口：用 Yosys 跑一条综合流程，返回门数和关键路径深度。

一条完整的流程 = 读入设计 -> 粗粒度综合 -> 三个阶段各自选一个配方 -> 统计。
"""

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 优先用环境变量指定的 yosys；否则用本机 pip 装的 yowasp-yosys（免安装的 WebAssembly 版）
def find_yosys() -> str:
    if os.environ.get("YOSYS"):
        return os.environ["YOSYS"]
    # 1) PATH 里有没有 yosys / yowasp-yosys
    for name in ("yowasp-yosys", "yosys"):
        found = shutil.which(name)
        if found:
            return found
    # 2) 当前 Python 环境的 Scripts 目录（pip 装出来的可执行文件都在这里）
    local = Path(sys.executable).parent / "Scripts" / "yowasp-yosys.exe"
    if local.exists():
        return str(local)
    # 3) 兜底：在 Codex 运行时目录里搜一遍（版本更新后路径会变，所以用通配符找）
    for pattern in (
        r"C:\Users\12239\.cache\codex-runtimes\*\*\python\Scripts\yowasp-yosys.exe",
        r"C:\Users\12239\.cache\codex-runtimes\*\*\*\python\Scripts\yowasp-yosys.exe",
        r"C:\Users\12239\AppData\Local\Programs\Python\**\Scripts\yowasp-yosys.exe",
    ):
        hits = sorted(glob.glob(pattern, recursive=True))
        if hits:
            return str(hits[-1])
    return "yosys"


YOSYS = find_yosys()
_CACHE: dict[tuple[str, str], dict] = {}

_CELLS_RE = re.compile(r"^\s+(\d+)\s+cells\s*$", re.M)
_DEPTH_RE = re.compile(r"length=(\d+)")


def load_config() -> dict:
    return json.loads((HERE / "recipes.json").read_text(encoding="utf-8"))


def build_script(design: dict, arms: list[str], cfg: dict) -> str:
    """把三个阶段和固定的映射步骤拼成一条 Yosys 脚本。

    stages 的顺序是：阶段1 → 阶段2 → [固定映射] → 阶段3 …，映射步骤对所有组合都一样，
    这样比较的才是"优化配方的选择"，而不是"有没有做门级映射"。
    """
    parts = [
        f"read_verilog {design['file']}",
        f"synth -top {design['top']} -run :fine",
    ]
    map_after = cfg.get("map_after_stage")
    for index, arm in enumerate(arms, start=1):
        parts.append(arm)
        if map_after is not None and index == map_after:
            parts.append(cfg["map_step"])
    parts.extend(["ltp", "stat"])
    return "; ".join(parts)


def run_flow(design: dict, arms: list[str], cfg: dict | None = None) -> dict:
    """按给定的多阶段配方跑一次综合，返回 {cells, depth, seconds, command}。"""
    cfg = cfg or load_config()
    key = (design["name"], " | ".join(arms))
    if key in _CACHE:
        return _CACHE[key]

    script = build_script(design, arms, cfg)
    start = time.time()
    proc = subprocess.run(
        [YOSYS, "-p", script],
        cwd=HERE,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    seconds = time.time() - start
    log = proc.stdout + proc.stderr

    cells_match = _CELLS_RE.search(log)
    depth_match = _DEPTH_RE.search(log)
    result = {
        "design": design["name"],
        "arms": arms,
        "cells": int(cells_match.group(1)) if cells_match else None,
        "depth": int(depth_match.group(1)) if depth_match else None,
        "seconds": round(seconds, 2),
        "ok": proc.returncode == 0 and cells_match is not None,
    }
    if not result["ok"]:
        result["tail"] = log.strip().splitlines()[-3:]
    _CACHE[key] = result
    return result


if __name__ == "__main__":
    cfg = load_config()
    design = cfg["designs"][1]
    default = [stage["arms"][0] for stage in cfg["stages"]]
    got = run_flow(design, default, cfg)
    print(json.dumps({**got, "script": build_script(design, default, cfg)}, ensure_ascii=False, indent=2))
