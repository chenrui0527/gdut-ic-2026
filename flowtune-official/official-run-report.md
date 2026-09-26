# FlowTune 官方代码运行记录（GitHub Actions）

- 运行时间（UTC）：2026-09-26 08:32:50
- 运行环境：ubuntu-latest（x86_64），gcc 13
- 官方仓库：https://github.com/Yu-Maryland/FlowTune

## 1. 编译日志（末尾 120 行）
```
[ 88%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddAddApply.c.o
[ 88%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddAddFind.c.o
[ 88%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddAddInv.c.o
[ 88%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddAddIte.c.o
[ 88%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddAddNeg.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddAddWalsh.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddAndAbs.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddAnneal.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddApa.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddApprox.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddBddAbs.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddBddCorr.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddBddIte.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddBridge.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddCache.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddCheck.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddClip.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddCof.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddCompose.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddDecomp.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddEssent.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddExact.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddExport.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddGenCof.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddGenetic.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddGroup.c.o
[ 90%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddHarwell.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddInit.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddInteract.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddLCache.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddLevelQ.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddLinear.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddLiteral.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddMatMult.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddPriority.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddRead.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddRef.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddReorder.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddSat.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddSign.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddSolve.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddSplit.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddSubsetHB.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddSubsetSP.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddSymmetry.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddTable.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddUtil.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddWindow.c.o
[ 92%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddCount.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddFuncs.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddGroup.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddIsop.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddLin.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddMisc.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddPort.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddReord.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddSetop.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddSymm.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/cudd/cuddZddUtil.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddAuto.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddCas.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddImage.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddKmap.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddMaxMin.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddMisc.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddSet.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddSymm.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddThresh.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddTime.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/extrab/extraBddUnate.c.o
[ 94%] Building C object CMakeFiles/libabc.dir/src/bdd/dsd/dsdApi.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/dsd/dsdCheck.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/dsd/dsdLocal.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/dsd/dsdMan.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/dsd/dsdProc.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/dsd/dsdTree.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/epd/epd.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/mtr/mtrBasic.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/mtr/mtrGroup.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/reo/reoApi.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/reo/reoCore.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/reo/reoProfile.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/reo/reoShuffle.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/reo/reoSift.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/reo/reoSwap.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/reo/reoTransfer.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/reo/reoUnits.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/cas/casCore.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/cas/casDec.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/bbr/bbrCex.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/bbr/bbrImage.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/bbr/bbrNtbdd.c.o
[ 96%] Building C object CMakeFiles/libabc.dir/src/bdd/bbr/bbrReach.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Cluster.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Constr.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Core.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Group.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Hint.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Man.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Matrix.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Pivot.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Reach.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb1Sched.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb2Bad.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb2Core.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb2Driver.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb2Dump.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb2Flow.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb2Image.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb3Image.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb3Nonlin.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb4Cex.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb4Image.c.o
[ 98%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb4Nonlin.c.o
[100%] Building C object CMakeFiles/libabc.dir/src/bdd/llb/llb4Sweep.c.o
[100%] Linking CXX static library libabc.a
[100%] Built target libabc
[100%] Building C object CMakeFiles/abc.dir/src/base/main/main.c.o
[100%] Linking CXX executable abc
[100%] Built target abc
```

## 2. 编译产物
```
-rwxr-xr-x 1 runner runner 25900400 Sep 26 08:25 official-flowtune/src/build/abc
```

## 3. 官方示例运行输出（single_design.sh adder2 adder2.blif 1 1 0 1 1）
```
*************  level-0 tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> ftune -d adder2.blif -r 1 -t 0 -p 1 -i 1 -s 1
rm: cannot remove '.temp.result.txt': No such file or directory
rm: cannot remove 'adder2.blif.log': No such file or directory
Your current setups:
Design = adder2.blif, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 1, nSample = 1, liberty = (null)
begin:abc -c "read adder2.blif;strash;
0,10
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> read adder2.blif; source adder2.script;strash;write internal.aig;ps
[1;37mADD2                          :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
[1;37mADD2                          :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
abc 10> ***EOF***
*************  level[1] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 1 -s 1
rm: cannot remove 'internal.aig.log': No such file or directory
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 1, nSample = 1, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,10
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> read internal.aig; source adder2.script;strash;write internal.aig
[1;37minternal                      :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: adder2.ftune.aig[0m
********************************************************
```

