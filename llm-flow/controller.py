#!/usr/bin/env python3

import argparse
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path


MAX_COMMANDS = 10
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ALLOWED = SCRIPT_DIR / "allowed_commands.json"
DEFAULT_PROMPT = SCRIPT_DIR / "depth_prompt.txt"
DEFAULT_REFERENCE = SCRIPT_DIR / "flowtune_t1_reference.json"

STATS_RE = re.compile(
    r"i/o\s*=\s*(\d+)\s*/\s*(\d+).*?"
    r"lat\s*=\s*(\d+).*?"
    r"and\s*=\s*(\d+).*?"
    r"lev\s*=\s*(\d+)"
)


def normalize_command(command):
    return " ".join(command.strip().split())


def parse_stats(output):
    matches = STATS_RE.findall(output)
    if not matches:
        raise RuntimeError("Could not parse ABC print_stats output.")
    inputs, outputs, latches, and_gates, levels = matches[-1]
    return {
        "inputs": int(inputs),
        "outputs": int(outputs),
        "latches": int(latches),
        "and_gates": int(and_gates),
        "levels": int(levels),
    }


def run_abc(abc, script, timeout):
    started = time.perf_counter()
    result = subprocess.run(
        [abc, "-c", script],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise RuntimeError(
            f"ABC failed with code {result.returncode}:\n{output[-4000:]}"
        )
    return output, round(time.perf_counter() - started, 3)


def create_original(abc, benchmark, output_path, timeout):
    script = (
        f"read {benchmark}; "
        "strash; "
        f"write {output_path}; "
        "print_stats; "
        "quit"
    )
    output, seconds = run_abc(abc, script, timeout)
    return parse_stats(output), output, seconds


def evaluate_commands(abc, original, commands, output_path, timeout):
    transform = "; ".join(commands)
    script = (
        f"read {original}; "
        "strash; "
        f"{transform}; "
        "strash; "
        "ifraig; "
        "dch -f; "
        "strash; "
        "print_stats; "
        f"write {output_path}; "
        "quit"
    )
    output, seconds = run_abc(abc, script, timeout)
    return {
        "commands": commands,
        "command_count": len(commands),
        "output": str(output_path),
        "seconds": seconds,
        "metrics": parse_stats(output),
    }


def measure_fixed_baseline(abc, original, output_path, log_path, timeout):
    script = (
        f"read {original}; "
        "strash; "
        "ifraig; "
        "dch -f; "
        "strash; "
        "print_stats; "
        f"write {output_path}; "
        "quit"
    )
    output, seconds = run_abc(abc, script, timeout)
    log_path.write_text(output, encoding="utf-8")
    return {
        "seconds": seconds,
        "metrics": parse_stats(output),
    }


def verify_equivalence(abc, original, optimized, timeout):
    output, seconds = run_abc(
        abc,
        f"dsec -n {original} {optimized}; quit",
        timeout,
    )
    return {
        "equivalent": "Networks are equivalent" in output,
        "seconds": seconds,
        "output": output.strip(),
    }


def chat_completions_url(base_url):
    url = base_url.rstrip("/")
    if url.endswith("/chat/completions"):
        return url
    return url + "/chat/completions"


def request_llm(base_url, api_key, model, system_prompt, user_prompt, temperature, max_tokens, timeout):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    request = urllib.request.Request(
        chat_completions_url(base_url),
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "gdut-llm-flow/1.0",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))

    content = body["choices"][0]["message"]["content"]
    return {
        "content": content,
        "usage": body.get("usage", {}),
        "model": body.get("model", model),
    }


def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("No JSON object found in the LLM response.")
    return json.loads(text[start : end + 1])


def validate_candidates(content, allowed, requested_count):
    value = extract_json(content)
    candidates = value.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("Response must contain a candidates list.")

    valid = []
    for item in candidates:
        if not isinstance(item, dict):
            continue
        commands = item.get("commands")
        if not isinstance(commands, list) or not commands:
            continue
        if not all(isinstance(command, str) for command in commands):
            continue

        normalized = [normalize_command(command) for command in commands]
        if len(normalized) > MAX_COMMANDS:
            continue
        if any(command not in allowed for command in normalized):
            continue
        valid.append(normalized)
        if len(valid) >= requested_count:
            break

    if not valid:
        raise ValueError("No valid candidate passed validation.")
    return valid


