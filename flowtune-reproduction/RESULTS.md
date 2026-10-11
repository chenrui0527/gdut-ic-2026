# FlowTune 论文复现结果（六个基准 × 两个目标）

- 运行时间（UTC）：2026-10-11 10:27:04
- 运行环境：GitHub Actions ubuntu-latest，gcc 13
- 作者代码：https://github.com/Yu-Maryland/FlowTune
- **本次配置**：用作者的 `single_design.sh`，参数 `repeat=1 iteration=6 target=t sample=5 stage=2`
- **与论文的对齐**：六个基准设计（论文表 III 全部）；两个优化目标（t=0 门数 / t=1 深度）；用作者自己的脚本；多阶段结构；iteration=6 与论文的 6_10 那一组一致
- **多阶段轮数**：用作者的 `single_design.sh`，它会先做一次 level-0 搜索再循环 stage 次，所以 `stage=2` 表示总共 **3 轮**（论文 6_10 那组是 11 轮）
- **缩小的部分**：stage 从论文的 10 缩到 2（3 轮 vs 11 轮）。作者原配置一个设计一个目标要两个多小时，六个设计 × 两个目标就是十几个小时，一次运行内做不完
- **论文未给出**：nSample 的取值；这里沿用作者脚本里的 sample=5

## 0. 实验自检（先看这一节）

# 实验自检

- ✅ 所有日志中都没有 abc: not found / 哨兵值 1e+09 / unknown command ps
- 结论：本次各组结果都来自真实评估，可以采信。

> 表格里每个格子是「逻辑门数量 and / 网表深度 lev」，取自 ABC 的 print_stats 原始输出。

| 设计 | 原始设计 | 基线一 resyn | 基线二 resyn×25 | FlowTune t=0（门数） | FlowTune t=1（深度） |
|---|---|---|---|---|---|
| bfly | 28910/97 | 26177/68 | 24276/68 | 21634/88 | 22132/86 |
| dscg | 28252/92 | 25427/67 | 23511/67 | 21180/88 | 21870/76 |
| fir | 27704/94 | 24930/67 | 23147/67 | 20630/90 | 21051/82 |
| ode | 16069/98 | 14723/71 | 13747/71 | 12364/92 | 12737/89 |
| or1200 | 12833/148 | 11256/132 | 11214/132 | 10159/132 | 10198/130 |
| syn2 | 30003/93 | 26911/67 | 24771/67 | 22534/85 | 23085/80 |

## 网表产物（字节）
```
total 4412
-rw-r--r-- 1 runner runner 190442 Oct 11 10:23 baseline_resyn.aig
-rw-r--r-- 1 runner runner 184000 Oct 11 10:23 baseline_resyn25.aig
-rw-r--r-- 1 runner runner 190442 Oct 11 10:24 bfly.resyn.aig
-rw-r--r-- 1 runner runner 184000 Oct 11 10:24 bfly.resyn25.aig
-rw-r--r-- 1 runner runner 174610 Oct 11 10:27 bfly.t0.aig
-rw-r--r-- 1 runner runner 176070 Oct 11 10:27 bfly.t1.aig
-rw-r--r-- 1 runner runner 181857 Oct 11 10:25 dscg.resyn.aig
-rw-r--r-- 1 runner runner 175170 Oct 11 10:25 dscg.resyn25.aig
-rw-r--r-- 1 runner runner 167047 Oct 11 10:27 dscg.t0.aig
-rw-r--r-- 1 runner runner 168943 Oct 11 10:27 dscg.t1.aig
-rw-r--r-- 1 runner runner 190156 Oct 11 10:25 fir.resyn.aig
-rw-r--r-- 1 runner runner 184177 Oct 11 10:25 fir.resyn25.aig
-rw-r--r-- 1 runner runner 175941 Oct 11 10:27 fir.t0.aig
-rw-r--r-- 1 runner runner 177361 Oct 11 10:27 fir.t1.aig
-rw-r--r-- 1 runner runner 180718 Oct 11 10:23 flowtune_t0.aig
-rw-r--r-- 1 runner runner 182300 Oct 11 10:23 flowtune_t1.aig
-rw-r--r-- 1 runner runner 115887 Oct 11 10:26 ode.resyn.aig
-rw-r--r-- 1 runner runner 112839 Oct 11 10:26 ode.resyn25.aig
-rw-r--r-- 1 runner runner 108693 Oct 11 10:27 ode.t0.aig
-rw-r--r-- 1 runner runner 109780 Oct 11 10:27 ode.t1.aig
-rw-r--r-- 1 runner runner 113928 Oct 11 10:26 or1200.resyn.aig
-rw-r--r-- 1 runner runner 113762 Oct 11 10:26 or1200.resyn25.aig
-rw-r--r-- 1 runner runner 110411 Oct 11 10:27 or1200.t0.aig
-rw-r--r-- 1 runner runner 110566 Oct 11 10:27 or1200.t1.aig
-rw-r--r-- 1 runner runner 183898 Oct 11 10:27 syn2.resyn.aig
-rw-r--r-- 1 runner runner 175829 Oct 11 10:27 syn2.resyn25.aig
-rw-r--r-- 1 runner runner 168456 Oct 11 10:27 syn2.t0.aig
-rw-r--r-- 1 runner runner 170409 Oct 11 10:27 syn2.t1.aig
```

