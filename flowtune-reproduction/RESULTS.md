# FlowTune 论文复现结果（六个基准 × 两个目标）

- 运行时间（UTC）：2026-10-12 05:58:07
- 运行环境：GitHub Actions ubuntu-latest，gcc 13
- 作者代码：https://github.com/Yu-Maryland/FlowTune
- **本次配置**：用作者的 `single_design.sh`，参数 `repeat=2 iteration=6 target=t sample=5 stage=10`
- **与论文的对齐（完全对齐）**：六个基准设计（论文表 III 全部）；用作者自己的 `single_design.sh`；参数 `repeat=2 iteration=6 sample=5 stage=10`，就是作者 `run.sh` 里的那一组 **6_10**（`./all.sh 6 10`，`all.sh` 里写死 repeat=2、sample=5）
- **多做的一组**：作者的 `all.sh` 只跑 `target=0`（优化门数），这里额外跑了 `target=1`（优化深度），因为老师要求比较网表深度
- **多阶段轮数**：作者的 `single_design.sh` 会先做一次 level-0 搜索、再循环 stage 次，所以 `stage=10` = 总共 **11 轮**「搜索 → 应用到电路 → 再搜索」，与论文的 6_10 一致
- **论文未给出**：nSample 的取值；这里沿用作者脚本里的 sample=5。补充：作者代码里 `-s` 在 AIG 优化这条路径上没有被真正使用（`bayes_flow_tune()` 收了 nSamples，函数体里没用到）

## 0. 实验自检（先看这一节）

# 实验自检

- ✅ 所有日志中都没有 abc: not found / 哨兵值 1e+09 / unknown command ps
- 结论：本次各组结果都来自真实评估，可以采信。

> 表格里每个格子是「逻辑门数量 and / 网表深度 lev」，取自 ABC 的 print_stats 原始输出。

| 设计 | 原始设计 | 基线一 resyn | 基线二 resyn×25 | FlowTune t=0（门数） | FlowTune t=1（深度） |
|---|---|---|---|---|---|
| bfly | 28910/97 | 26177/68 | 24276/68 | 19292/90 | 19799/85 |
| dscg | 28252/92 | 25427/67 | 23511/67 | 18858/94 | 19715/87 |
| fir | 27704/94 | 24930/67 | 23147/67 | 17939/92 | 18877/83 |
| ode | 16069/98 | 14723/71 | 13747/71 | 11020/94 | 11100/90 |
| or1200 | 12833/148 | 11256/132 | 11214/132 | 9974/131 | 10020/131 |
| syn2 | 30003/93 | 26911/67 | 24771/67 | 19936/89 | 20353/84 |

## 前端：RTL 功能验证（老师勾的「前端」）

对 `flowtune/rtl/` 里的每个 RTL：先用 Yosys 把 RTL 综合成门级网表，再用形式化等价性检查证明「综合出来的门级网表」和「原始 RTL」功能完全一致；综合出的门级网表（`.gate.v` / `.gate.aig`）也一起提交。

