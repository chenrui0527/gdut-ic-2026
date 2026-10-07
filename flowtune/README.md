# FlowTune 论文复现：用多臂老虎机做逻辑综合流程搜索

这一部分是第五题（进阶挑战）。下面写的是我实际做过的事，包括跑失败、返工的过程，
以及最后在云端 Ubuntu 上把作者官方代码编译并跑通的结果。

这个子项目对应招新考核书第五部分"进阶挑战"里的第 2 类任务（读懂论文 + 跑通前端后端），
论文是 IEEE Xplore 上的 **FlowTune: End-to-End Automatic Logic Optimization Exploration via Domain-Specific Multiarmed Bandit**（IEEE TCAD，作者 Cunxi Yu）：
<https://ieeexplore.ieee.org/abstract/document/9916059>

## 一、论文讲了什么（三句话版）

1. 芯片设计流程是一串变换的组合（综合、布局、布线里的各种操作），组合空间极大，靠专家经验手工调，很难为每个设计都调到最好。
2. 已有的机器学习做法要么需要大量标注数据和长时间训练，要么计算开销大到没法真的接进 EDA 工具的流程里。
3. FlowTune 把"流程搜索"写成一个**多阶段的序列决策问题**，用**领域知识加持的多阶段多臂老虎机**逐步挑变换（配方）：不需要训练数据，边跑边学，可以直接嵌进工具。

## 二、前端 / 后端分别干了什么

在逻辑综合这个场景里：

- **前端 = 设计输入与功能验证**
  写 RTL 源码（`rtl/counter.v` 4 位计数器、`rtl/mult8.v` 8×8 乘法器），用 Yosys 读入并展开（`prep`），
  然后用**形式化等价性检查**证明"综合后的门级网表"和"原始 RTL"功能完全一致 —— 见 `verify_equivalence.ys`，
  跑完会输出 `Equivalence successfully proven!`。
  这台机器没有 iverilog / verilator 这类仿真器，所以这里用形式化证明代替跑波形，强度不低于仿真。
- **后端 = 逻辑综合与优化**
  把 RTL 综合成门级网表（`synth` → `techmap` → `simplemap`），统计**门数**（`stat`）和**关键路径深度**（`ltp`）。
  这一环正是论文要优化的对象。

## 三、多臂老虎机是怎么实现的

- 一条流程拆成 **3 个阶段**：粗粒度优化 → 映射前优化 → 映射后优化；中间的映射步骤对**所有组合都一样**，
  这样比较的才是"配方选择"，而不是"有没有做门级映射"。
- 每个阶段有若干"臂"（候选配方），组合空间 3 × 3 × 6 = **54 种**。
- 每一轮：用 **UCB1** 给每个阶段挑一个臂（没试过的先试；否则按 `平均奖励 + 1.2 × √(ln N / n)` 选），
  跑一次**真实综合**，把"相对默认流程省下的门数比例"作为奖励，回填给本轮被选中的三个臂。
- 跑 30 轮，把它找到的最好组合和**穷举 54 种**的结果对比。

## 四、实测结果

| 设计 | 默认流程 | 老虎机 30 轮找到的最好 | 穷举 54 种的最好 | 面积变化 |
|---|---|---|---|---|
| counter（4 位计数器） | 39 门 | **10 门**（第 2 轮就找到） | 10 门 | −74% |
| mult8（8×8 乘法器） | 769 门 | **367 门**（第 2 轮就找到） | 367 门 | −52% |

找到的最优组合（两个设计一致）：

```
阶段1: opt -full
阶段2: opt -full; opt_merge
映射:   techmap; simplemap
阶段3: opt -full; opt_merge; opt_clean
```

**结论**：多臂老虎机只用了 **2 次**综合评估，就找到了穷举要跑 **54 次**才能确认的最优配方。
这就是论文的核心价值：不依赖训练数据、不靠穷举，边跑边学。

每轮的完整记录在 `results/*_history.csv`，汇总在 `results/summary.json`。

