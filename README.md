# 模拟电路：从读懂到设计

> 一本写给计算机专业学生的本科模拟电路教材。正文、公式、内联 SVG 电路图与 **34 个可直接运行的 LTspice 网表**放在同一个 HTML 页面里，浏览器打开即可读，复制代码即可仿真。

[![Static HTML](https://img.shields.io/badge/format-static%20HTML-orange)](./index.html)
[![Chapters](https://img.shields.io/badge/chapters-25%20%2B%20appendix-blue)](#内容结构)
[![LTspice](https://img.shields.io/badge/LTspice-34%20netlists-2ea44f)](#快速开始)
[![Python 3](https://img.shields.io/badge/toolchain-Python%203-3776AB)](#工具链与维护)
[![License](https://img.shields.io/badge/license-not%20specified-lightgrey)](#许可证)

**仓库**：[github.com/bertowang/analogCircuits](https://github.com/bertowang/analogCircuits) · **阅读入口**：[index.html](./index.html) · **版本**：v0.2 · 2026-11

---

## 目录

- [一眼看懂](#一眼看懂)
- [这本书解决什么问题](#这本书解决什么问题)
- [快速开始](#快速开始)
- [内容结构](#内容结构)
- [仓库结构](#仓库结构)
- [每章包含什么](#每章包含什么)
- [工具链与维护](#工具链与维护)
- [质量保障](#质量保障)
- [约定与边界](#约定与边界)
- [同系列教材](#同系列教材)
- [作者与 AI 使用说明](#作者与-ai-使用说明)
- [许可证](#许可证)

## 一眼看懂

| 项目 | 内容 |
| --- | --- |
| 读者定位 | 本科，尤其面向计算机专业学生；先修只需线性方程组、复数相量、一阶常微分方程、拉普拉斯结论 |
| 规模 | 25 章（00–24）+ 附录 A · 4 篇 · 27 个 HTML 页面 · 34 个 `.cir` 网表（含附录模板） |
| 内容形态 | 纯静态 HTML5 + CSS + 原生 JS + 内联 SVG；无外部依赖，离线 / `file://` 可读 |
| 仿真实验 | [ADI LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html)（免费，Windows / macOS）；网表注释统一 ASCII 英文 |
| 维护工具 | Python 3 标准库，5 个脚本；无需安装任何 Python 第三方包 |
| 学习闭环 | **手算 → 仿真 → 改参数看趋势 → 写结论** |
| 状态 | 25 章全部完稿；静态自检 0 错误 0 提示 |

## 这本书解决什么问题

**「读懂电路」和「设计电路」是两种可以训练的能力**，而不是「看多了自然会」。本书把这两件事拆成明确步骤（第 19、20 章），再用可运行的仿真把每一步的结论验证一遍：

- 公式与电路图同页：解释写在正文，示意图用内联 SVG，没有图片素材依赖。
- 每章至少一个完整 LTspice 网表：给出预期波形、该验证哪条公式、改哪个参数看什么趋势。
- 逐条知识点挂扩展学习链接：教材、课程、器件手册与开源例程入口集中在知识点地图与「扩展学习」。
- 方法论篇补齐工程侧：仿真方法论、PVT / 蒙特卡洛 / 最坏情况、PCB 与仪器调试。

**不适合**：需要版图设计、射频或工艺级器件物理的读者；本书止于板级模拟电路与仿真验证。

## 快速开始

### 1. 阅读（无需构建、无需服务器）

```bash
git clone git@github.com:bertowang/analogCircuits.git
cd analogCircuits
open index.html          # macOS；Linux 用 xdg-open，Windows 双击即可
```

也可以直接在本仓库点开 [index.html](./index.html) 查看源码，或启用 GitHub Pages 后以 `index.html` 为入口发布成站点。页面带侧栏目录、面包屑与上下章导航，共用 [assets/toc.js](./assets/toc.js) 这一份数据。

### 2. 跑一个 LTspice 实验（约 30 秒）

1. 安装 [ADI LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html)（免费）。
2. 直接使用仓库里的网表，例如 [part1/06-mosfet/sim/06-common-source.cir](./part1/06-mosfet/sim/06-common-source.cir)；或从任意章节的「仿真实验」点代码块右上角「复制」另存为 `.cir`。
3. LTspice 菜单 `File → Open` 选中该文件，点工具栏 `Run`。
4. 波形窗口 `Plot Settings → Add Trace` 选 `V(out)` 等节点；`.op` 的结果在 `View → SPICE Error Log`，不弹波形窗。
5. 同一网表可能同时写了 `.op` / `.tran` / `.ac`：只想看一类波形时，把其余分析行行首加 `*` 注释掉再 Run。

> 仓库里的 `.cir` 由 `tools/extract_netlists.py` 从 HTML 的 `<pre class="spice" data-file="sim/xxx.cir">` 自动抽出，页面与网表永远一致。

### 3. 运行静态自检

```bash
python3 tools/check_book.py
# 自检：27 个 HTML 页面，26 个章节，34 个网表，0 条错误，0 条提示
```

## 内容结构

| 分部 | 章节 | 主要内容 |
| --- | --- | --- |
| 卷首 · 工具与约定 | 00–02 | 绪论与阅读方法、LTspice 快速上手、SPICE 网表语法与仿真指令 |
| 第一篇 · 电路基础与器件 | 03–08 | 电路定律与读图、无源元件/暂态/频域、二极管整流限幅、MOSFET 两级模型、BJT 三种组态、理想运放与负反馈入门 |
| 第二篇 · 核心模拟电路模块 | 09–18 | 单级放大、电流源/电流镜/基准、差分放大、频响与极点、反馈与稳定性、运放设计、有源滤波、比较器/振荡器、电源与功率、噪声失真与误差预算 |
| 第三篇 · 方法论：从读懂到设计 | 19–23 | 读懂陌生电路、从规格设计电路、仿真方法论、PVT/蒙特卡洛鲁棒性、PCB/仪器/调试 |
| 第四篇 · 综合课程设计 | 24 | 综合实验与课程设计课题 |
| 附录 | A | 公式、SPICE 指令、中英术语速查，附网表模板 `sim/A-template.cir` |

建议两个学期、四阶段推进：工具与器件基础 → 核心模块 → 方法论 → 综合课题。完整目录与各章知识点见 [index.html](./index.html)。

## 仓库结构

```text
analogCircuits/
├── index.html                     # 总目录：学习路线、使用说明、全书目录、参考资源
├── appendix/                      # 附录 A：速查与资源总表
│   ├── index.html
│   └── sim/A-template.cir
├── part0/ … part4/                # 每章一个文件夹
│   └── NN-slug/
│       ├── index.html             # 正文：学习目标、§x.y、仿真实验、误区、习题、扩展学习
│       └── sim/*.cir              # 1–2 个 LTspice 网表
├── assets/
│   ├── style.css                  # 统一排版（含深色主题、打印样式）
│   ├── app.js                     # 侧栏、复制代码块、导航填充
│   └── toc.js                     # 目录唯一数据源：BOOK_TOC / BOOK_FLAT
├── tools/
│   ├── build_book.py              # 生成章节页（含结构化章节数据）
│   ├── book_expansion.py          # 章节正文补写数据 EXTRA_SECTIONS
│   ├── book_resources.py          # 扩展学习链接唯一数据源
│   ├── extract_netlists.py        # 从 HTML 代码块同步 sim/*.cir
│   └── check_book.py              # 全书静态自检
└── .gitignore                     # 忽略缓存与 LTspice 运行产物（.raw/.log/.op/...）
```

## 每章包含什么

| 栏目 | 作用 |
| --- | --- |
| 学习目标 | 学完应能做什么，用可检验的动词描述 |
| 正文小节 §x.y | 概念、直觉、公式推导、内联 SVG 电路图 |
| 仿真实验 | 完整 LTspice 网表 + 预期波形 + 该验证哪条公式 |
| 常见误区 / 习题 | 「仿真看着对其实错」的典型问题；先手算再用仿真核对 |
| 知识点地图 | 逐条列出知识点，每条挂 1–2 个扩展学习链接 |
| 扩展学习 / 延伸阅读 | 精读资料、检索入口与全书内链 |
| 状态徽章 | `已完稿` / `框架待补` / `待建`，当前 25 章均为已完稿 |

## 工具链与维护

**单一数据源**：正文与网表写在 `tools/` 的结构化 Python 数据里，HTML 由生成器产出。**不要直接编辑章节 HTML**，否则下次重建会被覆盖。

| 想改什么 | 编辑哪里 |
| --- | --- |
| 章节正文、SVG、仿真实验 | `tools/build_book.py` 中的章节数据 / `tools/book_expansion.py` |
| 扩展学习链接 | `tools/book_resources.py` 的 `R`、`TOPIC_RULES`、`CHAPTER_RESOURCES` |
| 页面结构、总目录 | `tools/build_book.py` 的 `render()` / `render_index()` |
| 样式与交互 | `assets/style.css`、`assets/app.js` |
| 新增章节 | `tools/build_book.py` 的 `CHAPTERS` 与 `assets/toc.js` 对应数据 |

| 命令 | 作用 |
| --- | --- |
| `python3 tools/build_book.py` | 只生成缺失的章节页（不覆盖已有文件） |
| `python3 tools/build_book.py --force` | 全量重建（会丢失对章节页的手工修改） |
| `python3 tools/build_book.py --list` | 列出章节 id / 路径 / 状态 |
| `python3 tools/extract_netlists.py` | 从 HTML 代码块同步写出 `sim/*.cir` |
| `python3 tools/extract_netlists.py --check` | 只检查页面与网表是否一致 |
| `python3 tools/extract_netlists.py --clean` | 同步并删除无对应代码块的旧 `.cir` |
| `python3 tools/check_book.py` | 全文自检，退出码非 0 时逐条报错 |

推荐改动顺序：

```bash
python3 tools/build_book.py --force      # 1. 重建页面
python3 tools/extract_netlists.py        # 2. 同步网表
python3 tools/check_book.py              # 3. 自检
```

## 质量保障

`tools/check_book.py` 覆盖：目录与 `toc.js` 一致性、内部链接、HTML 标签配对、页面代码块与 `.cir` 同步、SPICE 点指令与元件行基本语法、网表非 ASCII 字符检查。

当前本地运行结果：**27 个 HTML 页面 / 26 个章节 / 34 个网表，0 条错误，0 条提示**。

> 说明：以上是静态自检，不替代真机仿真。波形与数值结论请以本机 LTspice 实跑及权威教材、器件手册为准。

## 约定与边界

- `sim/*.cir` 是源网表，纳入版本控制；LTspice 生成的 `.raw` / `.log` / `.net` / `.op` / `.plt` 等运行产物由 `.gitignore` 排除。
- 网表内注释一律 ASCII 英文，中文解释全部放在 HTML 正文，避免 LTspice 中文编码兼容问题。
- **ngspice** 只作为通用 SPICE 语法对照资源，**PyLTSpice** 是可选的批量仿真推荐，二者都不是本仓库的运行依赖；仓库不提供 `.asc` 原理图。
- LTspice 为 Analog Devices 的免费工具，本书与之无从属关系；书中外部链接的版权归各自维护者所有。

## 同系列教材

三本教材共用同一套静态站点骨架与「单一数据源 + 自检」维护方式：

| 仓库 | 主题 | 示例形态 |
| --- | --- | --- |
| **analogCircuits**（本仓库） | 模拟电路（本科） | LTspice `.cir` 网表 |
| [imageProcessing](https://github.com/bertowang/imageProcessing) | 数字图像处理（本科到研究生） | GNU Octave `.m` + 开源工程链接 |
| [studyingEconomics](https://github.com/bertowang/studyingEconomics) | 经济学（本科到研究生） | Python 3 标准库 `.py` 建模脚本 |

## 作者与 AI 使用说明

- **作者**：汪亮（bertonwang） · [47608843@qq.com](mailto:47608843@qq.com)
- **AI 使用说明**：本教材的知识框架、正文与 LTspice 示例代码在 AI 辅助下整理生成，并经人工校订与静态自检；公式、数值与仿真结论请以 LTspice 实跑及权威教材、官方文档为准。发现错漏欢迎通过上方邮箱勘误。

## 许可证

本仓库目前**未附带 `LICENSE` 文件**，尚未声明开源许可证。个人学习与课堂教学可直接阅读、使用页面内容；转载、二次分发或商业使用前请先联系作者。外部参考资料与工具的版权归各自维护者所有。
