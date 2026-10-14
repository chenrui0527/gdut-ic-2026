# 网表一致性检测（ABC 等价性检查）

- 运行时间（UTC）：2026-10-14 09:49:38
- 工具：作者仓库编译出来的 FlowTune 版 ABC（`ABC command line: "version".`）
- **检测的是什么**：① 输入网表（原始设计 `xxx.abc.blif` 经 `read + strash` 得到的网表）与 ② 优化后的网表，之间的功能一致性
- **怎么检测的**：`cec`（组合等价性检查）+ `dsec`（归纳式时序等价性检查，因为这几个设计都带触发器，所以时序这条才是决定性的）
- `-n` 表示输入/输出按**顺序**对应（AIG 网表文件里不带名字）

| 设计 | 优化后的网表 | cec（组合） | dsec（时序） |
|---|---|---|---|
| bfly | resyn | ✅ 等价 | ✅ 等价 |
| bfly | resyn25 | ✅ 等价 | ✅ 等价 |
| bfly | t0 | ✅ 等价 | ✅ 等价 |
| bfly | t1 | ✅ 等价 | ✅ 等价 |
| dscg | resyn | ✅ 等价 | ✅ 等价 |
| dscg | resyn25 | ✅ 等价 | ✅ 等价 |
| dscg | t0 | ✅ 等价 | ✅ 等价 |
| dscg | t1 | ✅ 等价 | ✅ 等价 |
| fir | resyn | ✅ 等价 | ✅ 等价 |
| fir | resyn25 | ✅ 等价 | ✅ 等价 |
| fir | t0 | ✅ 等价 | ⚠️ 见日志 |
| fir | t1 | ✅ 等价 | ⚠️ 见日志 |
| ode | resyn | ✅ 等价 | ✅ 等价 |
| ode | resyn25 | ✅ 等价 | ✅ 等价 |
| ode | t0 | ✅ 等价 | ✅ 等价 |
| ode | t1 | ✅ 等价 | ✅ 等价 |
| or1200 | resyn | ✅ 等价 | ✅ 等价 |
| or1200 | resyn25 | ✅ 等价 | ✅ 等价 |
| or1200 | t0 | ✅ 等价 | ✅ 等价 |
| or1200 | t1 | ✅ 等价 | ✅ 等价 |
| syn2 | resyn | ✅ 等价 | ✅ 等价 |
| syn2 | resyn25 | ✅ 等价 | ✅ 等价 |
| syn2 | t0 | ✅ 等价 | ✅ 等价 |
| syn2 | t1 | ✅ 等价 | ✅ 等价 |

## 每个设计输入网表的规模（与 RESULTS.md 里的「原始设计」一致）

```
bfly     [1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  28910  lev = 97
dscg     [1;37mdscg                          :[0m i/o =  418/  257  lat = 1618  and =  28252  lev = 92
fir      [1;37mfir                           :[0m i/o =  450/  225  lat = 1882  and =  27704  lev = 94
ode      [1;37mode                           :[0m i/o =  275/  169  lat = 1316  and =  16069  lev = 98
or1200   [1;37mor1200_flat                   :[0m i/o =  588/  509  lat =  670  and =  12833  lev =148
syn2     [1;37msyn2                          :[0m i/o =  450/  321  lat = 1512  and =  30003  lev = 93
```

## 原始输出（每个设计的输入网表统计）
### bfly.orig.log
```
ABC command line: "read bfly.abc.blif; strash; print_stats; write bfly.orig.aig".

Hierarchy reader converted 4 instances of blackboxes.
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  28910  lev = 97
```

### dscg.orig.log
```
ABC command line: "read dscg.abc.blif; strash; print_stats; write dscg.orig.aig".

Hierarchy reader converted 4 instances of blackboxes.
[1;37mdscg                          :[0m i/o =  418/  257  lat = 1618  and =  28252  lev = 92
```

### fir.orig.log
```
ABC command line: "read fir.abc.blif; strash; print_stats; write fir.orig.aig".

Hierarchy reader converted 4 instances of blackboxes.
[1;37mfir                           :[0m i/o =  450/  225  lat = 1882  and =  27704  lev = 94
```

### ode.orig.log
```
ABC command line: "read ode.abc.blif; strash; print_stats; write ode.orig.aig".

Hierarchy reader converted 2 instances of blackboxes.
[1;37mode                           :[0m i/o =  275/  169  lat = 1316  and =  16069  lev = 98
```

### or1200.orig.log
```
ABC command line: "read or1200.abc.blif; strash; print_stats; write or1200.orig.aig".

Hierarchy reader converted 65 instances of blackboxes.
[1;37mor1200_flat                   :[0m i/o =  588/  509  lat =  670  and =  12833  lev =148
```