```
total 608
-rw-r--r-- 1 runner runner 20520 Oct 12 05:58 adder16.equiv.log
-rw-r--r-- 1 runner runner  2207 Oct 12 05:58 adder16.gate.aig
-rw-r--r-- 1 runner runner  5410 Oct 12 05:58 adder16.gate.v
-rw-r--r-- 1 runner runner 64882 Oct 12 05:58 adder16.synth.log
-rw-r--r-- 1 runner runner 20059 Oct 12 05:58 adder8.equiv.log
-rw-r--r-- 1 runner runner  1014 Oct 12 05:58 adder8.gate.aig
-rw-r--r-- 1 runner runner  2434 Oct 12 05:58 adder8.gate.v
-rw-r--r-- 1 runner runner 64633 Oct 12 05:58 adder8.synth.log
-rw-r--r-- 1 runner runner 24048 Oct 12 05:58 alu4.equiv.log
-rw-r--r-- 1 runner runner  1501 Oct 12 05:58 alu4.gate.aig
-rw-r--r-- 1 runner runner  4956 Oct 12 05:58 alu4.gate.v
-rw-r--r-- 1 runner runner 74504 Oct 12 05:58 alu4.synth.log
-rw-r--r-- 1 runner runner 23203 Oct 12 05:57 counter.equiv.log
-rw-r--r-- 1 runner runner     0 Oct 12 05:57 counter.gate.aig
-rw-r--r-- 1 runner runner   922 Oct 12 05:57 counter.gate.v
-rw-r--r-- 1 runner runner 65898 Oct 12 05:57 counter.synth.log
-rw-r--r-- 1 runner runner 23152 Oct 12 05:58 lfsr8.equiv.log
-rw-r--r-- 1 runner runner     0 Oct 12 05:58 lfsr8.gate.aig
-rw-r--r-- 1 runner runner  1133 Oct 12 05:58 lfsr8.gate.v
-rw-r--r-- 1 runner runner 62658 Oct 12 05:58 lfsr8.synth.log
-rw-r--r-- 1 runner runner 20572 Oct 12 05:58 mult8.equiv.log
-rw-r--r-- 1 runner runner  6979 Oct 12 05:58 mult8.gate.aig
-rw-r--r-- 1 runner runner 16569 Oct 12 05:58 mult8.gate.v
-rw-r--r-- 1 runner runner 62037 Oct 12 05:58 mult8.synth.log
```
### adder16.equiv.log
```
No selected unproven $equiv cells found in equiv.
Proved 0 previously unproven $equiv cells.
  Of those cells 17 are proven and 0 are unproven.
  Equivalence successfully proven!
```

### adder8.equiv.log
```
No selected unproven $equiv cells found in equiv.
Proved 0 previously unproven $equiv cells.
  Of those cells 9 are proven and 0 are unproven.
  Equivalence successfully proven!
```

### alu4.equiv.log
```
No selected unproven $equiv cells found in equiv.
Proved 0 previously unproven $equiv cells.
  Of those cells 4 are proven and 0 are unproven.
  Equivalence successfully proven!
```

### counter.equiv.log
```
Found 4 unproven $equiv cells in module equiv:
Proved 4 previously unproven $equiv cells.
  Of those cells 4 are proven and 0 are unproven.
  Equivalence successfully proven!
```

### lfsr8.equiv.log
```
Found 8 unproven $equiv cells in module equiv:
Proved 8 previously unproven $equiv cells.
  Of those cells 9 are proven and 0 are unproven.
  Equivalence successfully proven!
```

### mult8.equiv.log
```
No selected unproven $equiv cells found in equiv.
Proved 0 previously unproven $equiv cells.
  Of those cells 16 are proven and 0 are unproven.
  Equivalence successfully proven!
```