def build_user_prompt(design, original_metrics, allowed, history, requested_count, search_id):
    compact_history = sorted(
        history,
        key=lambda item: (
            item["metrics"]["levels"],
            item["metrics"]["and_gates"],
            item["seconds"],
        ),
    )[:10]

    return json.dumps(
        {
            "task": "Propose distinct ABC command flows that reduce AIG depth.",
            "design": design,
            "search_id": search_id,
            "original_metrics": original_metrics,
            "allowed_commands": sorted(allowed),
            "maximum_commands_per_candidate": MAX_COMMANDS,
            "number_of_candidates_requested": requested_count,
            "ranking_rule": [
                "lower levels is better",
                "for equal levels, lower and_gates is better",
            ],
            "top_history": [
                {
                    "commands": item["commands"],
                    "levels": item["metrics"]["levels"],
                    "and_gates": item["metrics"]["and_gates"],
                }
                for item in compact_history
            ],
        },
        ensure_ascii=False,
        indent=2,
    )


def llm_request_with_retry(args, system_prompt, user_prompt, call_log):
    error = None
    for attempt in range(1, 4):
        try:
            response = request_llm(
                args.base_url,
                args.api_key,
                args.model,
                system_prompt,
                user_prompt,
                args.temperature,
                args.max_tokens,
                args.api_timeout,
            )
            call_log.append(
                {
                    "attempt": attempt,
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                    "response": response,
                }
            )
            return response
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as exc:
            error = exc
            time.sleep(2**attempt)
    raise RuntimeError(f"LLM request failed after retries: {error}")


