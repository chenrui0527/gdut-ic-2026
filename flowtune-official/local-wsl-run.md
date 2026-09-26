# 在本机运行作者代码的记录（WSL）

云端那次跑通之后，我又在自己电脑上装了一套 Linux 环境，把作者代码**在本机编译并运行**了一遍。

## 环境

| 项目 | 内容 |
|---|---|
| 系统 | Windows + WSL2，Ubuntu 26.04.1 LTS（内核 6.18.33.2-microsoft-standard-WSL2） |
| 编译器 | gcc / g++ 15.2.0 |
| 构建工具 | cmake 4.2.3、make（16 核并行） |
| 依赖 | build-essential、libreadline-dev、git |
| 代码来源 | <https://github.com/Yu-Maryland/FlowTune>（作者官方仓库） |

## 步骤（全部在本机执行）

1. 开启 Windows 自带的 WSL 组件（两条 `dism /online /enable-feature ...`），重启；
2. 安装 WSL 官方包 `wsl.2.7.14.0.x64.msi`，再安装 Ubuntu 26.04；
3. 在 Ubuntu 里装编译依赖：`apt-get install -y build-essential cmake libreadline-dev git`；
4. 编译作者代码：`cd src/build && cmake .. && make -j16`；
5. 跑官方示例：`./single_design.sh adder2 adder2.blif 1 5 0 5 1`。

## 结果

编译产物（本机编译，时间戳就是这次运行的时间）：

```
-rwxr-xr-x 1 root root 24842056 Sep 27 00:03 /root/FlowTune/src/build/abc
UC Berkeley, ABC 1.01 (compiled Sep 27 2026 00:02:49)
```

`ftune`（论文里的多臂老虎机）在本机运行，并打印出它选出的流程与臂统计：

```
Best Flow(s) (#max=5):
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;

******  ARM   --  ACTIONS --  WINRATE  *********
```

`adder2` 设计的结果（AIG 节点数 / 逻辑级数）：

```
ADD2 : i/o = 4/3  lat = 0  and = 10  lev = 4
```

完整日志：[local-wsl-ftune.log](local-wsl-ftune.log)

## 两点说明

1. `adder2` 这个示例本来就极简（10 个 AIG 节点），所以各流程结果都一样、臂胜率均等；要看"优化了多少"要看云端那次跑的 `bfly`（AIG 节点 23192 → 22270）。
2. 编译时踩的坑：`ftune` 内部会调用名叫 `abc` 的程序，必须把编译产物放进 `PATH`，否则日志会刷一屏 `sh: abc: not found`，内部评估全部失败。云端第一次运行就踩了这个坑。