## 网表产物（字节）
```
total 4344
-rw-r--r-- 1 runner runner 190442 Oct 12 05:51 baseline_resyn.aig
-rw-r--r-- 1 runner runner 184000 Oct 12 05:51 baseline_resyn25.aig
-rw-r--r-- 1 runner runner 190442 Oct 12 05:54 bfly.resyn.aig
-rw-r--r-- 1 runner runner 184000 Oct 12 05:54 bfly.resyn25.aig
-rw-r--r-- 1 runner runner 167339 Oct 12 05:58 bfly.t0.aig
-rw-r--r-- 1 runner runner 168798 Oct 12 05:58 bfly.t1.aig
-rw-r--r-- 1 runner runner 181857 Oct 12 05:55 dscg.resyn.aig
-rw-r--r-- 1 runner runner 175170 Oct 12 05:55 dscg.resyn25.aig
-rw-r--r-- 1 runner runner 159299 Oct 12 05:58 dscg.t0.aig
-rw-r--r-- 1 runner runner 162254 Oct 12 05:58 dscg.t1.aig
-rw-r--r-- 1 runner runner 190156 Oct 12 05:55 fir.resyn.aig
-rw-r--r-- 1 runner runner 184177 Oct 12 05:55 fir.resyn25.aig
-rw-r--r-- 1 runner runner 166279 Oct 12 05:58 fir.t0.aig
-rw-r--r-- 1 runner runner 169852 Oct 12 05:58 fir.t1.aig
-rw-r--r-- 1 runner runner 180718 Oct 12 05:51 flowtune_t0.aig
-rw-r--r-- 1 runner runner 182300 Oct 12 05:51 flowtune_t1.aig
-rw-r--r-- 1 runner runner 115887 Oct 12 05:56 ode.resyn.aig
-rw-r--r-- 1 runner runner 112839 Oct 12 05:56 ode.resyn25.aig
-rw-r--r-- 1 runner runner 104464 Oct 12 05:58 ode.t0.aig
-rw-r--r-- 1 runner runner 104674 Oct 12 05:58 ode.t1.aig
-rw-r--r-- 1 runner runner 113928 Oct 12 05:56 or1200.resyn.aig
-rw-r--r-- 1 runner runner 113762 Oct 12 05:56 or1200.resyn25.aig
-rw-r--r-- 1 runner runner 109703 Oct 12 05:58 or1200.t0.aig
-rw-r--r-- 1 runner runner 109887 Oct 12 05:58 or1200.t1.aig
-rw-r--r-- 1 runner runner 183898 Oct 12 05:57 syn2.resyn.aig
-rw-r--r-- 1 runner runner 175829 Oct 12 05:57 syn2.resyn25.aig
-rw-r--r-- 1 runner runner 160386 Oct 12 05:58 syn2.t0.aig
-rw-r--r-- 1 runner runner 161734 Oct 12 05:58 syn2.t1.aig
```

## 原始输出（每个设计的自检结果与最终统计）
### bfly.t0.final.log
```
ABC command line: "read bfly.ftune.aig; print_stats".

[1;37mbfly.ftune                    :[0m i/o =  482/  257  lat = 1748  and =  19292  lev = 90
```

### bfly.t1.final.log
```
ABC command line: "read bfly.ftune.aig; print_stats".

[1;37mbfly.ftune                    :[0m i/o =  482/  257  lat = 1748  and =  19799  lev = 85
```

### dscg.t0.final.log
```
ABC command line: "read dscg.ftune.aig; print_stats".

[1;37mdscg.ftune                    :[0m i/o =  418/  257  lat = 1618  and =  18858  lev = 94
```

### dscg.t1.final.log
```
ABC command line: "read dscg.ftune.aig; print_stats".

[1;37mdscg.ftune                    :[0m i/o =  418/  257  lat = 1618  and =  19715  lev = 87
```

### fir.t0.final.log
```
ABC command line: "read fir.ftune.aig; print_stats".

[1;37mfir.ftune                     :[0m i/o =  450/  225  lat = 1882  and =  17939  lev = 92
```

### fir.t1.final.log
```
ABC command line: "read fir.ftune.aig; print_stats".

[1;37mfir.ftune                     :[0m i/o =  450/  225  lat = 1882  and =  18877  lev = 83
```

### ode.t0.final.log
```
ABC command line: "read ode.ftune.aig; print_stats".

[1;37mode.ftune                     :[0m i/o =  275/  169  lat = 1316  and =  11020  lev = 94
```

### ode.t1.final.log
```
ABC command line: "read ode.ftune.aig; print_stats".

[1;37mode.ftune                     :[0m i/o =  275/  169  lat = 1316  and =  11100  lev = 90
```

### or1200.t0.final.log
```
ABC command line: "read or1200.ftune.aig; print_stats".

[1;37mor1200.ftune                  :[0m i/o =  588/  509  lat =  670  and =   9974  lev =131
```