## 原始输出（每个设计的自检结果与最终统计）
### bfly.t0.final.log
```
ABC command line: "read bfly.ftune.aig; print_stats".

[1;37mbfly.ftune                    :[0m i/o =  482/  257  lat = 1748  and =  21634  lev = 88
```

### bfly.t1.final.log
```
ABC command line: "read bfly.ftune.aig; print_stats".

[1;37mbfly.ftune                    :[0m i/o =  482/  257  lat = 1748  and =  22132  lev = 86
```

### dscg.t0.final.log
```
ABC command line: "read dscg.ftune.aig; print_stats".

[1;37mdscg.ftune                    :[0m i/o =  418/  257  lat = 1618  and =  21180  lev = 88
```

### dscg.t1.final.log
```
ABC command line: "read dscg.ftune.aig; print_stats".

[1;37mdscg.ftune                    :[0m i/o =  418/  257  lat = 1618  and =  21870  lev = 76
```

### fir.t0.final.log
```
ABC command line: "read fir.ftune.aig; print_stats".

[1;37mfir.ftune                     :[0m i/o =  450/  225  lat = 1882  and =  20630  lev = 90
```

### fir.t1.final.log
```
ABC command line: "read fir.ftune.aig; print_stats".

[1;37mfir.ftune                     :[0m i/o =  450/  225  lat = 1882  and =  21051  lev = 82
```

### ode.t0.final.log
```
ABC command line: "read ode.ftune.aig; print_stats".

[1;37mode.ftune                     :[0m i/o =  275/  169  lat = 1316  and =  12364  lev = 92
```

### ode.t1.final.log
```
ABC command line: "read ode.ftune.aig; print_stats".

[1;37mode.ftune                     :[0m i/o =  275/  169  lat = 1316  and =  12737  lev = 89
```

### or1200.t0.final.log
```
ABC command line: "read or1200.ftune.aig; print_stats".

[1;37mor1200.ftune                  :[0m i/o =  588/  509  lat =  670  and =  10159  lev =132
```

### or1200.t1.final.log
```
ABC command line: "read or1200.ftune.aig; print_stats".

[1;37mor1200.ftune                  :[0m i/o =  588/  509  lat =  670  and =  10198  lev =130
```

### syn2.t0.final.log
```
ABC command line: "read syn2.ftune.aig; print_stats".

[1;37msyn2.ftune                    :[0m i/o =  450/  321  lat = 1512  and =  22534  lev = 85
```

