# FlowTune 论文复现：用多臂老虎机做逻辑综合流程搜索

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

## 五、怎么运行

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

## 六、目录结构

```
flowtune/
├── rtl/counter.v            4 位计数器（前端示例设计）
├── rtl/mult8.v              8×8 乘法器
├── verify_equivalence.ys    前端：形式化等价性检查脚本
├── recipes.json             三个阶段各自的候选配方（老虎机的"臂"）
├── run_synth.py             后端接口：调 Yosys 跑一条流程，返回门数/深度
├── flowtune_mab.py          论文算法复现：多阶段 UCB1 老虎机 + 穷举对照
└── results/                 实验输出（CSV + summary.json）
```

## 七、诚实说明

- 论文原文没有公开可用的代码（我在 GitHub 上没有找到作者发布的 FlowTune 实现），本机也没有 C++ 编译环境，
  所以**这个项目复现的是论文的算法框架（多阶段多臂老虎机选配方 + 真实综合反馈），不是原作者的代码**。
- 本机 Yosys 是 WebAssembly 版，不带 iverilog/verilator，也没有 ABC 外部二进制，因此：
  - 技术映射用的是 Yosys 自带的 `techmap` + `simplemap`，不是论文里的 ABC 配方；
  - 前端用形式化等价性检查代替波形仿真。
- 奖励只用了"门数"（面积）这一个指标；论文还考虑了延时，以及多个设计之间的泛化。