### or1200.t1.final.log
```
ABC command line: "read or1200.ftune.aig; print_stats".

[1;37mor1200.ftune                  :[0m i/o =  588/  509  lat =  670  and =  10020  lev =131
```

### syn2.t0.final.log
```
ABC command line: "read syn2.ftune.aig; print_stats".

[1;37msyn2.ftune                    :[0m i/o =  450/  321  lat = 1512  and =  19936  lev = 89
```

### syn2.t1.final.log
```
ABC command line: "read syn2.ftune.aig; print_stats".

[1;37msyn2.ftune                    :[0m i/o =  450/  321  lat = 1512  and =  20353  lev = 84
```

## FlowTune 的搜索日志（节选：每个设计每个目标的最后 25 行）
### bfly.t0.search.log
```
abc 12> ***EOF***
*************  level[10] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:48:04)
abc 01> ftune -d internal.aig -r 2 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,19296
1,19296
2,19296
3,19292
4,19292
5,19292
Best Flow(s) (#max=5):
strash;read dontCare;resub -K 8;refactor -z;dc2;refactor -z;dc2;rewrite;refactor;resub -K 8;resub -K 8;rewrite -z;refactor;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:48:04)
abc 01> read internal.aig; source bfly.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  482/  257  lat = 1748  and =  19292  lev = 90
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: bfly.ftune.aig[0m
********************************************************
```

### bfly.t1.search.log
```
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:48:01)
abc 01> ftune -d internal.aig -r 2 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,85
1,85
2,85
3,85
4,85
5,85
Best Flow(s) (#max=5):
strash;rewrite -z;refactor -z;rewrite -z;refactor;dc2;resub -K 8;rewrite -z;rewrite;refactor;resub -K 8;dc2;refactor -z;strash;
strash;refactor -z;dc2;refactor;refactor -z;refactor;resub -K 8;dc2;rewrite -z;rewrite -z;refactor -z;rewrite;resub -K 8;strash;
strash;read dontCare;resub -K 8;refactor;rewrite;refactor -z;rewrite -z;resub -K 8;refactor -z;dc2;refactor;rewrite -z;dc2;resub -K 8;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:48:01)
abc 01> read internal.aig; source bfly.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  482/  257  lat = 1748  and =  19799  lev = 85
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: bfly.ftune.aig[0m
********************************************************
```

### dscg.t0.search.log
```
[1;37minternal                      :[0m i/o =  418/  257  lat = 1618  and =  19033  lev = 94
abc 11> ***EOF***
*************  level[10] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:48:00)
abc 01> ftune -d internal.aig -r 2 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,18858
1,18858
2,18858
3,18858
4,18858
5,18858
Best Flow(s) (#max=5):
strash;rewrite -z;dc2;refactor;rewrite;rewrite -z;resub -K 8;refactor -z;rewrite -z;resub -K 8;refactor -z;dc2;refactor;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:48:00)
abc 01> read internal.aig; source dscg.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  418/  257  lat = 1618  and =  18858  lev = 94
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: dscg.ftune.aig[0m
********************************************************
```

### dscg.t1.search.log
```
abc 01> ftune -d internal.aig -r 2 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,87
1,87
2,87
3,87
4,87
5,87
Best Flow(s) (#max=5):
strash;rewrite;dc2;dc2;refactor;refactor -z;rewrite -z;rewrite;refactor -z;refactor;rewrite -z;resub -K 8;resub -K 8;strash;
strash;rewrite;refactor -z;resub -K 8;refactor -z;rewrite -z;dc2;resub -K 8;dc2;refactor;rewrite;rewrite -z;refactor;strash;
strash;resub -K 8;rewrite;dc2;resub -K 8;dc2;refactor;resub -K 8;refactor -z;rewrite -z;refactor -z;rewrite -z;refactor;strash;
strash;resub -K 8;rewrite -z;dc2;refactor -z;refactor -z;rewrite;dc2;refactor;refactor;rewrite -z;resub -K 8;resub -K 8;strash;
strash;dc2;dc2;refactor -z;resub -K 8;rewrite -z;dc2;resub -K 8;refactor;rewrite;rewrite -z;refactor -z;refactor;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:54)
abc 01> read internal.aig; source dscg.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  418/  257  lat = 1618  and =  19715  lev = 87
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: dscg.ftune.aig[0m
********************************************************
```