## 五、跨设计迁移：把经验带到下一个设计（领域知识的代理实现）

论文标题里的 **domain-specific（领域特定）** 强调“用领域知识指导搜索”，其中最典型的一条就是**跨设计复用经验**：
一个设计上学到的“哪些配方好”，不应该让下一个设计再从零学一遍。

`flowtune_mab.py` 里实现了三种配置并做对比：

- **冷启动**：每个设计的臂统计都从零开始（不复用任何经验）；
- **弱迁移**：把前面设计的臂统计压成“每个臂一条虚拟观测”（n = 1）后作为先验，只轻推一把；
- **强迁移**：直接把累计的臂统计当先验（相当于很相信前面的经验）。

评价指标是**第一次找到穷举最优所需的评估次数**（越少越好），每个配置跑 **10 个随机种子**取中位数：

| 设计 | 默认门数 | 穷举最优 | 冷启动（中位数） | 弱迁移 | 强迁移 |
|---|---|---|---|---|---|
| counter | 39 | 10 | 2 | 2 | 2 |
| mult8 | 769 | 367 | 2 | **1** | 4 |
| adder8 | 97 | 52 | 2 | **1** | 1 |
| alu4 | 183 | 120 | 2 | **1** | 1 |
| adder16 | 198 | 113 | 2 | **1** | 1 |

（10 个种子下所有配置都在 30 轮预算内找到了最优，命中率 10/10。）

**结论（包括一个反例）**：

1. **弱迁移稳定有效**：5 个设计里有 4 个把“找到最优所需评估次数”从 2 次降到 1 次；
2. **强迁移会出现“负迁移”**：`mult8` 反而从 2 次变成 4 次——前一个设计的偏好太强，把新设计带偏了；
3. 这说明 domain-specific **不是“把经验直接搬过去”这么简单**：迁移多少、迁移给谁需要领域知识来决策。
   这正是我下一步要做的事——用设计特征/相似度决定迁移强度（也就是论文里 contextual bandit 那类做法）。

## 六、怎么运行

```powershell
cd flowtune
python run_synth.py        # 单条流程自检，打印门数/深度
python flowtune_mab.py     # 多臂老虎机实验 + 穷举对照（约 2 分钟）
```

前端验证（等价性检查）：

```powershell
yowasp-yosys -s verify_equivalence.ys
```

本机的 Yosys 是用 pip 安装的 WebAssembly 版（`yowasp-yosys`），不需要管理员权限。
换到装了原生 Yosys 的机器上，只要设置环境变量 `YOSYS` 指向 `yosys` 即可。

## 七、目录结构

```
flowtune/
├── rtl/counter.v            4 位计数器（时序逻辑）
├── rtl/mult8.v              8×8 乘法器（组合逻辑，规模最大）
├── rtl/adder8.v             8 位加法器
├── rtl/adder16.v            16 位加法器
├── rtl/alu4.v               4 位 ALU（多路选择结构）
├── rtl/lfsr8.v              8 位 LFSR（备用设计，无优化余量）
├── verify_equivalence.ys    前端：形式化等价性检查脚本
├── recipes.json             三个阶段各自的候选配方（老虎机的“臂”）
├── run_synth.py             后端接口：调 Yosys 跑一条流程，返回门数/深度
├── flowtune_mab.py          论文算法复现：多阶段 UCB1 + 跨设计迁移 + 穷举对照
└── results/                 实验输出（每种配置的 CSV + summary.json）
```

## 八、我自己实现的那套，还差什么

- 论文里说的"代码公开"是成立的：作者仓库是 <https://github.com/Yu-Maryland/FlowTune>，**我已经把它编译并跑通**（见第九节，在 GitHub Actions 的 Ubuntu 上完成）。
- 我自己实现的那套（第五～七节）跑在 Yosys（WebAssembly 版）上，它不带 iverilog/verilator，也没有 ABC 外部二进制，因此：
  - 技术映射用的是 Yosys 自带的 `techmap` + `simplemap`，不是论文里的 ABC 配方；
  - 前端用形式化等价性检查代替波形仿真。