### syn2.orig.log
```
ABC command line: "read syn2.abc.blif; strash; print_stats; write syn2.orig.aig".

Hierarchy reader converted 4 instances of blackboxes.
[1;37msyn2                          :[0m i/o =  450/  321  lat = 1512  and =  30003  lev = 93
```

## 原始输出（每个网表的 cec 结论）
### bfly.resyn.cec.log
```
ABC command line: "cec -n bfly.orig.aig bfly.resyn.aig".

Networks are equivalent.  Time =     8.98 sec
```

### bfly.resyn25.cec.log
```
ABC command line: "cec -n bfly.orig.aig bfly.resyn25.aig".

Networks are equivalent.  Time =    10.24 sec
```

### bfly.t0.cec.log
```
ABC command line: "cec -n bfly.orig.aig bfly.t0.aig".

Networks are equivalent.  Time =    19.54 sec
```

### bfly.t1.cec.log
```
ABC command line: "cec -n bfly.orig.aig bfly.t1.aig".

Networks are equivalent.  Time =    19.03 sec
```

### dscg.resyn.cec.log
```
ABC command line: "cec -n dscg.orig.aig dscg.resyn.aig".

Networks are equivalent.  Time =     8.12 sec
```

### dscg.resyn25.cec.log
```
ABC command line: "cec -n dscg.orig.aig dscg.resyn25.aig".

Networks are equivalent.  Time =     8.72 sec
```

### dscg.t0.cec.log
```
ABC command line: "cec -n dscg.orig.aig dscg.t0.aig".

Networks are equivalent.  Time =    11.66 sec
```

### dscg.t1.cec.log
```
ABC command line: "cec -n dscg.orig.aig dscg.t1.aig".

Networks are equivalent.  Time =    17.91 sec
```

### fir.resyn.cec.log
```
ABC command line: "cec -n fir.orig.aig fir.resyn.aig".

Networks are equivalent.  Time =     8.23 sec
```

### fir.resyn25.cec.log
```
ABC command line: "cec -n fir.orig.aig fir.resyn25.aig".

Networks are equivalent.  Time =     8.91 sec
```

### fir.t0.cec.log
```
ABC command line: "cec -n fir.orig.aig fir.t0.aig".

Networks are equivalent.  Time =    18.61 sec
```

### fir.t1.cec.log
```
ABC command line: "cec -n fir.orig.aig fir.t1.aig".

Networks are equivalent.  Time =    17.37 sec
```

### ode.resyn.cec.log
```
ABC command line: "cec -n ode.orig.aig ode.resyn.aig".

Networks are equivalent.  Time =     3.40 sec
```

### ode.resyn25.cec.log
```
ABC command line: "cec -n ode.orig.aig ode.resyn25.aig".

Networks are equivalent.  Time =     3.97 sec
```

### ode.t0.cec.log
```
ABC command line: "cec -n ode.orig.aig ode.t0.aig".

Networks are equivalent.  Time =     5.24 sec
```

### ode.t1.cec.log
```
ABC command line: "cec -n ode.orig.aig ode.t1.aig".

Networks are equivalent.  Time =     7.99 sec
```

### or1200.resyn.cec.log
```
ABC command line: "cec -n or1200.orig.aig or1200.resyn.aig".

Networks are equivalent.  Time =     1.78 sec
```

### or1200.resyn25.cec.log
```
ABC command line: "cec -n or1200.orig.aig or1200.resyn25.aig".

Networks are equivalent.  Time =     2.12 sec
```

### or1200.t0.cec.log
```
ABC command line: "cec -n or1200.orig.aig or1200.t0.aig".

Networks are equivalent.  Time =     3.96 sec
```

### or1200.t1.cec.log
```
ABC command line: "cec -n or1200.orig.aig or1200.t1.aig".

Networks are equivalent.  Time =     4.37 sec
```

### syn2.resyn.cec.log
```
ABC command line: "cec -n syn2.orig.aig syn2.resyn.aig".

Networks are equivalent.  Time =     7.91 sec
```

### syn2.resyn25.cec.log
```
ABC command line: "cec -n syn2.orig.aig syn2.resyn25.aig".

Networks are equivalent.  Time =     8.84 sec
```

### syn2.t0.cec.log
```
ABC command line: "cec -n syn2.orig.aig syn2.t0.aig".

Networks are equivalent.  Time =    14.13 sec
```

### syn2.t1.cec.log
```
ABC command line: "cec -n syn2.orig.aig syn2.t1.aig".

Networks are equivalent.  Time =    16.65 sec
```