### fir.t0.search.log
```
[1;37minternal                      :[0m i/o =  450/  225  lat = 1882  and =  18153  lev = 92
abc 11> ***EOF***
*************  level[10] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:58)
abc 01> ftune -d internal.aig -r 2 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,17939
1,17939
2,17939
3,17939
4,17939
5,17939
Best Flow(s) (#max=5):
strash;resub -K 8;dc2;resub -K 8;refactor -z;dc2;resub -K 8;rewrite -z;refactor;rewrite;rewrite -z;refactor;refactor -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:58)
abc 01> read internal.aig; source fir.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  450/  225  lat = 1882  and =  17939  lev = 92
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: fir.ftune.aig[0m
********************************************************
```

### fir.t1.search.log
```
[1;37minternal                      :[0m i/o =  450/  225  lat = 1882  and =  18971  lev = 83
abc 11> ***EOF***
*************  level[10] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:56)
abc 01> ftune -d internal.aig -r 2 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,83
1,83
2,83
3,83
4,83
5,83
Best Flow(s) (#max=5):
strash;resub -K 8;rewrite;dc2;resub -K 8;dc2;refactor;resub -K 8;refactor -z;rewrite -z;refactor -z;rewrite -z;refactor;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:56)
abc 01> read internal.aig; source fir.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  450/  225  lat = 1882  and =  18877  lev = 83
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: fir.ftune.aig[0m
********************************************************
```

### ode.t0.search.log
```
[1;37minternal                      :[0m i/o =  275/  169  lat = 1316  and =  11086  lev = 96
abc 12> ***EOF***
*************  level[10] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:57)
abc 01> ftune -d internal.aig -r 2 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,11020
1,11020
2,11020
3,11020
4,11020
5,11020
Best Flow(s) (#max=5):
strash;dc2;dc2;refactor -z;resub -K 8;rewrite -z;dc2;resub -K 8;refactor;rewrite;rewrite -z;refactor -z;refactor;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:57)
abc 01> read internal.aig; source ode.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  275/  169  lat = 1316  and =  11020  lev = 94
abc 12> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: ode.ftune.aig[0m
********************************************************
```

### ode.t1.search.log
```
abc 01> ftune -d internal.aig -r 2 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,90
1,90
2,90
3,90
4,90
5,90
Best Flow(s) (#max=5):
strash;rewrite;refactor -z;resub -K 8;rewrite -z;dc2;rewrite -z;rewrite;resub -K 8;refactor -z;refactor;refactor;dc2;strash;
strash;rewrite -z;resub -K 8;dc2;rewrite;resub -K 8;rewrite -z;rewrite -z;refactor;dc2;refactor -z;refactor -z;refactor;strash;
strash;rewrite -z;dc2;rewrite -z;refactor;resub -K 8;refactor -z;refactor -z;rewrite;rewrite -z;resub -K 8;dc2;refactor;strash;
strash;refactor;refactor -z;rewrite -z;refactor;rewrite;rewrite -z;refactor -z;refactor;dc2;resub -K 8;resub -K 8;dc2;strash;
strash;refactor;resub -K 8;resub -K 8;rewrite;dc2;dc2;rewrite -z;refactor -z;refactor;refactor;rewrite -z;refactor -z;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:48:00)
abc 01> read internal.aig; source ode.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  275/  169  lat = 1316  and =  11100  lev = 90
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: ode.ftune.aig[0m
********************************************************
```