- 我自己实现的奖励只用了"门数"（面积）这一个指标；论文还考虑延时，以及多个设计之间的泛化。
- 第五节的跨设计迁移是我对论文 "domain-specific" 思想的一个**可运行代理实现**（用已优化设计的臂统计做先验），
  并不是论文里完整的领域知识建模：论文还会结合设计特征做 context、并覆盖不同的电路表示与后端工具。

## 九、官方代码复现（跑通作者仓库，GitHub Actions 自动执行）

前面第五节到第七节是我自己实现的多阶段老虎机；这一节是**把作者的官方代码真正编译并运行起来**（代码级复现）。

- **官方仓库**：<https://github.com/Yu-Maryland/FlowTune>（FlowTune 的实现就是 ABC 的一个分支，编译出一个带 `ftune` 命令的 `abc`）
- **为什么在云端跑**：本机是 Windows，没有 Linux 编译器（也没装 WSL），而作者的 `install.sh` 要求 Ubuntu + g++ + cmake + readline。
  所以我写了工作流 [.github/workflows/flowtune-official.yml](../.github/workflows/flowtune-official.yml)，在 GitHub Actions 的 `ubuntu-latest` 上自动完成：装依赖 → `cmake && make` 编译 ABC → 运行作者的 `single_design.sh`。
- **完整日志**（自动提交回仓库）：[flowtune-official/official-run-report.md](../flowtune-official/official-run-report.md)

**跑出来的结果**（作者代码的真实输出）：

| 项目 | 结果 |
|---|---|
| 编译 | 成功，生成 `abc`（25.9 MB，`UC Berkeley, ABC 1.01`） |
| `ftune` 命令 | 正常运行，打印出多臂老虎机的探索过程与最终选择 |
| 臂统计（`ARM -- ACTIONS -- WINRATE`） | 例如 adder2：6 个臂 × 6 个动作，胜率均 1/6（因为该设计所有流程结果相同） |
| `adder2` 基准 | AIG 节点 10 → 10、级数 4 → 4（这个设计已经是极简，没有优化空间） |
| `bfly` 基准 | **原来写的 `23192 → 22270` 有误，已在下方的"修正说明"里改正** |
| 产物 | 生成 `adder2.ftune.aig`（FlowTune 优化后的 AIG） |

**FlowTune 在这两个基准上选出的最佳流程**（作者代码打印）：

```
strash;rewrite;dc2;resub -K 8;refactor;refactor -z;rewrite -z;strash;ifraig;dch -f;strash;print_stats;
```

**说明与边界**：

- 这是**跑通了作者代码**（代码级复现）；第六节那张"5 设计 × 10 种子"的表才是**方法级**实验（我自己实现的老虎机 + Yosys 环境）。
- 官方仓库的默认示例参数很小（`-i 5 -s 5`），我按它的用法原样跑，没有改参数，所以提升幅度有限；论文里报的大数字是在更大规模的基准和更多迭代下得到的。
- 编译过程中遇到的坑也记录在报告里：新版本 gcc 需要 `-fcommon -w` 兜住老代码的多重定义；`ftune` 内部会调用 `abc`，必须把编译产物加进 `PATH`，否则内部评估全部失败（第一次运行就是这个错，第二次修好后正常）。

### 修正说明（2026-10-07）

上面这张表里 `bfly` 那一行原来写的是"23192 → 22270（−4.0%）"。**这个说法是错的。**

去翻原始报告 [flowtune-official/official-run-report.md](../flowtune-official/official-run-report.md) 的第 388–405 行就能看到：23192 是 `ftune` 搜索过程中打印出来的评分，22270 是应用它选出的流程之后的结果。**两个数都是 ftune 的输出，根本不是"优化前 → 优化后"。** 拿 ftune 跟 ftune 比，等于基准用错了。