### syn2.t1.final.log
```
ABC command line: "read syn2.ftune.aig; print_stats".

[1;37msyn2.ftune                    :[0m i/o =  450/  321  lat = 1512  and =  23085  lev = 80
```

## FlowTune 的搜索日志（节选：每个设计每个目标的最后 25 行）
### bfly.t0.search.log
```
abc 11> ***EOF***
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:18)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,21659
1,21659
2,21659
3,21659
4,21659
5,21634
Best Flow(s) (#max=5):
strash;read dontCare;dc2;rewrite -z;resub -K 8;refactor;refactor -z;dc2;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:18)
abc 01> read internal.aig; source bfly.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  482/  257  lat = 1748  and =  21634  lev = 88
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: bfly.ftune.aig[0m
********************************************************
```

### bfly.t1.search.log
```
Your current setups:
Design = internal.aig, target = 1, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,86
1,86
2,86
3,86
4,86
5,86
Best Flow(s) (#max=5):
strash;rewrite -z;refactor;rewrite -z;resub -K 8;dc2;refactor -z;strash;
strash;rewrite -z;rewrite -z;refactor -z;dc2;resub -K 8;refactor;strash;
strash;rewrite -z;refactor;refactor -z;resub -K 8;rewrite -z;dc2;strash;
strash;refactor;resub -K 8;refactor;refactor -z;dc2;rewrite -z;strash;
strash;read dontCare;rewrite -z;resub -K 8;rewrite -z;refactor -z;refactor;dc2;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:19)
abc 01> read internal.aig; source bfly.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  482/  257  lat = 1748  and =  22132  lev = 86
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: bfly.ftune.aig[0m
********************************************************
```

### dscg.t0.search.log
```
abc 11> ***EOF***
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:17)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,21209
1,21209
2,21180
3,21180
4,21180
5,21180
Best Flow(s) (#max=5):
strash;read dontCare;dc2;refactor;refactor -z;rewrite -z;dc2;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:17)
abc 01> read internal.aig; source dscg.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  418/  257  lat = 1618  and =  21180  lev = 88
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: dscg.ftune.aig[0m
********************************************************
```

### dscg.t1.search.log
```
[1;37minternal                      :[0m i/o =  418/  257  lat = 1618  and =  22345  lev = 73
abc 10> ***EOF***
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:17)
abc 01> ftune -d internal.aig -r 1 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,76
1,76
2,76
3,76
4,76
5,76
Best Flow(s) (#max=5):
strash;resub -K 8;refactor -z;resub -K 8;dc2;refactor;rewrite -z;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:17)
abc 01> read internal.aig; source dscg.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  418/  257  lat = 1618  and =  21870  lev = 76
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: dscg.ftune.aig[0m
********************************************************
```

### fir.t0.search.log
```
abc 11> ***EOF***
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:22)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,20644
1,20644
2,20630
3,20630
4,20630
5,20630
Best Flow(s) (#max=5):
strash;read dontCare;dc2;rewrite -z;refactor -z;resub -K 8;dc2;refactor;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:22)
abc 01> read internal.aig; source fir.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  450/  225  lat = 1882  and =  20630  lev = 90
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: fir.ftune.aig[0m
********************************************************
```

### fir.t1.search.log
```
Your current setups:
Design = internal.aig, target = 1, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,82
1,82
2,82
3,82
4,82
5,82
Best Flow(s) (#max=5):
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;
strash;refactor;resub -K 8;refactor;refactor -z;dc2;rewrite -z;strash;
strash;refactor -z;dc2;rewrite -z;refactor -z;resub -K 8;refactor;strash;
strash;read dontCare;refactor -z;refactor;resub -K 8;refactor -z;dc2;rewrite -z;strash;
strash;read dontCare;rewrite -z;dc2;rewrite -z;refactor -z;refactor;resub -K 8;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:20)
abc 01> read internal.aig; source fir.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  450/  225  lat = 1882  and =  21051  lev = 82
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: fir.ftune.aig[0m
********************************************************
```

