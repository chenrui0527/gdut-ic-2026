# FlowTune 论文复现结果（按高鹏老师要求）

- 运行时间（UTC）：2026-10-06 15:59:28
- 运行环境：GitHub Actions ubuntu-latest，gcc 13
- 作者代码：https://github.com/Yu-Maryland/FlowTune
- 基准设计：`bfly.abc.blif`（论文用的六个 VTR 基准之一）
- 参数：ftune `-r 1 -i 5 -s 5`，t=0 优化门数，t=1 优化深度
- 老师要求：① 得到逻辑综合的网表 ② 比较逻辑门数量和网表深度 ③ 先不用跑布线

## 1. 结果对照表

| 做法 | 逻辑门数量 (and) | 网表深度 (lev) | 网表文件大小 (字节) |
|---|---|---|---|
| 基线一：ABC 默认 resyn | 26177 | 68 | 190442 |
| 基线二：resyn 连续 25 次 | 24276 | 68 | 184000 |
| FlowTune（目标 t=0 最小化门数） | 23711 | 87 | 182229 |
| FlowTune（目标 t=1 最小化深度） | 23711 | 87 | 182229 |

说明：`and` 是 ABC 统计出的 AIG 与门节点数，代表逻辑门数量；`lev` 是逻辑级数，代表网表深度。两者都来自 ABC 的 `print_stats` 原始输出。

## 原始输出：基线一
```
ABC command line: "read bfly.abc.blif; resyn; strash; print_stats; write baseline_resyn.aig".

Hierarchy reader converted 4 instances of blackboxes.
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  26177  lev = 68
```

## 原始输出：基线二
```
ABC command line: "read bfly.abc.blif; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; resyn; strash; print_stats; write baseline_resyn25.aig".

Hierarchy reader converted 4 instances of blackboxes.
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  24276  lev = 68
```

## 原始输出：FlowTune-t0-search
```
UC Berkeley, ABC 1.01 (compiled Oct  6 2026 15:57:52)
abc 01> ftune -d bfly.abc.blif -r 1 -t 0 -p 1 -i 5 -s 5
rm: cannot remove '.temp.result.txt': No such file or directory
rm: cannot remove 'bfly.abc.blif.log': No such file or directory
Your current setups:
Design = bfly.abc.blif, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 5, nSample = 5, liberty = (null)
begin:abc -c "read bfly.abc.blif;strash;
sh: 1: abc: not found
sh: 1: sh: 1: sh: 1: abc: not foundabc: not foundabc: not found


sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
0,1e+09
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: abc: not found
sh: 1: abc: not found
1,1e+09
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: abc: not foundsh: 1: 
abc: not found
2,1e+09
sh: 1: sh: 1: sh: 1: abc: not foundabc: not foundabc: not found


sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
3,1e+09
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: abc: not found
sh: 1: abc: not found
4,1e+09
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
```

## 原始输出：FlowTune-t0-应用
```
ABC command line: "read bfly.abc.blif; source chosen_t0.script; strash; print_stats; write flowtune_t0.aig".

Hierarchy reader converted 4 instances of blackboxes.
Hierarchy reader converted 4 instances of blackboxes.
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  23711  lev = 87
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  23711  lev = 87
```

## 原始输出：FlowTune-t1-search
```
UC Berkeley, ABC 1.01 (compiled Oct  6 2026 15:57:52)
abc 01> ftune -d bfly.abc.blif -r 1 -t 1 -p 1 -i 5 -s 5
Your current setups:
Design = bfly.abc.blif, target = 1, repeats = 1, prefix = 1, forget = 0, iteration = 5, nSample = 5, liberty = (null)
begin:abc -c "read bfly.abc.blif;strash;
sh: 1: sh: 1: sh: 1: abc: not foundabc: not foundsh: 1: abc: not found

abc: not found

sh: 1: sh: 1: sh: 1: abc: not foundabc: not foundabc: not found


sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
0,1e+09
sh: 1: sh: 1: abc: not foundabc: not found
sh: 1: 
sh: 1: abc: not foundabc: not found

sh: 1: abc: not found
sh: 1: abc: not found
1,1e+09
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
2,1e+09
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
sh: 1: abc: not found
3,1e+09
sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: sh: 1: abc: not foundabc: not found

sh: 1: sh: 1: abc: not foundabc: not found

4,1e+09
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;
strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;
abc 01> ***EOF***
```

## 原始输出：FlowTune-t1-应用
```
ABC command line: "read bfly.abc.blif; source chosen_t1.script; strash; print_stats; write flowtune_t1.aig".

Hierarchy reader converted 4 instances of blackboxes.
Hierarchy reader converted 4 instances of blackboxes.
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  23711  lev = 87
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  23711  lev = 87
```

## FlowTune 搜索出的候选流程（原始）
```
--- t=0（最小化门数）---
read bfly.abc.blif;strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
read bfly.abc.blif;strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
read bfly.abc.blif;strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
read bfly.abc.blif;strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
read bfly.abc.blif;strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
--- t=1（最小化深度）---
read bfly.abc.blif;strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
read bfly.abc.blif;strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
read bfly.abc.blif;strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
read bfly.abc.blif;strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
read bfly.abc.blif;strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
```

## 网表产物
```
total 728
-rw-r--r-- 1 runner runner 190442 Oct  6 15:59 baseline_resyn.aig
-rw-r--r-- 1 runner runner 184000 Oct  6 15:59 baseline_resyn25.aig
-rw-r--r-- 1 runner runner 182229 Oct  6 15:59 flowtune_t0.aig
-rw-r--r-- 1 runner runner 182229 Oct  6 15:59 flowtune_t1.aig
```