错在哪：我当时直接把日志里第一次出现的数字当成了原始值，没有单独去量"这个设计本来有多大"。

重新做的实验（第十节）里，我先单独量了原始设计，得到 **28910 个 AIG 节点、97 层**——与论文表 III 里 bfly 那一行（Nodes 28910、Level 97）完全一致。所以 **28910 才是正确的基准**。

---

## 十、按老师要求的复现：网表 + 逻辑门数量 + 网表深度

老师的批注要求是三条：**① 得到逻辑综合的网表；② 比较逻辑门的数量和网表的深度；③ 先不用跑布线。**

对应的实验在 `flowtune-reproduction/` 目录，由工作流 [.github/workflows/flowtune-reproduction.yml](../.github/workflows/flowtune-reproduction.yml) 在云端 Ubuntu 上完整跑出，**原始日志、网表文件、汇总表全部自动提交回仓库**，可以逐步复查。

**结果**（每个数字都取自 `flowtune-reproduction/raw/` 里的原始日志，来自 ABC 自己打印的 `print_stats`）：

| 做法 | 逻辑门数量 (and) | 网表深度 (lev) | 相对原始设计 |
|---|---|---|---|
| 原始设计（未做任何优化） | 28910 | 97 | — |
| 基线一：ABC 默认 `resyn` | 26177 | 68 | 门数 −9.5%，深度 −29.9% |
| 基线二：`resyn` 连续 25 次 | 24276 | 68 | 门数 −16.0%，深度 −29.9% |
| **FlowTune `t=0`（优化门数）** | **23192** | 87 | 门数 **−19.8%**，深度 −10.3% |
| **FlowTune `t=1`（优化深度）** | 23708 | 86 | 门数 −18.0%，深度 −11.3% |

**结论（好的和坏的都写）**

- **门数上 FlowTune 赢**：`t=0` 拿到 23192 个节点，比 `resyn×25` 的 24276 **再少 4.5%**，比原始设计少 19.8%，方向和论文一致。
- **深度上 FlowTune 输**：`resyn` 把深度从 97 降到 68，而 FlowTune 只降到 87 / 86。原因很具体——它两次选出的流程里**都没有 `balance` 这个命令**，而 `balance` 正是用来摊平电路、降低深度的；FlowTune 只能在它候选的命令集合里挑，候选里没有它。这不是它算错了，是命令集合决定的。
- **搜索配置偏小**：本次用 `-r 1 -i 5 -s 5`（共 25 次评估）。日志显示五轮迭代的评分始终是同一个数，说明第一轮就找到了最好值、后面四轮没有继续改进。论文用的是大得多的预算，所以提升幅度小于论文属于预期，不是复现失败。

**原始证据（老师问"你怎么知道数是对的"就打开这些）**

- 自检结论与汇总表：[flowtune-reproduction/SELFCHECK.md](../flowtune-reproduction/SELFCHECK.md)、[flowtune-reproduction/RESULTS.md](../flowtune-reproduction/RESULTS.md)
- 逐份原始日志：[flowtune-reproduction/raw/](../flowtune-reproduction/raw/)（`00_original` 原始设计、两组基线、两组 FlowTune 的搜索与应用日志）
- 综合出来的网表：[flowtune-reproduction/netlists/](../flowtune-reproduction/netlists/)（4 个 `.aig` 文件）

**踩坑记录（第二次，也是我自己犯的错）**：第一版工作流里我只把 `abc` 放进了当前目录、用 `./abc` 调用，但 `ftune` 内部是用 `system("abc ...")` 按 PATH 去找它的，结果每次评估都输出 `sh: 1: abc: not found`、评分全部变成哨兵值 `1e+09`，搜索等于没做。**我一开始没发现，是去翻原始日志才看到的。** 现在工作流里加了硬性自检：日志里只要出现 `abc: not found` 或 `1e+09` 就直接判定失败，并把结论写进 `SELFCHECK.md`——不允许把无效结果当成结果交出去。