### ode.t0.search.log
```
[1;37minternal                      :[0m i/o =  275/  169  lat = 1316  and =  12675  lev = 91
abc 11> ***EOF***
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:23)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,12364
1,12364
2,12364
3,12364
4,12364
5,12364
Best Flow(s) (#max=5):
strash;dc2;rewrite -z;dc2;refactor;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:23)
abc 01> read internal.aig; source ode.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  275/  169  lat = 1316  and =  12364  lev = 92
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: ode.ftune.aig[0m
********************************************************
```

### ode.t1.search.log
```
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:17)
abc 01> ftune -d internal.aig -r 1 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,90
1,90
2,90
3,90
4,89
5,89
Best Flow(s) (#max=5):
strash;read dontCare;rewrite;refactor -z;rewrite -z;resub -K 8;dc2;refactor;strash;
strash;read dontCare;refactor;refactor -z;resub -K 8;refactor;rewrite -z;dc2;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:17)
abc 01> read internal.aig; source ode.script;strash;write internal.aig
Generic file reader requires a known file extension to open "dontCare".
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  275/  169  lat = 1316  and =  12737  lev = 89
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: ode.ftune.aig[0m
********************************************************
```

### or1200.t0.search.log
```
[1;37minternal                      :[0m i/o =  588/  509  lat =  670  and =  10222  lev =132
abc 10> ***EOF***
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:25)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,10159
1,10159
2,10159
3,10159
4,10159
5,10159
Best Flow(s) (#max=5):
strash;resub -K 8;refactor -z;rewrite -z;resub -K 8;refactor;dc2;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:25)
abc 01> read internal.aig; source or1200.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  588/  509  lat =  670  and =  10159  lev =132
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: or1200.ftune.aig[0m
********************************************************
```

### or1200.t1.search.log
```
[1;37minternal                      :[0m i/o =  588/  509  lat =  670  and =  10257  lev =130
abc 10> ***EOF***
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:25)
abc 01> ftune -d internal.aig -r 1 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,130
1,130
2,130
3,130
4,130
5,130
Best Flow(s) (#max=5):
strash;rewrite -z;rewrite -z;resub -K 8;dc2;refactor -z;refactor;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:25)
abc 01> read internal.aig; source or1200.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  588/  509  lat =  670  and =  10198  lev =130
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: or1200.ftune.aig[0m
********************************************************
```

### syn2.t0.search.log
```
[1;37minternal                      :[0m i/o =  450/  321  lat = 1512  and =  23095  lev = 86
abc 11> ***EOF***
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:22)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,22534
1,22534
2,22534
3,22534
4,22534
5,22534
Best Flow(s) (#max=5):
strash;dc2;rewrite -z;dc2;refactor;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:22)
abc 01> read internal.aig; source syn2.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  450/  321  lat = 1512  and =  22534  lev = 85
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: syn2.ftune.aig[0m
********************************************************
```

### syn2.t1.search.log
```
*************  level[2] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:20)
abc 01> ftune -d internal.aig -r 1 -t 1 -p 1 -i 6 -s 5
Your current setups:
Design = internal.aig, target = 1, repeats = 1, prefix = 1, forget = 0, iteration = 6, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,80
1,80
2,80
3,80
4,80
5,80
Best Flow(s) (#max=5):
strash;refactor;refactor -z;dc2;rewrite -z;refactor;resub -K 8;strash;
strash;refactor;resub -K 8;dc2;refactor -z;refactor;rewrite -z;strash;
strash;read dontCare;resub -K 8;resub -K 8;dc2;refactor -z;refactor;rewrite -z;strash;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Oct 11 2026 09:50:20)
abc 01> read internal.aig; source syn2.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  450/  321  lat = 1512  and =  23085  lev = 80
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: syn2.ftune.aig[0m
********************************************************
```