def search_repeat(args, allowed, system_prompt, original, original_metrics, repeat_dir, repeat_index):
    repeat_dir.mkdir(parents=True, exist_ok=True)
    call_log = []
    results = []
    seen = set()
    rounds = 0
    max_rounds = max(30, (args.candidates_per_repeat // args.batch_size + 1) * 6)

    while len(results) < args.candidates_per_repeat and rounds < max_rounds:
        remaining = args.candidates_per_repeat - len(results)
        requested = min(args.batch_size, remaining)
        user_prompt = build_user_prompt(
            args.design,
            original_metrics,
            allowed,
            results,
            requested,
            f"repeat-{repeat_index}-round-{rounds + 1}",
        )
        candidates = None
        validation_error = None
        for validation_attempt in range(1, 4):
            retry_prompt = user_prompt
            if validation_error is not None:
                retry_prompt += (
                    "\n\nYour previous response was invalid: "
                    + str(validation_error)
                    + "\nReturn valid JSON with the required candidates list."
                )
            response = llm_request_with_retry(
                args,
                system_prompt,
                retry_prompt,
                call_log,
            )
            try:
                candidates = validate_candidates(
                    response["content"],
                    allowed,
                    requested,
                )
                break
            except ValueError as error:
                validation_error = error

        if candidates is None:
            rounds += 1
            print(
                f"repeat={repeat_index} round={rounds} "
                f"invalid_response={validation_error}",
                flush=True,
            )
            time.sleep(min(10, rounds))
            continue
        accepted = 0
        for commands in candidates:
            signature = tuple(commands)
            if signature in seen:
                continue
            seen.add(signature)
            candidate_index = len(results) + 1
            output_aig = repeat_dir / f"candidate-{candidate_index:03d}.aig"
            try:
                report = evaluate_commands(
                    args.abc,
                    original,
                    commands,
                    output_aig,
                    args.abc_timeout,
                )
                report["candidate_index"] = candidate_index
                results.append(report)
                accepted += 1
            except Exception as error:
                results.append(
                    {
                        "candidate_index": candidate_index,
                        "commands": commands,
                        "error": str(error),
                    }
                )
            if len(results) >= args.candidates_per_repeat:
                break

        rounds += 1
        print(
            f"repeat={repeat_index} round={rounds} "
            f"tested={len(results)} accepted={accepted}",
            flush=True,
        )

    successful = [item for item in results if "error" not in item]
    successful.sort(
        key=lambda item: (
            item["metrics"]["levels"],
            item["metrics"]["and_gates"],
            item["seconds"],
        )
    )
    if not successful:
        raise RuntimeError("No successful candidates in repeat.")

    best = successful[0]
    verification = verify_equivalence(
        args.abc,
        original,
        best["output"],
        args.abc_timeout,
    )

    (repeat_dir / "llm_calls.json").write_text(
        json.dumps(call_log, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (repeat_dir / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    usage = {
        "prompt_tokens": sum(
            item["response"].get("usage", {}).get("prompt_tokens", 0)
            for item in call_log
        ),
        "completion_tokens": sum(
            item["response"].get("usage", {}).get("completion_tokens", 0)
            for item in call_log
        ),
        "total_tokens": sum(
            item["response"].get("usage", {}).get("total_tokens", 0)
            for item in call_log
        ),
    }

    return {
        "repeat": repeat_index,
        "tested": len(results),
        "successful": len(successful),
        "best": best,
        "verification": verification,
        "usage": usage,
    }


def markdown_report(summary, reference):
    lines = [
        f"# {summary['design']} LLM Flow Result",
        "",
        f"- Model: `{summary['model']}`",
        f"- Temperature: `{summary['temperature']}`",
        f"- Candidates per repeat: `{summary['candidates_per_repeat']}`",
        f"- Repeats: `{summary['repeats']}`",
        f"- Fixed evaluation baseline: `lev={summary['fixed_baseline']['metrics']['levels']}, "
        f"and={summary['fixed_baseline']['metrics']['and_gates']}`",
        "",
        "| Repeat | lev | and | Equivalent | Total tokens | Best commands |",
        "|---:|---:|---:|---|---:|---|",
    ]
    for item in summary["repeat_results"]:
        best = item["best"]
        lines.append(
            f"| {item['repeat']} "
            f"| {best['metrics']['levels']} "
            f"| {best['metrics']['and_gates']} "
            f"| {item['verification']['equivalent']} "
            f"| {item['usage']['total_tokens']} "
            f"| `{'; '.join(best['commands'])}` |"
        )

    best_repeat = min(
        summary["repeat_results"],
        key=lambda item: (
            item["best"]["metrics"]["levels"],
            item["best"]["metrics"]["and_gates"],
        ),
    )["best"]
    lines.extend(
        [
            "",
            f"Overall best: `lev={best_repeat['metrics']['levels']}, "
            f"and={best_repeat['metrics']['and_gates']}`",
            "",
            f"FlowTune t=1 reference: `lev={reference['levels']}, "
            f"and={reference['and_gates']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--abc", required=True)
    parser.add_argument("--benchmark", required=True)
    parser.add_argument("--design", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--candidates-per-repeat", type=int, default=64)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=4000)
    parser.add_argument("--api-timeout", type=float, default=120)
    parser.add_argument("--abc-timeout", type=float, default=600)
    parser.add_argument("--base-url", default=os.getenv("LLM_BASE_URL", "https://api.deepseek.com"))
    parser.add_argument("--api-key", default=os.getenv("LLM_API_KEY", ""))
    parser.add_argument("--model", default=os.getenv("LLM_MODEL", "deepseek-v4-flash"))
    parser.add_argument("--allowed-file", default=str(DEFAULT_ALLOWED))
    parser.add_argument("--prompt-file", default=str(DEFAULT_PROMPT))
    parser.add_argument("--reference-file", default=str(DEFAULT_REFERENCE))
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("LLM_API_KEY is missing.")
    if args.candidates_per_repeat <= 0 or args.repeats <= 0 or args.batch_size <= 0:
        raise SystemExit("Experiment sizes must be positive.")

    allowed = {
        normalize_command(item)
        for item in json.loads(Path(args.allowed_file).read_text(encoding="utf-8"))
    }
    system_prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    reference = json.loads(Path(args.reference_file).read_text(encoding="utf-8"))[
        args.design
    ]

    output_dir = Path(args.output_dir).resolve()
    original_dir = output_dir / "original"
    original_dir.mkdir(parents=True, exist_ok=True)
    original_aig = original_dir / f"{args.design}.orig.aig"
    original_metrics, original_log, original_seconds = create_original(
        args.abc,
        args.benchmark,
        original_aig,
        args.abc_timeout,
    )
    (original_dir / "original.log").write_text(original_log, encoding="utf-8")

    fixed_baseline = measure_fixed_baseline(
        args.abc,
        original_aig,
        output_dir / "baseline.after_fixed_eval.aig",
        output_dir / "baseline.after_fixed_eval.log",
        args.abc_timeout,
    )

    repeat_results = []
    for repeat_index in range(1, args.repeats + 1):
        repeat_results.append(
            search_repeat(
                args,
                allowed,
                system_prompt,
                original_aig,
                original_metrics,
                output_dir / f"repeat-{repeat_index:02d}",
                repeat_index,
            )
        )

    summary = {
        "design": args.design,
        "benchmark": args.benchmark,
        "model": args.model,
        "temperature": args.temperature,
        "candidates_per_repeat": args.candidates_per_repeat,
        "repeats": args.repeats,
        "original": {
            "metrics": original_metrics,
            "seconds": original_seconds,
        },
        "fixed_baseline": fixed_baseline,
        "repeat_results": repeat_results,
        "flowtune_t1": reference,
    }

    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "SUMMARY.md").write_text(
        markdown_report(summary, reference),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