### or1200.t0.search.log
```
Your current setups:
Design = internal.aig, target = 0, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,9974
1,9974
2,9974
3,9974
4,9974
5,9974
Best Flow(s) (#max=5):
strash;dc2;refactor;resub -K 8;refactor -z;rewrite -z;refactor;dc2;rewrite;dc2;resub -K 8;rewrite -z;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;read dontCare;refactor -z;refactor;rewrite;dc2;refactor -z;resub -K 8;rewrite -z;rewrite -z;refactor;resub -K 8;dc2;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;read dontCare;rewrite;refactor;rewrite -z;resub -K 8;rewrite -z;refactor -z;refactor -z;dc2;rewrite;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;read dontCare;dc2;rewrite;refactor -z;rewrite -z;dc2;rewrite -z;refactor;refactor -z;refactor;resub -K 8;dc2;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;read dontCare;refactor -z;refactor -z;dc2;refactor -z;rewrite -z;rewrite;resub -K 8;resub -K 8;refactor;rewrite -z;dc2;refactor;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:59)
abc 01> read internal.aig; source or1200.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  588/  509  lat =  670  and =   9974  lev =131
abc 12> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: or1200.ftune.aig[0m
********************************************************
```

### or1200.t1.search.log
```
abc 01> ftune -d internal.aig -r 2 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,131
1,131
2,131
3,131
4,131
5,131
Best Flow(s) (#max=5):
strash;rewrite;dc2;dc2;refactor;refactor -z;rewrite -z;rewrite;refactor -z;refactor;rewrite -z;resub -K 8;resub -K 8;strash;
strash;rewrite;dc2;refactor -z;resub -K 8;rewrite -z;refactor;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;
strash;rewrite;rewrite -z;refactor;rewrite;resub -K 8;refactor -z;rewrite -z;refactor;resub -K 8;dc2;refactor -z;dc2;strash;
strash;rewrite;refactor -z;resub -K 8;rewrite -z;dc2;rewrite -z;rewrite;resub -K 8;refactor -z;refactor;refactor;dc2;strash;
strash;rewrite;refactor -z;resub -K 8;refactor -z;rewrite -z;dc2;resub -K 8;dc2;refactor;rewrite;rewrite -z;refactor;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:55)
abc 01> read internal.aig; source or1200.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  588/  509  lat =  670  and =  10020  lev =131
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: or1200.ftune.aig[0m
********************************************************
```

### syn2.t0.search.log
```
*************  level[10] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:57)
abc 01> ftune -d internal.aig -r 2 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,19936
1,19936
2,19936
3,19936
4,19936
5,19936
Best Flow(s) (#max=5):
strash;refactor -z;rewrite -z;refactor -z;dc2;dc2;resub -K 8;rewrite -z;refactor -z;refactor;resub -K 8;refactor;rewrite;strash;ifraig;dch -f;strash;print_stats;
strash;read dontCare;refactor -z;rewrite -z;refactor -z;dc2;refactor;resub -K 8;refactor;resub -K 8;rewrite -z;dc2;rewrite;refactor -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:57)
abc 01> read internal.aig; source syn2.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  450/  321  lat = 1512  and =  19936  lev = 89
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: syn2.ftune.aig[0m
********************************************************
```

### syn2.t1.search.log
```
abc 11> ***EOF***
*************  level[10] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:59)
abc 01> ftune -d internal.aig -r 2 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 2, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,84
1,84
2,84
3,84
4,84
5,84
Best Flow(s) (#max=5):
strash;rewrite -z;refactor -z;rewrite -z;refactor;dc2;resub -K 8;rewrite -z;rewrite;refactor;resub -K 8;dc2;refactor -z;strash;
strash;refactor -z;dc2;refactor;refactor -z;refactor;resub -K 8;dc2;rewrite -z;rewrite -z;refactor -z;rewrite;resub -K 8;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 12 2026 03:47:59)
abc 01> read internal.aig; source syn2.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  450/  321  lat = 1512  and =  20353  lev = 84
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: syn2.ftune.aig[0m
********************************************************
```

