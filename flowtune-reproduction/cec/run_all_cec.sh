#!/usr/bin/env bash
# 一次跑完全部 24 组网表一致性检测：6 个设计 × 4 个优化后网表（resyn / resyn25 / t0 / t1）。
#
# 用途：把云端那次一致性检测在本地重跑一遍（命令和云端完全一样：cec + dsec，-n 表示按顺序对应）。
#
# 用法（在 WSL 里跑）：
#   bash run_all_cec.sh [并行数] [网表目录] [输出目录]
#   默认：并行 6；网表在 /mnt/c/Users/12239/AppData/Local/Temp/cec-netlists；日志写到 /tmp/cec-logs
#
# 依赖：
#   /root/FlowTune/src/build/abc                （FlowTune 版 ABC，已编译）
#   /root/FlowTune/Benchmarks/BLIF/*.abc.blif   （六个设计的输入网表）
#   网表目录里的 <设计>.<resyn|resyn25|t0|t1>.aig（从仓库 flowtune-reproduction/netlists 复制过来）

set -u

JOBS=${1:-6}
NET=${2:-/mnt/c/Users/12239/AppData/Local/Temp/cec-netlists}
OUT=${3:-/tmp/cec-logs}
ABC=/root/FlowTune/src/build/abc
BLIF=/root/FlowTune/Benchmarks/BLIF
DESIGNS="bfly dscg fir ode or1200 syn2"
KS="resyn resyn25 t0 t1"

[ -x "$ABC" ] || { echo "找不到可执行的 abc：$ABC"; exit 1; }
[ -f "$BLIF/bfly.abc.blif" ] || { echo "找不到输入网表：$BLIF"; exit 1; }

mkdir -p "$OUT"
cd "$OUT" || exit 1

echo "===== 第一步：给每个设计生成「输入网表」并打印规模 ====="
for d in $DESIGNS; do
  "$ABC" -c "read $BLIF/$d.abc.blif; strash; print_stats; write $d.orig.aig" > "$OUT/$d.orig.log" 2>&1
  printf '%-8s %s\n' "$d" "$(grep -E 'and =' "$OUT/$d.orig.log" | tail -1 | sed 's/^ *//')"
done

echo
echo "===== 第二步：24 组 cec + dsec（$JOBS 路并行） ====="
run_one() {
  d=$1; k=$2
  f="$NET/$d.$k.aig"
  if [ ! -f "$f" ]; then echo "  缺少 $f"; return; fi
  "$ABC" -c "cec -n $d.orig.aig $f"  > "$OUT/$d.$k.cec.log"  2>&1
  "$ABC" -c "dsec -n $d.orig.aig $f" > "$OUT/$d.$k.dsec.log" 2>&1
  printf '  %-8s %-8s cec=%-14s dsec=%s\n' "$d" "$k" \
    "$(grep -oE 'Networks are (equivalent|NOT EQUIVALENT|UNDECIDED)' "$OUT/$d.$k.cec.log" | head -1 | sed 's/Networks are //')" \
    "$(grep -oE 'Networks are (equivalent|NOT EQUIVALENT|UNDECIDED)' "$OUT/$d.$k.dsec.log" | head -1 | sed 's/Networks are //')"
}
export -f run_one
export ABC NET OUT

START=$(date +%s)
for d in $DESIGNS; do for k in $KS; do echo "$d $k"; done; done | xargs -n2 -P "$JOBS" bash -c 'run_one "$@"' _
echo "第二步用时 $(( $(date +%s) - START )) 秒"

echo
echo "================= 汇总表 ================="
printf '%-8s %-9s %-18s %-18s\n' design netlist cec dsec
for d in $DESIGNS; do
  for k in $KS; do
    c=$(grep -oE 'Networks are (equivalent|NOT EQUIVALENT|UNDECIDED)' "$OUT/$d.$k.cec.log" 2>/dev/null | head -1)
    s=$(grep -oE 'Networks are (equivalent|NOT EQUIVALENT|UNDECIDED)' "$OUT/$d.$k.dsec.log" 2>/dev/null | head -1)
    printf '%-8s %-9s %-18s %-18s\n' "$d" "$k" "${c:-见日志}" "${s:-见日志}"
  done
done
echo
echo "每组的完整日志在 $OUT"