## 原始输出（每个网表的 dsec 结论）
### bfly.resyn.dsec.log
```
ABC command line: "dsec -n bfly.orig.aig bfly.resyn.aig".

Networks are equivalent.  Time =    22.39 sec
```

### bfly.resyn25.dsec.log
```
ABC command line: "dsec -n bfly.orig.aig bfly.resyn25.aig".

Networks are equivalent.  Time =    23.77 sec
```

### bfly.t0.dsec.log
```
ABC command line: "dsec -n bfly.orig.aig bfly.t0.aig".

Networks are equivalent.  Time =    31.69 sec
```

### bfly.t1.dsec.log
```
ABC command line: "dsec -n bfly.orig.aig bfly.t1.aig".

Networks are equivalent.  Time =    43.80 sec
```

### dscg.resyn.dsec.log
```
ABC command line: "dsec -n dscg.orig.aig dscg.resyn.aig".

Networks are equivalent.  Time =    21.65 sec
```

### dscg.resyn25.dsec.log
```
ABC command line: "dsec -n dscg.orig.aig dscg.resyn25.aig".

Networks are equivalent.  Time =    22.43 sec
```

### dscg.t0.dsec.log
```
ABC command line: "dsec -n dscg.orig.aig dscg.t0.aig".

Networks are equivalent.  Time =    65.32 sec
```

### dscg.t1.dsec.log
```
ABC command line: "dsec -n dscg.orig.aig dscg.t1.aig".

Networks are equivalent.  Time =    64.65 sec
```

### fir.resyn.dsec.log
```
ABC command line: "dsec -n fir.orig.aig fir.resyn.aig".

Networks are equivalent.  Time =    56.23 sec
```

### fir.resyn25.dsec.log
```
ABC command line: "dsec -n fir.orig.aig fir.resyn25.aig".

Networks are equivalent.  Time =    58.51 sec
```

### fir.t0.dsec.log
```
ABC command line: "dsec -n fir.orig.aig fir.t0.aig".

Reached timeout (60 seconds) in frame 12.
Networks are UNDECIDED.   Time =   191.06 sec
The unsolved reduced miter is written into file "sm01.aig".
```

### fir.t1.dsec.log
```
ABC command line: "dsec -n fir.orig.aig fir.t1.aig".

Reached timeout (60 seconds) in frame 12.
Networks are UNDECIDED.   Time =   178.95 sec
The unsolved reduced miter is written into file "sm01.aig".
```

### ode.resyn.dsec.log
```
ABC command line: "dsec -n ode.orig.aig ode.resyn.aig".

Networks are equivalent.  Time =    27.03 sec
```

### ode.resyn25.dsec.log
```
ABC command line: "dsec -n ode.orig.aig ode.resyn25.aig".

Networks are equivalent.  Time =    27.62 sec
```

### ode.t0.dsec.log
```
ABC command line: "dsec -n ode.orig.aig ode.t0.aig".

Networks are equivalent.  Time =    28.53 sec
```

### ode.t1.dsec.log
```
ABC command line: "dsec -n ode.orig.aig ode.t1.aig".

Networks are equivalent.  Time =    27.64 sec
```

### or1200.resyn.dsec.log
```
ABC command line: "dsec -n or1200.orig.aig or1200.resyn.aig".

Networks are equivalent.  Time =    15.37 sec
```

### or1200.resyn25.dsec.log
```
ABC command line: "dsec -n or1200.orig.aig or1200.resyn25.aig".

Networks are equivalent.  Time =    15.33 sec
```

### or1200.t0.dsec.log
```
ABC command line: "dsec -n or1200.orig.aig or1200.t0.aig".

Networks are equivalent.  Time =    17.21 sec
```

### or1200.t1.dsec.log
```
ABC command line: "dsec -n or1200.orig.aig or1200.t1.aig".

Networks are equivalent.  Time =    16.64 sec
```

### syn2.resyn.dsec.log
```
ABC command line: "dsec -n syn2.orig.aig syn2.resyn.aig".

Networks are equivalent.  Time =    33.02 sec
```

### syn2.resyn25.dsec.log
```
ABC command line: "dsec -n syn2.orig.aig syn2.resyn25.aig".

Networks are equivalent.  Time =    35.12 sec
```

### syn2.t0.dsec.log
```
ABC command line: "dsec -n syn2.orig.aig syn2.t0.aig".

Networks are equivalent.  Time =    33.21 sec
```

### syn2.t1.dsec.log
```
ABC command line: "dsec -n syn2.orig.aig syn2.t1.aig".

Networks are equivalent.  Time =    34.02 sec
```