## 3b. 多轮采样运行（1 5 0 5 1，能看出老虎机的学习过程）
```
*************  level-0 tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> ftune -d adder2.blif -r 1 -t 0 -p 1 -i 5 -s 5
Your current setups:
Design = adder2.blif, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 5, nSample = 5, liberty = (null)
begin:abc -c "read adder2.blif;strash;
0,10
1,10
2,10
3,10
4,10
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> read adder2.blif; source adder2.script;strash;write internal.aig;ps
[1;37mADD2                          :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
[1;37mADD2                          :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
abc 10> ***EOF***
*************  level[1] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 5 -s 5
rm: cannot remove 'internal.aig.log': No such file or directory
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 5, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,10
1,10
2,10
3,10
4,10
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> read internal.aig; source adder2.script;strash;write internal.aig
[1;37minternal                      :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: adder2.ftune.aig[0m
********************************************************
```

## 3c. FlowTune 学到的臂统计（.temp.result.txt）
```
(Warning)Mean : 10; best : 10; size : 36stdev: 0
0: mean=10; stdev=0; current_epoch_win_rate : 0
1: mean=10; stdev=0; current_epoch_win_rate : 0
2: mean=10; stdev=0; current_epoch_win_rate : 0
3: mean=10; stdev=0; current_epoch_win_rate : 0
4: mean=10; stdev=0; current_epoch_win_rate : 0
5: mean=10; stdev=0; current_epoch_win_rate : 0

*********  Info  ************
******  ARM   --  ACTIONS --  WINRATE  *********
	 [0] -- [6] : [0.166667]
	 [1] -- [6] : [0.166667]
	 [2] -- [6] : [0.166667]
	 [3] -- [6] : [0.166667]
	 [4] -- [6] : [0.166667]
	 [5] -- [6] : [0.166667]
Mean : 10; best : 10; size : 42stdev: 0
0: mean=10; stdev=0; current_epoch_win_rate : 0
1: mean=10; stdev=0; current_epoch_win_rate : 0
2: mean=10; stdev=0; current_epoch_win_rate : 0
3: mean=10; stdev=0; current_epoch_win_rate : 0
4: mean=10; stdev=0; current_epoch_win_rate : 0
5: mean=10; stdev=0; current_epoch_win_rate : 0

*********  Info  ************
******  ARM   --  ACTIONS --  WINRATE  *********
	 [0] -- [7] : [0.166667]
	 [1] -- [7] : [0.166667]
	 [2] -- [7] : [0.166667]
	 [3] -- [7] : [0.166667]
	 [4] -- [7] : [0.166667]
	 [5] -- [7] : [0.166667]
Mean : 10; best : 10; size : 48stdev: 0
0: mean=10; stdev=0; current_epoch_win_rate : 0
1: mean=10; stdev=0; current_epoch_win_rate : 0
2: mean=10; stdev=0; current_epoch_win_rate : 0
3: mean=10; stdev=0; current_epoch_win_rate : 0
4: mean=10; stdev=0; current_epoch_win_rate : 0
5: mean=10; stdev=0; current_epoch_win_rate : 0

*********  Info  ************
******  ARM   --  ACTIONS --  WINRATE  *********
	 [0] -- [8] : [0.166667]
	 [1] -- [8] : [0.166667]
	 [2] -- [8] : [0.166667]
	 [3] -- [8] : [0.166667]
	 [4] -- [8] : [0.166667]
	 [5] -- [8] : [0.166667]
Mean : 10; best : 10; size : 54stdev: 0
0: mean=10; stdev=0; current_epoch_win_rate : 0
1: mean=10; stdev=0; current_epoch_win_rate : 0
2: mean=10; stdev=0; current_epoch_win_rate : 0
3: mean=10; stdev=0; current_epoch_win_rate : 0
4: mean=10; stdev=0; current_epoch_win_rate : 0
5: mean=10; stdev=0; current_epoch_win_rate : 0

*********  Info  ************
******  ARM   --  ACTIONS --  WINRATE  *********
	 [0] -- [9] : [0.166667]
	 [1] -- [9] : [0.166667]
	 [2] -- [9] : [0.166667]
	 [3] -- [9] : [0.166667]
	 [4] -- [9] : [0.166667]
	 [5] -- [9] : [0.166667]
Mean : 10; best : 10; size : 60stdev: 0
0: mean=10; stdev=0; current_epoch_win_rate : 0
1: mean=10; stdev=0; current_epoch_win_rate : 0
2: mean=10; stdev=0; current_epoch_win_rate : 0
3: mean=10; stdev=0; current_epoch_win_rate : 0
4: mean=10; stdev=0; current_epoch_win_rate : 0
5: mean=10; stdev=0; current_epoch_win_rate : 0

```

## 3d. FlowTune 最终选出的流程（adder2.script）
```
read internal.aig;strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
```

## 4. 第二个基准的运行输出
### ftune_adder2_long.log
```
*************  level-0 tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> ftune -d adder2.blif -r 1 -t 0 -p 1 -i 5 -s 5
Your current setups:
Design = adder2.blif, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 5, nSample = 5, liberty = (null)
begin:abc -c "read adder2.blif;strash;
0,10
1,10
2,10
3,10
4,10
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> read adder2.blif; source adder2.script;strash;write internal.aig;ps
[1;37mADD2                          :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
[1;37mADD2                          :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
abc 10> ***EOF***
*************  level[1] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 5 -s 5
rm: cannot remove 'internal.aig.log': No such file or directory
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 5, nSample = 5, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,10
1,10
2,10
3,10
4,10
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;rewrite -z;refactor -z;dc2;refactor;resub -K 8;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;refactor;dc2;rewrite -z;resub -K 8;refactor -z;strash;ifraig;dch -f;strash;print_stats;
strash;rewrite;resub -K 8;dc2;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> read internal.aig; source adder2.script;strash;write internal.aig
[1;37minternal                      :[0m i/o =    4/    3  lat =    0  and =     10  lev =  4
abc 10> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: adder2.ftune.aig[0m
********************************************************
```
### ftune_bfly.abc.log
```
*************  level-0 tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> ftune -d bfly.abc.blif -r 1 -t 0 -p 1 -i 1 -s 1
rm: cannot remove 'bfly.abc.blif.log': No such file or directory
Your current setups:
Design = bfly.abc.blif, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 1, nSample = 1, liberty = (null)
begin:abc -c "read bfly.abc.blif;strash;
0,23192
Best Flow(s) (#max=5):
strash;dc2;dc2;refactor;resub -K 8;rewrite -z;refactor -z;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> <source bfly.abc.script;strash;write internal.aig;ps
Hierarchy reader converted 4 instances of blackboxes.
Hierarchy reader converted 4 instances of blackboxes.
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  23192  lev = 87
[1;37mbfly                          :[0m i/o =  482/  257  lat = 1748  and =  23192  lev = 87
abc 11> ***EOF***
*************  level[1] tuning starts *********** 
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> ftune -d internal.aig -r 1 -t 0 -p 1 -i 1 -s 1
rm: cannot remove 'internal.aig.log': No such file or directory
Your current setups:
Design = internal.aig, target = 0, repeats = 1, prefix = 1, forget = 0, iteration = 1, nSample = 1, liberty = (null)
begin:abc -c "read internal.aig;strash;
0,22270
Best Flow(s) (#max=5):
strash;dc2;refactor -z;rewrite -z;dc2;resub -K 8;refactor;strash;ifraig;dch -f;strash;print_stats;
abc 01> ***EOF***
UC Berkeley, ABC 1.01 (compiled Sep 26 2026 08:24:44)
abc 01> read internal.aig; source bfly.abc.script;strash;write internal.aig
Warning: The choice nodes in the original AIG are removed by strashing.
[1;37minternal                      :[0m i/o =  482/  257  lat = 1748  and =  22270  lev = 87
abc 11> ***EOF***
********************************************************
[0;31m Final design produced by FlowTune: bfly.abc.ftune.aig[0m
********************************************************
```

## 5. FlowTune 产物文件
```
-rw-r--r-- 1 runner runner    225 Sep 26 08:25 official-flowtune/FlowTune-AIG-Optimization/adder2.ftune.aig
-rw-r--r-- 1 runner runner 176481 Sep 26 08:32 official-flowtune/FlowTune-AIG-Optimization/bfly.abc.ftune.aig
-rw-r--r-- 1 runner runner 167139 Sep 26 08:24 official-flowtune/FlowTune-AIG-Optimization/bfly.ftune.aig
```
