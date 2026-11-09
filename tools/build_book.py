#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""章节页生成器。

教材正文以 HTML 为唯一呈现形式；本文件保存章节的结构化数据，用于一次性
生成各章 index.html。默认不覆盖已存在文件，因此之后可以直接编辑 HTML，
不用担心被重新生成时冲掉。

用法:
    python3 tools/build_book.py            # 只生成缺失的章节页
    python3 tools/build_book.py --force    # 全部重建（会丢失手工修改，慎用）
    python3 tools/build_book.py --list     # 列出章节 id / 路径 / 状态
"""
from __future__ import annotations

import argparse
import html as html_mod
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOK_TITLE = "模拟电路：从读懂到设计"

P0 = "卷首 · 工具与约定"
P1 = "第一篇 · 电路基础与器件"
P2 = "第二篇 · 核心模拟电路模块"
P3 = "第三篇 · 方法论：从读懂到设计"
P4 = "第四篇 · 综合课程设计"
PA = "附录"


def C(cid, part, folder, title, lede, status="skeleton", goals=None, points=None,
      sections=None, svg="", sims=None, pitfalls=None, exercises=None,
      further=None, hours="2 学时"):
    """一章的全部数据。sections: [(编号, 标题, HTML正文)];
    sims: [{file, title, code, steps, expect}]; 其余为字符串列表。"""
    return dict(id=cid, part=part, folder=folder, title=title, lede=lede,
                status=status, goals=goals or [], points=points or [],
                sections=sections or [], svg=svg, sims=sims or [],
                pitfalls=pitfalls or [], exercises=exercises or [],
                further=further or [], hours=hours)


def sim(file, title, code, steps, expect):
    return dict(file=file, title=title, code=code.strip("\n"),
                steps=steps, expect=expect)


CHAPTERS: list[dict] = [

# ============================ 卷首 ============================
C("00", P0, "part0/00-preface", "绪论：如何阅读这本教材",
  "先约定语言，再开始读电路：符号、单位、先修知识，以及手算与仿真各自负责什么。",
  hours="1 学时",
  goals=["知道本书四篇之间的关系与两种阅读顺序", "能说清直流、交流小信号、大信号三种视图的区别",
         "能列出学习一章时固定要问的四个问题"],
  points=["教学目标与结构", "符号约定（大小写、相量、直流/交流/小信号）", "单位前缀与工程记数法",
          "手算与仿真的分工", "先修数学清单", "教材与工业界分析范式对照"],
  sections=[
      ("0.1", "三类变量，三种视图", """<p>同一张电路图，其实叠了三层信息。读图出错，大多是因为把三层混在一起：</p>
<table><thead><tr><th>视图</th><th>符号习惯</th><th>关心什么</th><th>对应仿真</th></tr></thead><tbody>
<tr><td>直流 / 静态工作点</td><td>大写大写下标，如 <code>V<sub>GS</sub></code>、<code>I<sub>D</sub></code></td><td>偏置是否成立、器件在哪个工作区</td><td><code>.op</code> / <code>.dc</code></td></tr>
<tr><td>交流小信号</td><td>小写，如 <code>v<sub>gs</sub></code>、<code>i<sub>d</sub></code></td><td>增益、阻抗、频率响应、噪声</td><td><code>.ac</code> / <code>.noise</code></td></tr>
<tr><td>大信号 / 瞬态总量</td><td>小写大写下标，如 <code>v<sub>GS</sub>(t)</code></td><td>摆幅、失真、启动、饱和、压摆</td><td><code>.tran</code></td></tr>
</tbody></table>
<p><strong>读图口诀</strong>：先用直流视图确认每个器件“活着”（有正确偏置、在正确工作区），再切到小信号视图算增益与阻抗，最后用瞬态视图检查摆幅和失真。</p>"""),
      ("0.2", "固定要问的四个问题", """<p>后面每一章、每一个电路，都问同样四个问题，答案会自然形成笔记：</p>
<ol><li><strong>直流怎么偏置？</strong>电源到地有没有直流通路？每个节点的静态电压大约多少？</li>
<li><strong>小信号增益怎么算？</strong>控制量是什么（<code>v<sub>be</sub></code> / <code>v<sub>gs</sub></code>）？跨导 <code>g<sub>m</sub></code> 多大？负载阻抗多大？</li>
<li><strong>输入、输出阻抗是多少？</strong>前一级会不会被拖垮？后一级会不会成为负载？</li>
<li><strong>带宽与摆幅边界在哪？</strong>哪个电容形成主极点？输出最高/最低能到多少？</li></ol>"""),
      ("0.3", "手算与仿真的分工", """<p>仿真是<strong>验证</strong>工具，不是<strong>推导</strong>工具。手算给出数量级和趋势，仿真给出精确数值与非理想效应，两者不一致时先怀疑自己的模型假设，而不是先怀疑软件。</p>
<div class=\"card tip\"><p style=\"margin-bottom:0\">推荐记录格式：手算预期值 → 仿真实测值 → 偏差百分比 → 偏差原因。写满 20 组这样的记录，读电路的能力会有明显变化。</p></div>"""),
  ],
  sims=[sim("sim/00-minimal.cir", "最小完整网表：分压器",
            """* Ch00 Minimal netlist: a voltage divider
V1 in 0 DC 5
R1 in out 3k
R2 out 0 2k
.op
.end""",
            "保存为 .cir → LTspice 打开 → Run → View → SPICE Error Log 查看 V(out)。",
            "手算 V(out) = 5 × 2k/(3k+2k) = 2.000 V，电流 1 mA。")],
  pitfalls=["把 m 当成兆：SPICE 里 m = 毫，1Meg = 兆。",
            "只看波形不看工作点：偏置错了，波形也可能“看起来有形状”。"],
  exercises=["把 R2 改成 2k 的 1% 公差，估计 V(out) 的变化范围。",
             "在分压器输出端接 1k 负载，重算 V(out)，再用仿真核对。"],
  further=["<a href='../01-ltspice-quickstart/index.html'>第 1 章 LTspice 快速上手</a>",
           "<a href='../02-spice-netlist/index.html'>第 2 章 SPICE 网表语法</a>",
           "<a href='../../appendix/index.html'>附录 A · 公式与术语速查</a>"]),

C("01", P0, "part0/01-ltspice-quickstart", "LTspice 快速上手",
  "从安装到第一个波形。理解原理图与网表两种工作流，掌握四类基本分析和排错入口。",
  status="done", hours="2 学时",
  goals=["能独立安装 LTspice 并运行一个 .cir 网表", "能区分 .op / .dc / .tran / .ac 各自回答什么问题",
         "会用波形窗口、游标和 SPICE Error Log 取数与排错"],
  points=["安装与界面", ".asc 原理图 / .cir 网表", ".op / .tran / .ac / .dc",
          "Add Trace 与游标测量", "SPICE Error Log 排错", "常用快捷键"],
  sections=[
      ("1.1", "为什么是 LTspice", """<p>LTspice 是 Analog Devices 维护的免费 SPICE 仿真器：启动快、收敛性好、自带大量真实器件模型，工业界与高校都在用。对自学者更关键的一点是——它既能画原理图（<code>.asc</code>），也能直接读纯文本网表（<code>.cir</code> / <code>.net</code>）。</p>
<p>本书统一使用<strong>网表</strong>：<code>.cir</code> 是纯文本，可以放进 Git、可以 diff、可以由 HTML 代码块自动生成，也更容易把“电路”当代码来读。想看原理图时，LTspice 也能把网表里的元件逐一键入画布。</p>"""),
      ("1.2", "四类分析，回答四个问题", """<table><thead><tr><th>指令</th><th>回答的问题</th><th>典型用法</th></tr></thead><tbody>
<tr><td><code>.op</code></td><td>静态工作点：各节点电压、各管 Id / gm / 工作区</td><td>确认偏置是否成立（结果在 Error Log，不弹波形）</td></tr>
<tr><td><code>.dc</code></td><td>某个直流源扫描时，电路怎么变化</td><td>二极管 I-V 曲线、MOS 输出特性、传输曲线</td></tr>
<tr><td><code>.tran</code></td><td>随时间怎么变化</td><td>充放电、放大波形、失真、启动过程、振荡</td></tr>
<tr><td><code>.ac</code></td><td>不同频率下增益与相位</td><td>波特图、带宽、相位裕度、滤波器</td></tr>
</tbody></table>
<p>另有 <code>.noise</code>（噪声）、<code>.tf</code>（直流小信号传递函数与输入/输出电阻）、<code>.four</code>（频谱 / THD），见<a href="../02-spice-netlist/index.html">第 2 章</a>与<a href="../../part3/21-simulation-method/index.html">第 21 章</a>。</p>"""),
      ("1.3", "第一个波形：逐步操作", """<ol>
<li>复制下方代码块，保存为 <code>sim/01-rc-charge.cir</code>（或直接打开仓库里的同名文件）。</li>
<li><code>File → Open</code> 打开它，点工具栏 Run（奔跑小人）。第一次会弹出波形窗口，标题是 <em>Transient Analysis</em>。</li>
<li>右键波形区 → <code>Add Trace</code> → 选 <code>V(out)</code>；也可以先用 <code>V(in)</code> 看激励。</li>
<li>把鼠标移到曲线上，游标会显示坐标；按住左键拖一段可测 Δt、ΔV、斜率。</li>
<li>菜单 <code>View → SPICE Error Log</code>（或 <code>Ctrl+L</code>）里能找到 <code>.meas</code> 的测量结果与警告。</li>
</ol>
<div class="card warn"><span class="card-label">常见坑</span><p style="margin-bottom:0">纯网表没有原理图可点，必须手动 <code>Add Trace</code>；只有 <code>.op</code> 时不会弹出波形窗口，别以为仿真没跑。网表注释请用英文 ASCII，中文注释在部分版本会乱码。</p></div>"""),
      ("1.4", "报错时先看这三处", """<ul><li><strong>Floating node / No DC path to ground</strong>：某节点只有电容或理想电流源相连，SPICE 求不出直流解。给它并联一个大电阻（如 <code>1G</code>）或在电容上加初始条件。</li>
<li><strong>Unknown model / Can't find library</strong>：用了 <code>.model</code> 未定义的器件名，或 <code>.lib</code> 路径不对。本书全部自包含定义模型，不依赖外部库。</li>
<li><strong>Timestep too small / Convergence failed</strong>：瞬态不收敛。检查是否有理想开关、无串联电阻的电容环路、过陡的 <code>PULSE</code> 边沿；给边沿一个有限上升时间（如 <code>1n</code>），必要时加 <code>.options gmin=1n</code>。</li></ul>"""),
  ],
  sims=[sim("sim/01-rc-charge.cir", "实验 1-1：RC 充电与时间常数",
            """* Ch01 RC charging transient - first LTspice run
V1 in 0 PULSE(0 5 0 1u 1u 5m 10m)
R1 in out 10k
C1 out 0 100n
.tran 0 8m 0 10u
* tau = R1*C1 = 1ms ; V(out) = 5*(1-exp(-t/tau))
.meas TRAN v_1m FIND V(out) AT 1m
.meas TRAN v_5m FIND V(out) AT 5m
.end""",
            "Run 后 Add Trace 选 V(out) 与 V(in)；在 Error Log 里读两条 .meas 结果。",
            "τ = 10k × 100n = 1 ms；t = 1 ms 时 V(out) ≈ 5(1−e⁻¹) = 3.16 V；t = 5τ = 5 ms 时约 4.97 V。把 R1 改成 20k，τ 翻倍，曲线变缓。")],
  pitfalls=["以为 .op 会弹波形：它只写 Error Log。", "PULSE 上升时间写 0 导致仿真警告或步长过小，给 1u 这类有限值即可。",
            "直接把波形截图当结论，没有记下手算预期值。"],
  exercises=["把 C1 改成 220n，先手算 t = 1 ms 时的 V(out)，再仿真核对。",
             "添加 .meas 测出 V(out) 到达 2.5 V 的时刻，与 0.693τ 比较。"],
  further=["<a href='../02-spice-netlist/index.html'>第 2 章 SPICE 网表语法与仿真指令</a>",
           "<a href='../../part1/04-passive-dynamics/index.html'>第 4 章 无源元件、暂态与频域</a>",
           "<a href='https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html' target='_blank' rel='noopener'>ADI LTspice 官方下载与文档</a>"]),

C("02", P0, "part0/02-spice-netlist", "SPICE 网表语法与仿真指令",
  "把网表当作一门声明式语言来学：元件是对象，节点是变量，点指令是求解器，.step/.meas 是循环与断言。",
  status="done", hours="3 学时",
  goals=["能读懂并手写任意简单电路的网表", "会用 .param / .step / .meas 做参数扫描与自动测量",
         "知道 .model / .subckt / .include 的组织方式", "遇到收敛问题有排查顺序"],
  points=["元件行 R/C/L/V/I/Q/M/D/E", ".model 与 .param", ".step 参数扫描", ".meas 自动测量",
          ".include / .lib / .subckt", "收敛性与 .options"],
  sections=[
      ("2.1", "网表的五段结构", """<p>一个 <code>.cir</code> 文件只有五类内容，顺序固定：</p>
<ol><li><strong>标题行</strong>：第一行永远是标题，即使写成 <code>*</code> 注释也可以（不要在这里放元件）。</li>
<li><strong>元件行</strong>：名字 + 节点 + 值/模型。元件名首字母决定类型。</li>
<li><strong>模型 / 参数</strong>：<code>.model</code>、<code>.param</code>、<code>.func</code>。</li>
<li><strong>分析与控制</strong>：<code>.op</code>、<code>.tran</code>、<code>.ac</code>、<code>.dc</code>、<code>.step</code>、<code>.meas</code>、<code>.options</code>。</li>
<li><strong>结束</strong>：<code>.end</code>。</li></ol>
<p>注释：整行以 <code>*</code> 开头，行内用 <code>;</code>。节点名可以是数字或字符串，<code>0</code>（或 <code>GND</code>）是全局参考地。</p>"""),
      ("2.2", "元件行速查", """<table><thead><tr><th>首字母</th><th>语法</th><th>示例</th></tr></thead><tbody>
<tr><td>R / C / L</td><td><code>名字 节点+ 节点- 值</code></td><td><code>R1 in out 10k</code></td></tr>
<tr><td>V / I</td><td><code>名字 节点+ 节点- DC 值 AC 幅值 波形</code></td><td><code>V1 in 0 DC 0 AC 1 SINE(0 1 1k)</code></td></tr>
<tr><td>D</td><td><code>名字 阳极 阴极 模型名</code></td><td><code>D1 a 0 DGEN</code></td></tr>
<tr><td>Q</td><td><code>名字 C B E 模型名</code></td><td><code>Q1 out base emit NPN1</code></td></tr>
<tr><td>M</td><td><code>名字 D G S B 模型名 W= L=</code></td><td><code>M1 d g 0 0 NM1 W=10u L=1u</code></td></tr>
<tr><td>E / G / F / H</td><td>受控源，<code>E名 输出+ 输出- 输入+ 输入- 增益</code></td><td><code>E1 out 0 inp inn 1e5</code></td></tr>
<tr><td>B</td><td>行为源，<code>B名 节点+ 节点- V=表达式</code></td><td><code>B1 out 0 V=max(0,V(in))</code></td></tr>
</tbody></table>
<p>激励波形：<code>SINE(Voffset Vamp Freq)</code>、<code>PULSE(V1 V2 Tdelay Trise Tfall Ton Tperiod)</code>、<code>EXP</code>、<code>PWL</code>。</p>"""),
      ("2.3", "单位：最容易踩的坑", """<p>SPICE 大小写不敏感，<code>m</code> 是<strong>毫</strong>，<code>Meg</code> 才是<strong>兆</strong>：<code>1m</code> = 10⁻³，<code>1u</code> = 10⁻⁶，<code>1n</code> = 10⁻⁹，<code>1p</code> = 10⁻¹²，<code>1f</code> = 10⁻¹⁵，<code>1k</code> = 10³，<code>1Meg</code> = 10⁶，<code>1G</code> = 10⁹。写 <code>1M</code> 得到的仍是 1 毫。</p>
<p>网表里不要写单位字母（<code>10k</code> 而不是 <code>10kΩ</code>），不要写千分位逗号。</p>"""),
      ("2.4", "参数化：把仿真变成实验", """<p><code>.param</code> 定义常量，元件值用花括号引用；<code>.step</code> 让同一个网表重复运行；<code>.meas</code> 把结果写成可比较的数字。三者合起来就是“带断言的参数化测试”：</p>
<pre class="spice" data-file="inline"><code>.param Rtop=3k
R1 in out {Rtop}
.step param Rtop list 1k 2k 3k
.meas OP vout FIND V(out)</code></pre>
<p class="code-hint">上面这段是语法片段，不是完整网表；完整可运行版本见下方实验 2-1。</p>
<p><code>.meas</code> 的常用形式：<code>.meas TRAN 名称 FIND V(x) AT 时间</code>、<code>.meas AC 名称 FIND mag(V(x)) AT 频率</code>、<code>.meas TRAN 名称 TRIG ... TARG ...</code>（测延时/上升时间）。结果全部写进 Error Log，可以用脚本解析。</p>"""),
      ("2.5", "模型与层次化", """<p><code>.model 名称 类型(参数...)</code> 定义器件模型，例如 <code>.model NM1 NMOS(Vto=0.5 Kp=200u Lambda=0.02)</code>。Level-1 MOS 模型参数少、行为可预测，特别适合教学；真实工艺模型（BSIM）有上百个参数，反而看不清物理含义。</p>
<p>真实项目里用 <code>.lib 厂商库.lib</code> 引入模型、<code>.subckt / .ends</code> 定义子电路、<code>.include</code> 包含文件、<code>X1 ... 子电路名</code> 实例化。本书为可移植性一律自包含，不用外部库。</p>"""),
      ("2.6", "收敛性速查", """<ol><li>每个节点是否有到地的直流通路（必要时并联 <code>1G</code> 电阻）。</li>
<li>理想电压源是否被电容直接短路、两个理想电压源是否并联（加小串联电阻）。</li>
<li><code>PULSE</code> 边沿是否过陡（给有限 <code>Trise/Tfall</code>）。</li>
<li>先跑 <code>.op</code> 确认工作点，再跑 <code>.tran</code>。</li>
<li>最后才动 <code>.options</code>（<code>gmin</code>、<code>abstol</code>、<code>reltol</code>、<code>maxstep</code>）——改容差是掩盖问题，不是解决问题。</li></ol>"""),
  ],
  sims=[sim("sim/02-param-divider.cir", "实验 2-1：参数化分压器 + 扫描 + 自动测量",
            """* Ch02 Netlist syntax: params, step and automatic measurements
.param Rtop=3k
V1 in 0 DC 5
R1 in out {Rtop}
R2 out 0 2k
.step param Rtop list 1k 2k 3k 4k
.op
.meas OP vout FIND V(out)
.meas OP ir1 FIND I(R1)
.end""",
            "Run → View → SPICE Error Log，找到 4 组 vout / ir1 的测量值。",
            "V(out) = 5×2k/(Rtop+2k)：Rtop = 1k/2k/3k/4k 时分别为 3.333 / 2.500 / 2.000 / 1.667 V。"),
       sim("sim/02-ac-source.cir", "实验 2-2：同一电路的 AC 与 DC 两种视图",
           """* Ch02 AC source specification and a small-signal sweep
V1 in 0 DC 0 AC 1
R1 in out 1k
C1 out 0 100n
.ac dec 20 10 100k
.meas AC g10 FIND mag(V(out)) AT 10
.meas AC g1k FIND mag(V(out)) AT 1k
.end""",
           "Run → Add Trace → V(out)，右键纵坐标可切到 dB 显示。",
           "低频增益约 1（0 dB）；fc = 1/(2πRC) ≈ 1.59 kHz；1 kHz 处 |H| ≈ 0.846。")],
  pitfalls=["用 1M 表示 1 兆：实际是 1 毫。", "把 .param 写在元件行之后才引用：LTspice 允许，但为可读性放在前面。",
            "网表里写中文注释或中文节点名：部分版本会报语法错。", "把原理图 .asc 当成文本网表直接改：.asc 有自己的语法，本书不涉及。"],
  exercises=["给实验 2-1 增加 .step param Rtop 的第五个值，并预测 vout。",
             "把实验 2-2 的 C1 增大 10 倍，用 .meas 验证 fc 下降 10 倍。",
             "用 .subckt 把分压器封装成模块，再实例化两次。"],
  further=["<a href='../01-ltspice-quickstart/index.html'>第 1 章 LTspice 快速上手</a>",
           "<a href='../../part3/21-simulation-method/index.html'>第 21 章 仿真方法论</a>",
           "<a href='../../appendix/index.html'>附录 A · SPICE 指令速查</a>",
           "<a href='https://github.com/nunobrum/PyLTSpice' target='_blank' rel='noopener'>PyLTSpice：用 Python 批量改网表并运行</a>"]),

# ============================ 第一篇 ============================
C("03", P1, "part1/03-circuit-laws", "电路定律与读图第一步",
  "所有复杂电路都从这一步开始：标节点、定参考地、写 KCL，先求直流，再看信号。",
  status="done", hours="3 学时",
  goals=["能对任意电阻网络标出节点、写出节点电压方程", "能识别分压器的负载效应并用戴维南等效解释",
         "会用 .op / .tf 验证手算的增益、输入电阻与输出电阻", "养成“先直流、后交流”的读图顺序"],
  points=["节点与参考地", "KCL / KVL / 欧姆定律", "分压与分流、负载效应",
          "叠加、戴维南 / 诺顿", "节点电压法", "受控源与 .tf"],
  svg="""<svg viewBox="0 0 430 210" width="430" role="img" aria-label="带负载的分压器电路图">
  <g class="wire">
    <path d="M60 40 H210 M60 40 V160 H210 M270 40 H370 M270 160 H370 M370 40 V160"/>
    <path d="M210 40 V60 M210 130 V160 M270 40 V60 M270 130 V160"/>
  </g>
  <rect class="part" x="200" y="60" width="20" height="70" rx="2"/>
  <rect class="part" x="260" y="60" width="20" height="70" rx="2"/>
  <rect class="part" x="360" y="85" width="20" height="50" rx="2"/>
  <circle class="part" cx="60" cy="100" r="18"/>
  <text class="lbl" x="50" y="106">+</text><text class="lbl" x="92" y="106">V1</text>
  <text class="lbl" x="48" y="130">10 V</text>
  <text class="lbl" x="226" y="100">R1</text><text class="lbl-s" x="226" y="118">10k</text>
  <text class="lbl" x="286" y="100">R2</text><text class="lbl-s" x="286" y="118">10k</text>
  <text class="lbl" x="388" y="115">RL</text><text class="lbl-s" x="388" y="133">10k</text>
  <circle class="node" cx="240" cy="40" r="4"/><text class="lbl-s" x="230" y="30">out</text>
  <circle class="node" cx="60" cy="160" r="4"/><text class="lbl-s" x="30" y="182">0 (GND)</text>
  <text class="lbl-s" x="120" y="182">R2 与 RL 并联 → 分压比被改变</text>
</svg>""",
  sections=[
      ("3.1", "读图第一步：标节点、定参考地", """<p>电压永远是<strong>两点之间</strong>的差。所谓“某点电压”，默认指它相对参考地（节点 <code>0</code>）的电位。读图时先做三件笨功夫，能消掉一半的错误：</p>
<ol><li>把所有由理想导线直连的点圈成同一个节点，给每个节点起名字（<code>in</code>、<code>out</code>、<code>bias</code>…），别用自动生成的 <code>N001</code>。</li>
<li>找出参考地，以及电源正负端；画一条从电源正端经器件到地的直流通路。</li>
<li>在图上标出你猜的电位高低（<code>+</code> / <code>−</code>）和电流方向。猜错没关系，算出负值就说明方向反了。</li></ol>
<p>本书所有网表都用有意义的节点名，正是为了训练这个习惯。<a href="../../part3/19-read-circuit/index.html">第 19 章</a>会把它扩展成完整的十步法。</p>"""),
      ("3.2", "KCL / KVL 与节点电压法", """<p>KCL：任一节点流入电流之和等于流出之和（本质是电荷守恒）。KVL：沿任一闭合回路电压降之和为零（本质是能量守恒）。实际手算时，<strong>节点电压法</strong>最不容易出错：以地为参考，对每个未知节点写一条“流出电流总和 = 0"，得到线性方程组。</p>
<span class="eq">V<sub>out</sub> = V<sub>1</sub> · (R<sub>2</sub> ∥ R<sub>L</sub>) / [ R<sub>1</sub> + (R<sub>2</sub> ∥ R<sub>L</sub>) ]</span>
<p>上式就是下方电路的手算结果：R₂∥R_L = 5k，所以 V(out) = 10 × 5/(10+5) = 3.333 V，而不是“想当然”的 5 V。</p>"""),
      ("3.3", "负载效应与戴维南等效", """<p>把分压器从 <code>out</code> 看进去：开路电压 <em>V</em><sub>th</sub> = 5 V（R₁=R₂ 时），等效内阻 <em>R</em><sub>th</sub> = R₁∥R₂ = 5k。接上 R_L = 10k 后，输出变成 5 × 10k/(5k+10k) = 3.333 V。<strong>戴维南等效是“读懂前后级相互影响”的核心工具</strong>：前一级是源，后一级是负载，两者用 V<sub>th</sub> 和 R<sub>th</sub> 对话。</p>
<div class="card note"><p style="margin-bottom:0">工程判据：若希望分压比不被后级明显改变，一般要求 R<sub>th</sub> ≤ R<sub>L</sub>/10（即分压电流约为负载电流的 10 倍）。代价是功耗增大——模拟设计里到处都是这种取舍。</p></div>"""),
      ("3.4", "叠加、受控源与 .tf", """<p>线性电路中多个独立源的贡献可以分别计算再相加（叠加）；关掉电压源＝短路，关掉电流源＝开路。含<strong>受控源</strong>（晶体管小信号模型、运放模型）时叠加仍可用，但受控源不能关掉。</p>
<p><code>.tf V(out) V1</code> 让 SPICE 直接给出三件事：直流小信号增益 <code>V(out)/V1</code>、从 V1 看进去的输入电阻、从 <code>out</code> 看进去的输出电阻。它是验证戴维南手算最快的工具。</p>"""),
  ],
  sims=[sim("sim/03-divider-thevenin.cir", "实验 3-1：分压器、负载效应与 .tf 验证",
            """* Ch03 Divider with load: verify Thevenin by .tf
V1 in 0 DC 10
R1 in out 10k
R2 out 0 10k
RL out 0 10k
.op
.tf V(out) V1
.end""",
            "Run → View → SPICE Error Log，读 V(out)、transfer function、input / output impedance。",
            "V(out) = 3.333 V；V(out)/V1 = 0.3333；从 V1 看进去 R_in = R1 + (R2∥RL) = 15k；从 out 看进去 R_out = R1∥R2 = 5k。"),
       sim("sim/03-load-sweep.cir", "实验 3-2：负载从 1k 扫到 1Meg",
           """* Ch03 Load effect sweep
.param RLv=10k
V1 in 0 DC 10
R1 in out 10k
R2 out 0 10k
RL out 0 {RLv}
.step param RLv list 1k 10k 100k 1Meg
.op
.meas OP vout FIND V(out)
.end""",
            "Run → Error Log 里比较 4 个 vout；或把 V(out) 加到波形窗口看随 step 的变化。",
            "RL = 1k / 10k / 100k / 1Meg 时 V(out) ≈ 0.909 / 3.333 / 4.762 / 4.975 V，逐渐逼近开路值 5 V。")],
  pitfalls=["忘了后级输入阻抗也是负载，把分压器当理想电压源。", "把参考地当成“真实的地”：它只是人为选定的零电位参考点。",
            "KCL 方程里电流方向随意混用，导致符号错误；先统一假设方向再写。"],
  exercises=["手算 R1=4.7k、R2=10k、RL=2.2k 时的 V(out)，再用实验 3-1 的网表改值核对。",
             "用 .tf 求实验 3-2 在 RL=100k 时的输出电阻，解释为何与 R1∥R2 有关。",
             "把 V1 换成 5 V 加一个 1 V 的交流小信号，用叠加法分别算两个源对 V(out) 的贡献。"],
  further=["<a href='../04-passive-dynamics/index.html'>第 4 章 无源元件、暂态与频域</a>",
           "<a href='../../part3/19-read-circuit/index.html'>第 19 章 如何读懂一个陌生电路</a>",
           "<a href='../../appendix/index.html'>附录 A · 常用公式</a>"]),

C("04", P1, "part1/04-passive-dynamics", "无源元件、暂态与频域",
  "从时间常数到波特图：把 R/L/C 的时域行为与频域行为看成同一件事的两种表述。",
  hours="4 学时",
  goals=["能求一阶电路的时间常数并画出充放电曲线", "能写出 RC 低通的传递函数并指出 -3 dB 频率",
         "理解二阶系统的阻尼、谐振与 Q 值", "能用 .ac 扫频验证手算的零极点"],
  points=["实际元件寄生参数", "时间常数与充放电", "二阶系统与阻尼", "阻抗 / 相量 / 复数",
          "传递函数与零极点", "波特图与 -3 dB"],
  sims=[sim("sim/04-rc-lowpass.cir", "实验 4-1：RC 低通的频响",
            """* Ch04 RC low-pass: transfer function and -3dB point
V1 in 0 DC 0 AC 1
R1 in out 1k
C1 out 0 100n
.ac dec 30 10 100k
.meas AC g10 FIND mag(V(out)) AT 10
.meas AC g1k FIND mag(V(out)) AT 1k
.meas AC g10k FIND mag(V(out)) AT 10k
.end""",
            "Run → Add Trace → V(out)；纵坐标右键切 dB；Error Log 读三条 .meas。",
            "fc = 1/(2πRC) ≈ 1.59 kHz；10 Hz 处增益 ≈ 1；1 kHz 处 ≈ 0.846；10 kHz 处 ≈ 0.157。"),
       sim("sim/04-rlc-resonance.cir", "实验 4-2：RLC 串联谐振",
           """* Ch04 RLC series resonance (voltage across C)
V1 in 0 DC 0 AC 1
R1 in n1 10
L1 n1 out 10m
C1 out 0 100n
.ac dec 40 100 100k
.meas AC peak MAX mag(V(out))
.end""",
            "Run → Add Trace → V(out)，观察谐振峰；把 R1 改成 100 再看峰高变化。",
            "f0 = 1/(2π√(LC)) ≈ 5.03 kHz；电容上的峰值电压约等于 Q ≈ (1/R)·√(L/C) ≈ 31.6 倍输入。")],
  pitfalls=["把 -3 dB 当成“幅度降为 0.3”：其实是 1/√2 ≈ 0.707。", "忽略电容的 ESR，导致高频段仿真与实测不符。",
            "在 .ac 分析里用 SINE 源 expecting 时域波形：.ac 只看 AC 幅值。"],
  exercises=["手算实验 4-1 在 1 kHz 处的相位，再用波形窗口的相位显示核对。",
             "把实验 4-2 的 R1 依次改为 10 / 100 / 1k，记录峰值与带宽，总结 Q 的规律。"],
  further=["<a href='../03-circuit-laws/index.html'>第 3 章 电路定律与读图第一步</a>",
           "<a href='../../part2/12-frequency-response/index.html'>第 12 章 频率响应与极点</a>",
           "<a href='../../part2/15-active-filters/index.html'>第 15 章 有源滤波器</a>"]),

C("05", P1, "part1/05-diode", "二极管与整流、限幅电路",
  "第一个非线性器件。重点不是背公式，而是学会“假设导通/截止 → 验证”这一读图动作。",
  status="done", hours="3 学时",
  goals=["会用指数模型、恒压降模型、理想开关模型分别估算二极管电路",
         "能用假设-验证法判断二极管导通状态", "能分析整流、滤波、限幅与钳位电路的波形",
         "会用 .dc 扫描得到 I-V 曲线"],
  points=["PN 结与肖克利方程", "恒压降 / 分段线性模型", "半波与全波整流",
          "限幅与钳位", "稳压二极管", ".dc 扫描 I-V 曲线"],
  svg="""<svg viewBox="0 0 460 200" width="460" role="img" aria-label="半波整流与电容滤波电路">
  <g class="wire">
    <path d="M50 60 H130 M170 60 H260 M260 60 V150 H50 M400 60 V150 M260 150 H400"/>
    <path d="M300 60 V80 M300 120 V150 M360 60 V80 M360 120 V150"/>
  </g>
  <circle class="part" cx="80" cy="60" r="18"/>
  <text class="lbl" x="68" y="66">~</text><text class="lbl-s" x="60" y="92">V1 50Hz</text>
  <path class="part" d="M130 45 L170 60 L130 75 Z"/>
  <path class="wire" d="M170 45 V75"/>
  <text class="lbl-s" x="130" y="34">D1</text>
  <path class="wire" d="M300 80 H320 M320 80 H340 M340 80 H360"/>
  <path class="wire" d="M318 80 V96 M342 80 V96"/>
  <rect class="part" x="292" y="100" width="16" height="20" rx="1"/>
  <rect class="part" x="352" y="100" width="16" height="20" rx="1"/>
  <text class="lbl-s" x="292" y="140">C1</text><text class="lbl-s" x="352" y="140">R1</text>
  <circle class="node" cx="260" cy="60" r="4"/><text class="lbl-s" x="248" y="48">dc_out</text>
  <circle class="node" cx="260" cy="150" r="4"/><text class="lbl-s" x="240" y="172">0</text>
</svg>""",
  sections=[
      ("5.1", "指数模型与三个近似层", """<p>PN 结的直流行为由肖克利方程描述：</p>
<span class="eq">I<sub>D</sub> = I<sub>S</sub> ( e<sup>V<sub>D</sub>/(n V<sub>T</sub>)</sup> − 1 )，　V<sub>T</sub> = kT/q ≈ 26 mV（室温）</span>
<p>手算时按精度需求选一层近似，<strong>这一步选择本身就是读图能力</strong>：</p>
<table><thead><tr><th>模型</th><th>假设</th><th>适用</th></tr></thead><tbody>
<tr><td>理想开关</td><td>正偏短路、反偏开路</td><td>判断整流电路“哪条路通”，做逻辑级分析</td></tr>
<tr><td>恒压降</td><td>导通后 V<sub>D</sub> ≈ 0.7 V（硅）</td><td>手算输出电压、限幅电平</td></tr>
<tr><td>分段线性</td><td>0.7 V + 小电阻 r<sub>d</sub></td><td>估算纹波、导通压降随电流变化</td></tr>
<tr><td>指数 / SPICE</td><td>完整方程 + 结电容 + 反向恢复</td><td>仿真、小信号电阻 r<sub>d</sub> = nV<sub>T</sub>/I<sub>D</sub>、温度特性</td></tr>
</tbody></table>"""),
      ("5.2", "假设—验证法：读二极管电路的通用动作", """<ol><li>先假设每个二极管的状态（导通 / 截止），把导通的换成 0.7 V 电压源，截止的换成开路。</li>
<li>在这个<strong>线性化</strong>的电路里求各节点电压与二极管电流。</li>
<li>逐条验证：假设导通的，电流方向是否为正？假设截止的，阳极电位是否真的低于阴极 + 0.7 V？</li>
<li>若有矛盾，改假设重算。两个以上二极管时，从最“确定”的那个开始（例如接最高电位的那一路）。</li></ol>
<div class="card tip"><span class="card-label">迁移价值</span><p style="margin-bottom:0">同样的动作会反复出现在第 6 章判断 MOS 工作区、第 7 章判断 BJT 放大/饱和、第 16 章判断比较器状态。<strong>先假设、再线性化、后验证</strong>，是所有非线性电路的统一读法。</p></div>"""),
      ("5.3", "整流、滤波与纹波", """<p>半波整流只让正半周通过；加滤波电容后，电容在峰值附近被充电、在其余时间向负载放电，输出变成带纹波的直流。纹波峰峰值近似：</p>
<span class="eq">ΔV ≈ I<sub>load</sub> / (f · C)　（半波，f 为电网频率）</span>
<p>电流越大、频率越低、电容越小，纹波越大。全波（桥式）整流的等效充电频率是 2f，纹波减半。仿真里用 <code>.tran</code> 能看到真实的充放电尖峰，这是 <code>.ac</code> 做不到的——非线性电路必须用瞬态分析。</p>"""),
      ("5.4", "限幅、钳位与稳压", """<ul><li><strong>限幅（clip / limiter）</strong>：用二极管把电压钉在某个电平上，常用于保护 ADC 输入。串一个电阻限流是必须的。</li>
<li><strong>钳位（clamp）</strong>：电容 + 二极管把整个波形的直流电平搬移，波形形状不变、“底座”变了。</li>
<li><strong>稳压二极管</strong>：工作在反向击穿区（SPICE 模型里用 <code>Bv</code> / <code>Ibv</code> 指定），需串联限流电阻，并校核功耗。</li></ul>"""),
  ],
  sims=[sim("sim/05-diode-iv.cir", "实验 5-1：二极管的 I-V 曲线",
            """* Ch05 Diode I-V curve by DC sweep
.model DGEN D(Is=1n N=1.7 Rs=0.5)
V1 a 0 DC 0
D1 a 0 DGEN
.dc V1 -0.2 0.8 0.005
.end""",
            "Run → Add Trace → I(D1)；横坐标是 V(a)。",
            "正向约 0.6～0.7 V 开始明显导通，电流随电压指数上升；反向只有极小的漏电流。"),
       sim("sim/05-halfwave.cir", "实验 5-2：半波整流与电容滤波",
           """* Ch05 Half-wave rectifier with smoothing capacitor
.model DGEN D(Is=1n N=1.7 Rs=0.5)
V1 ac_in 0 SINE(0 5 50)
D1 ac_in dc_out DGEN
C1 dc_out 0 10u
R1 dc_out 0 1k
.tran 0 100m 0 100u
.meas TRAN vmax MAX V(dc_out)
.meas TRAN vmin MIN V(dc_out) FROM 40m
.end""",
            "Run → Add Trace → V(ac_in) 与 V(dc_out)；Error Log 读 vmax / vmin 估算纹波。",
            "峰值约 4.3～4.5 V（扣掉二极管压降）；纹波 ΔV ≈ I/(fC) ≈ 4.3 mA/(50·10µ) ≈ 8.6 V 的估值在轻载下偏大，实际由放电时间常数 10 ms 决定——正好说明近似式的适用边界。把 C1 改成 100u，纹波明显变小。")],
  pitfalls=["用 .ac 分析整流器：非线性电路的小信号线性化会给出完全错误的结果。",
            "二极管直接并在理想电压源上：电流无穷大，仿真必不收敛，必须串限流电阻。",
            "忘记二极管的反向恢复与结电容，高频开关电路里仿真会过于“干净”。"],
  exercises=["把实验 5-2 改成桥式全波整流（4 个二极管），比较纹波频率与幅值。",
             "用两个二极管搭一个 ±1.4 V 对称限幅器，.tran 验证输出电平。",
             "改变 .model 里的 Is，观察 I-V 曲线如何平移并解释温度趋势。"],
  further=["<a href='../06-mosfet/index.html'>第 6 章 MOSFET 与两级模型</a>",
           "<a href='../../part2/17-power-supply/index.html'>第 17 章 电源与功率电路</a>",
           "<a href='https://www.ecircuitcenter.com/' target='_blank' rel='noopener'>eCircuit Center · Diode circuits</a>"]),

C("06", P1, "part1/06-mosfet", "MOSFET 与两级模型",
  "现代模拟电路的主角。同一张图要能用“大信号”和“小信号”两套视图各读一遍。",
  status="done", hours="4 学时",
  goals=["能由 VGS、VDS、Vto 判断 NMOS 的三个工作区", "会计算 Id、gm、ro 与本征增益",
         "能画出共源放大器的小信号等效电路并估算增益", "会读 MOS 输出特性曲线族",
         "知道 Level-1 SPICE 模型各参数的物理含义"],
  points=["截止 / 线性 / 饱和", "阈值电压与体效应", "gm / ro / 本征增益",
          "小信号等效电路", ".model NMOS 参数", "输出特性曲线族"],
  svg="""<svg viewBox="0 0 400 230" width="400" role="img" aria-label="共源放大器电路图">
  <g class="wire">
    <path d="M80 30 H210 M80 30 V70 M210 30 V50"/>
    <path d="M80 120 V160 M210 90 V200 M80 200 H210"/>
    <path d="M40 120 H100 M40 120 V160 H100"/>
    <path d="M290 30 H330 M290 120 H330 M330 30 V120"/>
  </g>
  <rect class="part" x="196" y="50" width="28" height="40" rx="2"/>
  <text class="lbl-s" x="230" y="52">RD 2k</text>
  <rect class="part" x="130" y="95" width="60" height="70" rx="4"/>
  <text class="lbl" x="140" y="125">M1</text><text class="lbl-s" x="138" y="148">NMOS</text>
  <path class="wire" d="M130 115 H100 M130 145 H100 M160 165 V200"/>
  <circle class="part" cx="70" cy="140" r="18"/>
  <text class="lbl-s" x="48" y="182">VIN</text>
  <text class="lbl-s" x="60" y="22">VDD 5V</text>
  <circle class="node" cx="210" cy="90" r="4"/><text class="lbl-s" x="218" y="92">out</text>
  <path class="wire" d="M210 90 H290"/>
  <rect class="part" x="326" y="60" width="16" height="36" rx="1"/>
  <text class="lbl-s" x="346" y="82">CL</text>
  <circle class="node" cx="80" cy="200" r="4"/><text class="lbl-s" x="56" y="222">0</text>
</svg>""",
  sections=[
      ("6.1", "三个工作区与判据", """<p>以增强型 NMOS 为例（源极接地、体接地），令过驱动电压 <em>V</em><sub>ov</sub> = <em>V</em><sub>GS</sub> − <em>V</em><sub>to</sub>：</p>
<table><thead><tr><th>工作区</th><th>判据</th><th>电流</th><th>用途</th></tr></thead><tbody>
<tr><td>截止</td><td>V<sub>GS</sub> &lt; V<sub>to</sub></td><td>I<sub>D</sub> ≈ 0</td><td>开关断开</td></tr>
<tr><td>线性 / 三极管区</td><td>V<sub>GS</sub> &gt; V<sub>to</sub> 且 V<sub>DS</sub> &lt; V<sub>ov</sub></td><td>I<sub>D</sub> ≈ μ<sub>n</sub>C<sub>ox</sub>(W/L)[V<sub>ov</sub>V<sub>DS</sub> − V<sub>DS</sub>²/2]</td><td>开关闭合、可变电阻</td></tr>
<tr><td>饱和区</td><td>V<sub>GS</sub> &gt; V<sub>to</sub> 且 V<sub>DS</sub> ≥ V<sub>ov</sub></td><td>I<sub>D</sub> ≈ ½ μ<sub>n</sub>C<sub>ox</sub>(W/L) V<sub>ov</sub>² (1+λV<sub>DS</sub>)</td><td><strong>放大器必须在这里</strong></td></tr>
</tbody></table>
<p>在 SPICE Level-1 模型里 <code>Kp = μCox</code>。下方实验用 <code>Kp=200u</code>、<code>W/L=10</code>，于是 <code>½·Kp·(W/L) = 1 mA/V²</code>：V<sub>ov</sub> = 1 V 时 I<sub>D</sub> ≈ 1 mA，很好记。</p>"""),
      ("6.2", "小信号模型：把非线性变成线性", """<p>在静态工作点附近做泰勒展开，只保留一阶项，MOS 就变成三个元件：</p>
<span class="eq">g<sub>m</sub> = 2I<sub>D</sub>/V<sub>ov</sub> = √(2 K<sub>p</sub>(W/L) I<sub>D</sub>)，　r<sub>o</sub> ≈ 1/(λ I<sub>D</sub>)，　A<sub>0</sub> = g<sub>m</sub>r<sub>o</sub></span>
<ul><li><strong>压控电流源 g<sub>m</sub>v<sub>gs</sub></strong>：栅压变化引起漏流变化，这是放大的来源。</li>
<li><strong>输出电阻 r<sub>o</sub></strong>：沟道长度调制（λ）造成；λ 越小、L 越大，r<sub>o</sub> 越大。</li>
<li><strong>栅极开路</strong>：低频下输入电阻极高，这是 MOS 相对 BJT 的关键优势。</li></ul>
<p>共源放大器增益 <em>A</em><sub>v</sub> ≈ −g<sub>m</sub>(R<sub>D</sub> ∥ r<sub>o</sub>)。用实验 6-2 的参数：I<sub>D</sub> ≈ 1 mA，g<sub>m</sub> = 2 mA/V，r<sub>o</sub> = 50k，R<sub>D</sub>∥r<sub>o</sub> = 1.92k → 增益 ≈ −3.85，与仿真相符。</p>"""),
      ("6.3", "同一张图，两种读法", """<p><strong>大信号读法</strong>：把电容开路、电感短路、交流源置零，只留直流电源 → 求静态工作点（每个管子在哪个区、V(out) 是多少、摆幅还剩多少）。<strong>小信号读法</strong>：把直流电源置为交流地、把耦合/旁路电容视为短路、把管子换成 g<sub>m</sub>/r<sub>o</sub> 模型 → 求增益、阻抗、带宽。</p>
<div class="card note"><p style="margin-bottom:0">这两套视图的切换是模拟电路最重要的思维动作，也是<a href="../../part3/19-read-circuit/index.html">第 19 章十步法</a>的第 4、5 步。仿真里对应 <code>.op</code>（大信号）与 <code>.ac</code>（小信号）。</p></div>"""),
      ("6.4", "读输出特性曲线族", """<p>实验 6-1 画出 I<sub>D</sub>–V<sub>DS</sub> 曲线，每条对应一个 V<sub>GS</sub>。读图时看三处：</p>
<ol><li>左侧陡升段 = 线性区；右侧近似水平段 = 饱和区，两段的分界约在 V<sub>DS</sub> = V<sub>ov</sub>。</li>
<li>水平段的<strong>斜率</strong> = 1/r<sub>o</sub>（λ 越大越斜）；水平段的<strong>高度</strong>随 V<sub>GS</sub> 按平方律增长。</li>
<li>把负载电阻的 I–V 关系也画上去（负载线），两线交点就是静态工作点。</li></ol>"""),
  ],
  sims=[sim("sim/06-mos-iv.cir", "实验 6-1：NMOS 输出特性曲线族",
            """* Ch06 NMOS Id-Vds family by VGS stepping
.model NM1 NMOS(Vto=0.5 Kp=200u Lambda=0.02)
.param VGSET=1.5
VDS d 0 DC 0
VGS g 0 DC {VGSET}
M1 d g 0 0 NM1 W=10u L=1u
.dc VDS 0 3 0.02
.step param VGSET list 1.0 1.5 2.0 2.5
.end""",
            "Run → Add Trace → I(M1)（或 Id(M1)），可看到 4 条曲线。",
            "VGS=1.5 V 时 Vov=1 V，饱和区 Id ≈ 1 mA；VGS=2.5 V 时 Vov=2 V，Id ≈ 4 mA（平方律）。曲线右端上翘来自 Lambda。"),
       sim("sim/06-common-source.cir", "实验 6-2：共源放大的工作点与增益",
           """* Ch06 Common-source amplifier: .op, .ac and .tran
.model NM1 NMOS(Vto=0.5 Kp=200u Lambda=0.02)
VDD vdd 0 DC 5
VIN in 0 DC 1.5 AC 0.01 SINE(1.5 0.01 1k)
RD vdd out 2k
M1 out in 0 0 NM1 W=10u L=1u
.op
.ac dec 20 100 10Meg
.tran 0 5m 0 2u
.meas TRAN vin_pp PP V(in) FROM 2m
.meas TRAN vout_pp PP V(out) FROM 2m
.end""",
            "Run → Error Log 读工作点（Id、gm、Vout）与两条 .meas；Add Trace 看 V(out) 与 V(in) 反相。",
            "V(out) ≈ 3 V，Id ≈ 1 mA，gm ≈ 2 mS；增益 ≈ −3.85（输出与输入反相）。把 RD 改成 4k，先检查输出是否仍有足够 VDS 维持饱和，再看增益是否翻倍。")],
  pitfalls=["把 VDS ≥ Vov 记成 VDS ≥ Vto：饱和判据用的是过驱动电压。",
            "用 .ac 仿真时忘了给源写 AC 幅值，结果全为 0。",
            "只看增益不看工作点：RD 太大会把管子推入线性区，公式失效。",
            "把体（bulk）随便接地：集成电路里 NMOS 体接最低电位，PMOS 体接最高电位；体效应会抬高 Vto。"],
  exercises=["在实验 6-2 中加 500 Ω 源极退化电阻，先手算增益再仿真（提示：增益约 −RD/(RS+1/gm)）。",
             "把 L 从 1u 改成 2u，解释 Id、gm、ro 各自怎么变。",
             "用 .op 输出确认 M1 处于饱和区，并写出验证所用的两个电压值。"],
  further=["<a href='../07-bjt/index.html'>第 7 章 BJT 与三种基本组态（对照记忆）</a>",
           "<a href='../../part2/09-single-stage/index.html'>第 9 章 单级放大器</a>",
           "<a href='../../part3/19-read-circuit/index.html'>第 19 章 如何读懂一个陌生电路</a>"]),

C("07", P1, "part1/07-bjt", "BJT 与三种基本组态",
  "与 MOS 对照着学：控制量从 VGS 变成 VBE，输入电阻从无穷变成有限，其余推理框架完全一样。",
  hours="3 学时",
  goals=["能判断 BJT 的放大/饱和/截止区", "会算 gm、rπ、ro 并画出小信号模型",
         "能说出共射/共集/共基三种组态的增益与阻抗特征", "能列出 BJT 与 MOS 的对照表"],
  points=["放大 / 饱和 / 截止区", "β 与 Ic-Vbe", "gm / rπ / ro", "共射 / 共集 / 共基",
          "偏置电路", "与 MOS 对照表"],
  sims=[sim("sim/07-common-emitter.cir", "实验 7-1：分压偏置的共射放大器",
            """* Ch07 Common-emitter amplifier with divider bias
.model NPN1 NPN(Is=1e-15 Bf=200 Vaf=100)
VDD vdd 0 DC 12
R1 vdd base 100k
R2 base 0 20k
RC vdd out 4.7k
RE emit 0 1k
Q1 out base emit NPN1
VIN in 0 DC 0 AC 0.01 SINE(0 0.01 1k)
CIN base in 10u
.op
.tran 0 5m 0 2u
.ac dec 20 10 1Meg
.end""",
            "Run → Error Log 读静态工作点；Add Trace 看 V(out) 与 V(in) 的相位关系。",
            "基极约 2 V、发射极约 1.3 V、Ie ≈ 1.3 mA、Vc ≈ 5.9 V；增益约 −gm·RC，其中 gm ≈ Ic/26mV ≈ 50 mS，故增益可达上百倍（本例受 RE 影响会小一些）。")],
  pitfalls=["把 β 当成设计常量：β 随器件、温度、电流大幅变化，好的偏置电路必须对它不敏感。",
            "忘记基极电流会加载分压器：分压电流应远大于 Ib。",
            "把共集（射随器）误认为没有增益就“没用”：它的价值是阻抗变换。"],
  exercises=["把 RE 拆成两半，只旁路一半，推导并仿真验证增益变化。",
             "把 CIN 改成 100n，用 .ac 观察低频截止点如何上移。"],
  further=["<a href='../06-mosfet/index.html'>第 6 章 MOSFET 与两级模型</a>",
           "<a href='../../part2/09-single-stage/index.html'>第 9 章 单级放大器</a>"]),

C("08", P1, "part1/08-opamp-basics", "理想运放与负反馈入门",
  "把运放当作一块带反馈的积木，但要清楚“虚短虚断”什么时候才成立。",
  status="done", hours="3 学时",
  goals=["能说出理想运放三条假设及虚短虚断的适用条件", "能推导四种基本组态的闭环增益",
         "会判断一个含运放电路是否存在负反馈", "知道理想模型的四个边界并会用 E 源自建运放模型"],
  points=["理想运放三条假设", "虚短 / 虚断的判据", "反相 / 同相 / 跟随 / 差分",
          "负反馈与闭环增益", "饱和与压摆", "用 E 源自建运放模型"],
  svg="""<svg viewBox="0 0 420 210" width="420" role="img" aria-label="同相放大器电路图">
  <g class="wire">
    <path d="M40 110 H120 M120 110 V70 H200 M200 70 V90"/>
    <path d="M280 110 H350 M350 110 V170 H120 M120 170 V140"/>
    <path d="M280 110 V40 H200 M200 40 V170 M200 170 H120"/>
  </g>
  <path class="part" d="M200 65 L200 155 L280 110 Z"/>
  <text class="lbl" x="216" y="106">+</text><text class="lbl" x="216" y="140">−</text>
  <text class="lbl-s" x="228" y="86">E1 / OA</text>
  <rect class="part" x="234" y="164" width="40" height="12" rx="1"/>
  <text class="lbl-s" x="236" y="190">R2 1k</text>
  <rect class="part" x="150" y="164" width="40" height="12" rx="1"/>
  <text class="lbl-s" x="150" y="190">R3 9k</text>
  <circle class="part" cx="80" cy="110" r="16"/>
  <text class="lbl-s" x="56" y="140">VIN</text>
  <circle class="node" cx="350" cy="110" r="4"/><text class="lbl-s" x="356" y="106">oa</text>
  <circle class="node" cx="200" cy="170" r="4"/><text class="lbl-s" x="204" y="188">minus (反馈节点)</text>
</svg>""",
  sections=[
      ("8.1", "三条假设与虚短虚断的适用条件", """<p>理想运放：<strong>开环增益无穷大、输入电阻无穷大、输出电阻为零</strong>。由此得到教科书里的两条捷径：</p>
<ul><li><strong>虚断</strong>：输入端不取电流（i₊ = i₋ = 0）——只要运放未损坏，这条基本总成立。</li>
<li><strong>虚短</strong>：v₊ = v₋ —— <em>仅在“负反馈 + 线性区”时才成立</em>。</li></ul>
<div class="card warn"><span class="card-label">最常见的误用</span><p style="margin-bottom:0">比较器工作在开环、输出饱和，此时 v₊ ≠ v₋，虚短完全失效。判断顺序永远是：<strong>先找反馈通路 → 判断正负 → 假设线性区求解 → 再检查输出是否落在电源轨内</strong>；若超出，则改为饱和模型重算。这与第 5 章的“假设—验证”是同一个动作。</p></div>"""),
      ("8.2", "四种基本组态", """<table><thead><tr><th>组态</th><th>闭环增益</th><th>输入电阻</th><th>典型用途</th></tr></thead><tbody>
<tr><td>电压跟随器</td><td>1</td><td>极高</td><td>缓冲、隔离前后级</td></tr>
<tr><td>同相放大</td><td>1 + R2/R3</td><td>极高</td><td>传感器信号放大</td></tr>
<tr><td>反相放大</td><td>−Rf/Rin</td><td>≈ Rin</td><td>求和、跨阻、反相</td></tr>
<tr><td>差分 / 仪表放大</td><td>R2/R1（匹配时）</td><td>由输入电阻决定</td><td>桥式传感器、抑制共模</td></tr>
</tbody></table>
<p>下方实验中 R2 = 1k、R3 = 9k，同相增益 = 1 + 9/1 = 10。注意闭环增益<strong>只由电阻比决定</strong>，与开环增益无关——这正是负反馈用“增益换稳定与线性”的核心思想，第 13 章会展开。</p>"""),
      ("8.3", "用 E 源自建一个运放", """<p>与其调用厂商模型，不如亲手搭一次，把“理想运放”看透。网表里 <code>E1 int 0 in minus 1e5</code> 是一个<strong>压控电压源</strong>：输出 = 1e5 × (v(in) − v(minus))，就是开环增益 1e5。再串一个 R = 1k、C = 1 µF 的低通，得到约 159 Hz 的主极点，于是增益带宽积 ≈ 1e5 × 159 Hz ≈ 16 MHz。</p>
<p>这个自建模型自带“真实感”：增益有限、带宽有限、会相位滞后，却没有任何黑盒。后续第 13、14、17、20 章的反馈与稳定性实验都用它。</p>"""),
      ("8.4", "理想模型的四个边界", """<ol><li><strong>输出摆幅</strong>：不能超出电源轨；轨到轨运放也只是接近。</li>
<li><strong>压摆率 SR</strong>：大信号时输出电压变化速率有上限，正弦波会出现三角化失真。</li>
<li><strong>带宽与相位裕度</strong>：闭环增益越高，可用带宽越窄；反馈过深会振荡。</li>
<li><strong>非理想输入</strong>：输入失调电压 Vos、输入偏置电流 Ib、共模抑制比 CMRR、噪声，决定了直流精度下限。</li></ol>
<p>看到数据手册时，按这四类去查参数，就不会被几十页指标淹没。</p>"""),
  ],
  sims=[sim("sim/08-noninverting.cir", "实验 8-1：用 VCVS 搭同相放大器",
            """* Ch08 Non-inverting amplifier from a self-built opamp model
* E1 = open-loop gain 1e5 ; R1/C1 = dominant pole near 159 Hz
VIN in 0 DC 0 AC 1 SINE(0 0.5 1k)
E1 int 0 in minus 1e5
R1 int oa 1k
C1 oa 0 1u
R2 oa minus 1k
R3 minus 0 9k
.op
.tran 0 5m 0 5u
.ac dec 20 1 10Meg
.meas AC gain1k FIND mag(V(oa)) AT 1k
.end""",
            "Run → Add Trace → V(oa) 与 V(in)；.ac 结果里看闭环增益约 20 dB 的平坦段与高频滚降。",
            "闭环增益 1 + 9k/1k = 10（20 dB）；V(in)=0.5 V 峰值时 V(oa)=5 V（模型无电源轨限制）；带宽约 GBW/10 ≈ 1.6 MHz。"),
       sim("sim/08-openloop.cir", "实验 8-2：开环增益与虚短的边界",
           """* Ch08 Open-loop opamp: virtual short does NOT hold
VIN in 0 DC 0 AC 1
E1 int 0 in 0 1e5
R1 int oa 1k
C1 oa 0 1u
.op
.ac dec 20 1 10Meg
.meas AC aol_1k FIND mag(V(oa)) AT 1k
.end""",
            "Run → Add Trace → V(oa)；与实验 8-1 的闭环曲线对比。",
            "低频开环增益 1e5（100 dB），约 159 Hz 后以 −20 dB/dec 下降；开环时输出极易饱和，虚短不成立。")],
  pitfalls=["对比较器使用虚短：开环、饱和状态下不成立。", "忘记检查输出是否超出电源轨，算出“正确”却不可能实现的电压。",
            "反馈电阻取到 MΩ 级却忽略输入偏置电流与噪声。", "把 .ac 的 1 V 激励当成实际信号幅度：小信号分析只关心比值。"],
  exercises=["把 R3 改成 99k，预测闭环增益与带宽，再用 .ac 验证 GBW 近似守恒。",
             "在实验 8-1 中把 VIN 幅度提到 5 V，观察自建模型为何仍不失真，并说明真实运放会怎样。",
             "把 C1 增大 10 倍，解释相位裕度与阶跃响应振铃的趋势。"],
  further=["<a href='../../part2/13-feedback-stability/index.html'>第 13 章 反馈与稳定性</a>",
           "<a href='../../part2/14-opamp-design/index.html'>第 14 章 运算放大器设计</a>",
           "<a href='../../part3/20-design-circuit/index.html'>第 20 章 如何从规格设计电路</a>"]),

]

# ============================ 第二篇 ============================
CHAPTERS += [

C("09", P2, "part2/09-single-stage", "单级放大器",
  "把一只晶体管变成一个有增益、有阻抗、有摆幅边界的模块：三种组态其实是同一模型的三种接法。",
  hours="3 学时",
  goals=["能推导共源/共漏/共栅的增益与输入输出阻抗", "能设计并校核静态工作点与输出摆幅",
         "理解源极退化如何用线性度换增益", "会用 .op 检查所有管子是否在饱和区"],
  points=["增益与 gm·R", "输入/输出阻抗", "偏置点与摆幅", "源极退化", "有源负载", ".op 查工作点"],
  sections=[("9.1", "核心概念速览", """<ul>
<li><strong>共源 / 共射</strong>：电压增益最大（<code>−g<sub>m</sub>·R<sub>D</sub></code>），输出反相，输入阻抗高、输出阻抗由负载决定。</li>
<li><strong>共漏 / 共集（跟随器）</strong>：增益 ≈ 1，但输入阻抗高、输出阻抗低（≈ 1/g<sub>m</sub>），专职做<strong>阻抗变换</strong>。</li>
<li><strong>共栅 / 共基</strong>：输入阻抗低（≈ 1/g<sub>m</sub>）、带宽好，常作 cascode 的上管或电流缓冲。</li>
<li><strong>源极 / 发射极退化</strong>：加一个电阻引入局部负反馈，增益变成约 <code>−R<sub>D</sub>/(R<sub>S</sub>+1/g<sub>m</sub>)</code>，对器件参数不敏感、线性度变好。</li>
<li>设计顺序恒为：定偏置电流 → 定过驱动电压 → 算 W/L 或电阻 → <strong>校核摆幅与饱和区</strong>。</li></ul>
<div class="card stub"><span class="card-label">待补写</span><p style="margin-bottom:0">后续将展开：三种组态的完整推导、有源负载共源级、大信号摆幅边界、以及一组“给定增益和功耗反推尺寸”的例题。当前可先按下方实验体会源极退化。</p></div>""")],
  sims=[sim("sim/09-source-degeneration.cir", "实验 9-1：源极退化如何把增益交给电阻比",
            """* Ch09 Source degeneration: gain set by resistor ratio
.model NM1 NMOS(Vto=0.5 Kp=200u Lambda=0.02)
VDD vdd 0 DC 5
VIN in 0 DC 2.0 AC 0.05 SINE(2.0 0.05 1k)
RD vdd out 2k
M1 out in src 0 NM1 W=10u L=1u
RS src 0 500
.op
.ac dec 20 100 10Meg
.tran 0 5m 0 2u
.end""",
            "Run → Error Log 读 Id 与 V(src)；Add Trace 比较 V(in) 与 V(out) 幅度。",
            "静态 Id ≈ 1 mA（Vsrc = 0.5 V，VGS = 1.5 V）；gm ≈ 2 mS，1/gm = 500 Ω；增益 ≈ −2k/(500+500) = −2，比无退化时的 −3.85 更稳定、更线性。")],
  pitfalls=["只算增益不校核 VDS，管子掉进线性区公式全失效。", "把跟随器“增益为 1”理解成没用：它的价值是隔离。",
            "忽略 RD 上的直流压降，输出静态点过高或过低导致摆幅不对称。"],
  exercises=["把 RS 依次改为 0 / 250 / 1k，记录增益与失真趋势。", "给 RD 并联一个电流源负载，预测增益提高多少。"],
  further=["<a href='../../part1/06-mosfet/index.html'>第 6 章 MOSFET 与两级模型</a>",
           "<a href='../../part3/20-design-circuit/index.html'>第 20 章 如何从规格设计电路</a>"]),

C("10", P2, "part2/10-current-mirror", "电流源、电流镜与基准",
  "模拟电路里的“常量”从哪来：先复制一路电流，再想办法让它不随电源、温度和工艺变化。",
  hours="3 学时",
  goals=["能说明基本电流镜的复制条件与误差来源", "会计算输出阻抗与合规电压范围",
         "理解 cascode 电流镜为何能提高输出阻抗", "知道带隙基准的 PTAT/CTAT 组合思想与启动电路的作用"],
  points=["基本电流镜", "沟道长度调制误差", "cascode 提高输出阻抗", "PTAT / CTAT", "带隙基准", "启动电路"],
  sections=[("10.1", "核心概念速览", """<ul>
<li><strong>电流镜成立的条件</strong>：两管 V<sub>GS</sub> 相同、工艺相同 → I<sub>D</sub> 按 W/L 成比例复制；误差主要来自沟道长度调制（λ）与阈值失配。</li>
<li><strong>合规电压（compliance）</strong>：输出管必须保持饱和，V<sub>out</sub> ≥ V<sub>ov</sub>；低于这个值，镜像电流开始塌陷。</li>
<li><strong>cascode</strong>：叠一层管子屏蔽输出电压变化，输出阻抗从 r<sub>o</sub> 提升到约 g<sub>m</sub>r<sub>o</sub>²，代价是损失摆幅。</li>
<li><strong>带隙基准</strong>：把随温度<em>上升</em>的 PTAT（ΔV<sub>BE</sub>）与随温度<em>下降</em>的 CTAT（V<sub>BE</sub>）按系数相加，得到约 1.2 V 的零温度系数电压。</li>
<li><strong>启动电路</strong>：基准存在“零电流”这个合法但无用的平衡点，必须加一条只在启动时导通的支路把它推离。</li></ul>""")],
  sims=[sim("sim/10-current-mirror.cir", "实验 10-1：基本电流镜与合规电压",
            """* Ch10 Basic NMOS current mirror: output compliance
.model NM1 NMOS(Vto=0.5 Kp=200u Lambda=0.02)
VDD vdd 0 DC 5
IREF vdd ref 100u
M1 ref ref 0 0 NM1 W=10u L=1u
M2 out ref 0 0 NM1 W=10u L=1u
VOUT out 0 DC 2
.op
.dc VOUT 0 5 0.05
.end""",
            "Run → Add Trace → I(VOUT)（或 -I(VOUT)），横坐标是 V(out)。",
            "Vref ≈ Vto + Vov ≈ 0.5 + 0.316 = 0.816 V；当 V(out) 大于约 0.32 V 后 M2 进入饱和，电流接近 100 µA；曲线缓慢上翘的斜率正是 λ 造成的误差。")],
  pitfalls=["以为电流镜在任何输出电压下都成立：合规电压是硬约束。", "忽略 M1 二极管连接支路的压降预算。",
            "设计基准时忘记启动电路，仿真可能停在零电流解。"],
  exercises=["把 M2 的 W 改成 20u，验证输出电流是否翻倍。", "把 Lambda 改成 0，比较输出曲线的平坦度。"],
  further=["<a href='../11-diff-amp/index.html'>第 11 章 差分放大器</a>",
           "<a href='../../part3/19-read-circuit/index.html'>第 19 章 如何读懂一个陌生电路（含基准解剖）</a>"]),

C("11", P2, "part2/11-diff-amp", "差分放大器",
  "几乎所有运放的输入级。学会把任意输入拆成差模 + 共模，再用半电路法把它化简成单管问题。",
  hours="3 学时",
  goals=["能把任意双端输入分解为差模与共模", "会用半电路法求差模增益与共模增益",
         "能定义并计算 CMRR", "知道输入共模范围与失调的来源"],
  points=["差模 / 共模", "半电路等效", "共模抑制比", "电流镜负载", "失调与共模范围", ".dc 传输曲线"],
  sections=[("11.1", "核心概念速览", """<ul>
<li>任意两路输入可写成 <code>v<sub>id</sub> = v<sub>1</sub> − v<sub>2</sub></code>（要放大的）与 <code>v<sub>ic</sub> = (v<sub>1</sub>+v<sub>2</sub>)/2</code>（要抑制的）。</li>
<li><strong>半电路法</strong>：差模激励下对称面是交流地，电路对折成半个单管共源级；共模激励下对称面开路，尾电流源的有限阻抗决定了共模增益。</li>
<li><code>CMRR = |A<sub>d</sub>/A<sub>c</sub>|</code>，主要由尾电流源输出阻抗与器件失配决定；提高尾电流源 r<sub>o</sub> 是首要手段。</li>
<li>用<strong>电流镜作有源负载</strong>可把双端输出合并成单端，同时把差模增益翻倍——这正是第 19 章案例的结构。</li>
<li>输入共模范围：下限由尾电流管饱和决定，上限由输入管/负载管饱和决定，是数据手册必查参数。</li></ul>""")],
  sims=[sim("sim/11-diff-pair.cir", "实验 11-1：差分传输曲线与线性范围",
            """* Ch11 NMOS differential pair transfer curve
.model NM1 NMOS(Vto=0.5 Kp=200u Lambda=0.02)
VDD vdd 0 DC 5
ISS tail 0 200u
M1 o1 inp tail 0 NM1 W=10u L=1u
M2 o2 inn tail 0 NM1 W=10u L=1u
R1 vdd o1 10k
R2 vdd o2 10k
VINN inn 0 DC 2
VINP inp 0 DC 2
.dc VINP 1.5 2.5 0.01
.end""",
            "Run → Add Trace → 表达式 V(o1)-V(o2)；观察 S 形传输曲线。",
            "VINP = 2 V 时两支路各 100 µA，差分输出为 0；输入差增大到约 ±√2·Vov 时电流几乎全部流向一侧，曲线饱和——这段饱和区正是比较器与限幅放大器的工作依据。")],
  pitfalls=["把共模增益当成 0：尾电流源阻抗有限，共模增益不为零。", "忽略器件失配：实际 CMRR 常被失配而非理论增益限制。",
            "输入共模电压超出范围，仿真却“还能放大”（模型未体现全部边界）。"],
  exercises=["把 ISS 改成 400 µA，观察线性输入范围如何变化。", "给 R1 加 5% 失配，重新计算输出失调。"],
  further=["<a href='../10-current-mirror/index.html'>第 10 章 电流源、电流镜与基准</a>",
           "<a href='../../part3/19-read-circuit/index.html'>第 19 章 五管 OTA 解剖案例</a>"]),

C("12", P2, "part2/12-frequency-response", "频率响应与极点",
  "每个寄生电容都是一个低通。学会找出“哪一个电容说了算”，就抓住了带宽。",
  hours="3 学时",
  goals=["能从传递函数写出零极点与波特图", "会应用密勒等效估算输入电容",
         "理解主极点近似与增益带宽积", "知道右半平面零点的危害"],
  points=["极零点与波特图", "密勒等效", "主极点近似", "GBW", "右半平面零点", ".ac 扫频"],
  sections=[("12.1", "核心概念速览", """<ul>
<li>一阶低通 <code>H(s) = A<sub>0</sub>/(1+s/ω<sub>p</sub>)</code>：低于 ω<sub>p</sub> 增益平坦，高于后 −20 dB/dec、相位滞后最多 90°。</li>
<li><strong>密勒效应</strong>：跨接在增益为 −A 的反相级输入输出之间的电容 C，等效到输入端变成 <code>C(1+A)</code>，到输出端约 C。一个小小的 C<sub>gd</sub> 因此可以主导整个带宽。</li>
<li><strong>主极点近似</strong>：若第一个极点远低于其余极点，可只保留它；此时 <code>GBW ≈ A<sub>0</sub>·f<sub>p1</sub></code>，闭环增益越低、带宽越宽。</li>
<li><strong>右半平面零点</strong>（如共源级的 C<sub>gd</sub> 前馈通路）：幅度上升而相位继续滞后，恶化相位裕度，密勒补偿必须配合调零电阻。</li>
<li>节点电阻越大、电容越大，该节点极点越低；<strong>找主极点＝找“高阻 × 大电容”的那个节点</strong>。</li></ul>""")],
  sims=[sim("sim/12-miller-effect.cir", "实验 12-1：Cgd 变化如何移动主极点",
            """* Ch12 Miller effect: Cgd moves the dominant pole
.model NM1 NMOS(Vto=0.5 Kp=200u Lambda=0.02)
.param CGD=1p
VDD vdd 0 DC 5
VIN in 0 DC 1.5 AC 0.01 SINE(1.5 0.01 1k)
RD vdd out 2k
M1 out in 0 0 NM1 W=10u L=1u
CGD1 out in {CGD}
CL out 0 5p
.step param CGD list 0.1p 1p 5p
.ac dec 30 1k 100Meg
.end""",
            "Run → Add Trace → V(out)，比较 3 条曲线的 -3 dB 频率。",
            "增益约 −3.85（≈ 11.7 dB），Cgd 经密勒等效放大约 (1+3.85) 倍后并入输入电容；CGD 从 0.1p 增到 5p，带宽明显下降。")],
  pitfalls=["只按电容绝对值判断主极点，忽略它所在节点的阻抗与增益。", "把 .ac 的相位显示误读为“延时”。",
            "在瞬态仿真里用方波测带宽，却没考虑压摆率限制。"],
  exercises=["把 RD 改成 4k，预测带宽变化并说明两个相反的作用。", "在 CGD1 上串一个电阻，观察零点位置变化。"],
  further=["<a href='../../part1/04-passive-dynamics/index.html'>第 4 章 暂态与频域基础</a>",
           "<a href='../13-feedback-stability/index.html'>第 13 章 反馈与稳定性</a>"]),

C("13", P2, "part2/13-feedback-stability", "反馈与稳定性",
  "负反馈用增益换线性、带宽与可控性；但反馈太深或相位滞后太多，负反馈会变成正反馈。",
  hours="4 学时",
  goals=["能识别四种反馈拓扑并写出闭环增益", "理解环路增益与相位裕度的判据",
         "会用主极点/密勒补偿改善稳定性", "能从阶跃响应判断振铃与相位裕度"],
  points=["四种反馈拓扑", "环路增益与返回比", "增益/相位裕度", "主极点补偿", "密勒补偿", "稳定性判据"],
  sections=[("13.1", "核心概念速览", """<ul>
<li>四种拓扑按“采样输出的是电压还是电流、输入端是串联还是并联混合”分类：电压串联（同相放大）、电压并联（反相放大）、电流串联、电流并联。</li>
<li>闭环 <code>A<sub>cl</sub> = A/(1+Aβ)</code>；当 <code>Aβ ≫ 1</code> 时 <code>A<sub>cl</sub> ≈ 1/β</code>，与开环增益无关——这就是“用增益换稳定”。</li>
<li><strong>稳定性判据</strong>：在环路增益 |Aβ| = 1 的频率处，相位滞后必须小于 180°；差值就是<strong>相位裕度</strong>，工程上一般留 45°～60°。</li>
<li>两级放大器有两个低频极点，容易裕度不足；<strong>密勒补偿</strong>把主极点推低、次极点推高（极点分裂），用带宽换稳定。</li>
<li>时域征兆：阶跃响应过冲大、长时间振铃 ≈ 相位裕度不足；持续等幅振荡 ≈ 已失稳。</li></ul>""")],
  sims=[sim("sim/13-loop-stability.cir", "实验 13-1：补偿电容与阶跃振铃",
            """* Ch13 Feedback loop: ringing vs dominant-pole compensation
.param CC=100p
VIN in 0 DC 0 PULSE(0 0.1 0 1u 1u 1m 2m)
BERR err 0 V=V(in)-V(out)/10
E1 a 0 err 0 10
R1 a b 10k
C1 b 0 1n
E2 c 0 b 0 10
R2 c out 10k
C2 out 0 {CC}
.step param CC list 10p 100p 1n
.tran 0 2m 0 200n
.end""",
            "Run → Add Trace → V(out)，比较三条阶跃响应的过冲与振铃。",
            "CC 增大把第二级极点推低，两个极点靠得更近，相位裕度下降，过冲与振铃加剧；把 BERR 中的反馈系数从 1/10 改成 1/100，环路增益变大，也会更接近失稳。")],
  pitfalls=["只看直流闭环增益正确就认为电路稳定。", "把“负反馈”当成永远负：高频相移会让它变号。",
            "补偿电容越大越好：它同时牺牲带宽与压摆率。"],
  exercises=["把 CC 设为 1n 并把反馈系数改成 1/100，观察是否出现持续振荡。",
             "在 C2 上串一个小电阻引入零点，观察振铃是否改善。"],
  further=["<a href='../12-frequency-response/index.html'>第 12 章 频率响应与极点</a>",
           "<a href='../14-opamp-design/index.html'>第 14 章 运算放大器设计</a>",
           "<a href='../../part3/20-design-circuit/index.html'>第 20 章 如何从规格设计电路</a>"]),

C("14", P2, "part2/14-opamp-design", "运算放大器设计",
  "把前面所有模块拼起来：从指标分配开始，落到每一只管子的尺寸与补偿电容。",
  hours="5 学时",
  goals=["能把运放规格分解成各子模块的子指标", "会做两级 CMOS 运放的直流与频率设计",
         "理解摆率、功耗、噪声、失调之间的取舍", "能用一张检查表收尾设计"],
  points=["两级结构", "指标分解与分配", "补偿电容", "摆率与功耗", "失调与 PSRR", "设计检查表"],
  sections=[("14.1", "核心概念速览", """<ul>
<li>经典两级结构：<strong>差分输入级</strong>（提供高增益与 CMRR）+ <strong>共源第二级</strong>（提供摆幅）+ <strong>密勒补偿</strong>（保证稳定）。</li>
<li>规格分解顺序：增益 → 每级 gm·ro；带宽/相位裕度 → 补偿电容 Cc；摆率 SR = I<sub>tail</sub>/Cc → 反推尾电流；功耗 → 检查电流预算；噪声/失调 → 反推输入管尺寸。</li>
<li><code>C<sub>c</sub> ≈ g<sub>m1</sub>/(2π·GBW)</code> 量级；次极点应高于约 2～3 倍 GBW 才有足够相位裕度。</li>
<li>输入管取<strong>大 W·L、小过驱动</strong>有利于降低失调与 1/f 噪声；负载管取<strong>大 L</strong> 提高 r<sub>o</sub>。这就是模拟版图里面积与性能的交换。</li>
<li>设计检查表：所有管子饱和？共模范围？摆幅？SR？相位裕度？PSRR/CMRR？功耗？PVT 角？</li></ul>
<div class="card stub"><span class="card-label">待补写</span><p style="margin-bottom:0">后续将把下方行为级模型逐步替换为晶体管级电路，并给出一份完整的指标→尺寸手算例题。当前先用行为级模型理解“两级 + 密勒补偿”的骨架。</p></div>""")],
  sims=[sim("sim/14-two-stage.cir", "实验 14-1：两级运放行为模型与密勒补偿",
            """* Ch14 Two-stage opamp (behavioural) as unity-gain buffer
.param CM=2p
VIN inp 0 DC 0 AC 1 PULSE(0 0.1 0 1u 1u 100u 200u)
BERR err 0 V=V(inp)-V(out)
E1 a 0 err 0 1e3
R1 a n1 100k
C1 n1 0 1p
E2 b 0 n1 0 100
R2 b out 10k
C2 out 0 1p
CM1 n1 out {CM}
.step param CM list 0.2p 2p 20p
.tran 0 200u 0 20n
.ac dec 20 1k 100Meg
.end""",
            "Run → 瞬态看单位增益阶跃响应（3 条曲线），.ac 看开环形状的差别。",
            "CM 越大，主极点越低、极点分裂越明显，阶跃响应越平稳但越慢；这正是“带宽换相位裕度”的直观演示。")],
  pitfalls=["只优化增益与带宽，忘了摆率与静态功耗是同一个电流预算。", "用理想模型得出“完美”结果，没有做 PVT 与失配检查。",
            "补偿电容取值只看公式，不看次极点位置。"],
  exercises=["把 CM 固定为 2p，改变第二级增益 E2，观察相位裕度趋势。", "列出把该行为模型替换成晶体管级时需要补全的 6 个参数。"],
  further=["<a href='../11-diff-amp/index.html'>第 11 章 差分放大器</a>",
           "<a href='../13-feedback-stability/index.html'>第 13 章 反馈与稳定性</a>",
           "<a href='../../part3/22-robustness/index.html'>第 22 章 鲁棒性：PVT 与蒙特卡洛</a>"]),

C("15", P2, "part2/15-active-filters", "有源滤波器",
  "不用电感也能做二阶选频：让运放与 RC 网络共同实现一个指定的传递函数。",
  hours="3 学时",
  goals=["能写出二阶低通的标准形式并解释 Q", "会设计 Sallen-Key 低通",
         "知道 Butterworth / Bessel / Chebyshev 的选择依据", "理解运放带宽对滤波器实际响应的限制"],
  points=["低通/高通/带通", "Q 值与极点", "Sallen-Key", "多反馈拓扑", "运放带宽限制", ".ac 验证"],
  sections=[("15.1", "核心概念速览", """<ul>
<li>二阶低通标准式 <code>H(s) = H<sub>0</sub>ω<sub>0</sub>²/(s² + (ω<sub>0</sub>/Q)s + ω<sub>0</sub>²)</code>；Q 决定谐振峰与过渡带陡峭程度。</li>
<li>Butterworth（Q = 0.707）通带最平坦；Bessel 相位线性、阶跃过冲小；Chebyshev 过渡带最陡但通带有纹波。</li>
<li><strong>Sallen-Key</strong>：正反馈型、元件少、对运放带宽敏感；<strong>多反馈（MFB）</strong>：反相型、高频特性更好。</li>
<li>fc 附近运放开环增益必须远大于噪声增益，否则实际 Q 与 fc 都会偏移——这是“仿真用理想运放、实测不对”的常见原因。</li></ul>""")],
  sims=[sim("sim/15-sallen-key.cir", "实验 15-1：Sallen-Key 二阶低通",
            """* Ch15 Sallen-Key 2nd-order low-pass (unity-gain follower)
VIN in 0 DC 0 AC 1
R1 in n1 1.6k
R2 n1 n2 1.6k
C2 n2 0 100n
C1 n1 out 100n
E1 oa 0 n2 out 1e5
Ro oa out 100
.ac dec 30 10 100k
.meas AC g10 FIND mag(V(out)) AT 10
.meas AC g1k FIND mag(V(out)) AT 1k
.meas AC g10k FIND mag(V(out)) AT 10k
.end""",
            "Run → Add Trace → V(out)，切 dB 看 −40 dB/dec 的高频斜率。",
            "fc = 1/(2π·1.6k·100n) ≈ 995 Hz；单位增益 Sallen-Key 在 R、C 相等时 Q = 0.5（无峰），10 kHz 处约 −40 dB。")],
  pitfalls=["把一阶 RC 的 −20 dB/dec 套到二阶电路上。", "忽略运放带宽，实际 fc 与仿真不符。",
            "电容取太小，运放输入电容与 PCB 寄生成为误差主项。"],
  exercises=["把 C1 改成 200n，预测 Q 与峰值变化。", "把 E1 的增益降到 100，观察 fc 附近的偏差。"],
  further=["<a href='../../part1/04-passive-dynamics/index.html'>第 4 章 暂态与频域</a>",
           "<a href='../../part1/08-opamp-basics/index.html'>第 8 章 理想运放与负反馈</a>"]),

C("16", P2, "part2/16-comparator-oscillator", "比较器、施密特触发与振荡器",
  "正反馈、非线性与自激：从“输出只有高低两态”到“没有输入也能持续振荡”。",
  hours="3 学时",
  goals=["能说明比较器与运放闭环使用的区别", "会推导施密特触发器的上下阈值与迟滞宽度",
         "能陈述巴克豪森判据并解释环形振荡器起振条件", "会用 .tran 观察起振过程"],
  points=["开环比较器", "迟滞与噪声容限", "巴克豪森判据", "环形振荡器", "RC / LC 振荡", ".tran 看起振"],
  sections=[("16.1", "核心概念速览", """<ul>
<li><strong>比较器</strong>：开环使用、输出饱和、追求速度与低失调；<strong>运放</strong>：闭环使用、追求线性与稳定，二者不能随便互换。</li>
<li><strong>施密特触发</strong>：把输出经分压正反馈到输入，产生两个不同的翻转阈值；迟滞宽度即噪声容限，可消除慢边沿引起的多次翻转。</li>
<li><strong>巴克豪森判据</strong>：环路相移 360°（含反相的 180°）且环路增益 ≥ 1 时，微小扰动被放大成等幅振荡；稳态幅度由非线性限幅决定。</li>
<li>三级反相环每级约 60° 相移时总相移达 180°，加上反相本身 180°，满足振荡条件；起振需要一个初始扰动（仿真里用 <code>.ic</code> 或噪声）。</li></ul>""")],
  sims=[sim("sim/16-ring-oscillator.cir", "实验 16-1：三级环形振荡器起振",
            """* Ch16 Three-stage ring oscillator with RC delays
B1 y1 0 V=5*tanh(-20*V(z3))
R1 y1 z1 10k
C1 z1 0 10n
B2 y2 0 V=5*tanh(-20*V(z1))
R2 y2 z2 10k
C2 z2 0 10n
B3 y3 0 V=5*tanh(-20*V(z2))
R3 y3 z3 10k
C3 z3 0 10n
.ic V(z1)=0.1
.tran 0 5m 0 1u
.options plotwinsize=0
.end""",
            "Run → Add Trace → V(z1)、V(z2)、V(z3)，观察三级相位差与起振过程。",
            "每级 RC 约 100 µs，三级总环路满足振荡条件；约数个时间常数后幅度稳定在 ±5 V 附近，三级波形相差约 120°。删掉 .ic 行可能停在零解不动。")],
  pitfalls=["用 .ac 分析振荡器：小信号线性化看不到限幅后的稳态幅度。", "仿真中电路停在平衡点不起振，其实只缺一个初始扰动。",
            "把比较器当运放用，忽略了输出饱和与恢复时间。"],
  exercises=["把 C1～C3 加倍，测量周期变化并解释。", "把反相级改成 5 级，预测频率与相位关系。"],
  further=["<a href='../../part1/08-opamp-basics/index.html'>第 8 章 虚短的适用边界</a>",
           "<a href='../13-feedback-stability/index.html'>第 13 章 反馈与稳定性（正/负反馈对照）</a>"]),

C("17", P2, "part2/17-power-supply", "电源与功率电路",
  "从交流到稳定直流，再到驱动负载：纹波、环路、压降与热，是这一章反复出现的四个词。",
  hours="4 学时",
  goals=["能估算整流滤波后的纹波与电容取值", "理解线性稳压器/LDO 的环路与静态/瞬态调整率",
         "知道 Buck 变换器的基本能量传递关系", "能说明 A/B/D 类功放的效率与失真取舍"],
  points=["整流与纹波", "串联稳压 / LDO", "环路与负载瞬态", "Buck 基础", "A/B/D 类功放", "功耗与热阻"],
  sections=[("17.1", "核心概念速览", """<ul>
<li>整流 + 电容滤波：<code>ΔV ≈ I<sub>load</sub>/(f·C)</code>；二极管只在峰值附近导通，故导通角小、电流尖峰大。</li>
<li><strong>LDO</strong> = 基准 + 误差放大器 + 调整管 + 反馈分压；环路增益决定负载调整率，输出电容与 ESR 决定瞬态响应与稳定性。</li>
<li><strong>Buck</strong>：开关导通时电感储能、关断时经二极管/同步管续流；<code>V<sub>out</sub> ≈ D·V<sub>in</sub></code>，效率远高于线性稳压。</li>
<li>功放：A 类线性最好效率最低（理论 25%～50%），B/AB 类有交越失真，D 类用 PWM + LC 滤波换取高效率。</li>
<li>热：结温 = 环境温度 + 功耗 × 热阻；<strong>任何电源设计都必须算一次功耗</strong>。</li></ul>""")],
  sims=[sim("sim/17-ldo-load-step.cir", "实验 17-1：LDO 的负载阶跃与调整率",
            """* Ch17 Behavioural LDO: load-step transient and load regulation
VREF ref 0 DC 2.5
BERR err 0 V=V(ref)-V(fb)
E1 eout 0 err 0 100
RO eout out 0.5
R1 out fb 10k
R2 fb 0 10k
COUT out 0 10u
ILOAD out 0 PULSE(0 20m 0 1u 1u 2m 4m)
.tran 0 8m 0 2u
.meas TRAN v_light FIND V(out) AT 1m
.meas TRAN v_heavy FIND V(out) AT 3m
.end""",
            "Run → Add Trace → V(out) 与 I(ILOAD)；Error Log 读轻/重载两点电压。",
            "目标 5 V（2.5 V 基准 × 2），有限环路增益 100 带来约 2% 静态误差，实测约 4.90 V；20 mA 负载阶跃经 0.5 Ω 输出电阻再拉低约 10 mV，随后被环路拉回。")],
  pitfalls=["只看稳态输出电压，不看负载阶跃的下冲与恢复时间。", "LDO 输出电容 ESR 不在稳定性范围内（部分老结构反而需要一定 ESR）。",
            "忽略调整管功耗：压差 × 电流就是热。"],
  exercises=["把 E1 增益改成 1000，比较静态误差与瞬态恢复。", "把 COUT 增大 10 倍，观察下冲幅度与恢复时间的变化。"],
  further=["<a href='../../part1/05-diode/index.html'>第 5 章 二极管与整流</a>",
           "<a href='../13-feedback-stability/index.html'>第 13 章 反馈与稳定性</a>"]),

C("18", P2, "part2/18-noise-distortion", "噪声、失真与误差预算",
  "当信号小到一定程度，“对不对”变成“能分辨吗”；当信号大到一定程度，又变成“失真多少”。",
  hours="3 学时",
  goals=["能列出三类主要噪声源并写出热噪声密度", "会用 .noise 与 .four 得到噪声与 THD",
         "理解等效输入噪声与噪声带宽", "能把各项误差列成预算表并找出主项"],
  points=["热噪声 / 散粒 / 1/f", "等效输入噪声", ".noise 分析", "THD 与 .four", "PSRR / CMRR", "误差预算表"],
  sections=[("18.1", "核心概念速览", """<ul>
<li>电阻热噪声 <code>v<sub>n</sub> = √(4kTR·B)</code>；MOS/BJT 有沟道/散粒噪声；低频还有 1/f 噪声（与工艺、面积强相关）。</li>
<li>把各级噪声折算到输入端（<strong>等效输入噪声</strong>）才能统一比较；前级增益越高，后级噪声越不重要。</li>
<li><code>.noise</code> 给噪声密度与积分总噪声；<code>.four</code> 给指定基波的谐波分量与 THD。做频谱分析要关掉波形压缩（<code>.options plotwinsize=0</code>）。</li>
<li><strong>误差预算表</strong>：把失调、噪声、增益误差、温漂、电源抑制、非线性逐项列出，标注“相关/独立”与 RMS 合成方式，找出最大的一两项去优化——这比盲目换运放有效得多。</li></ul>""")],
  sims=[sim("sim/18-noise.cir", "实验 18-1：噪声分析",
            """* Ch18 Noise analysis of an RC + gain stage
VIN in 0 DC 0 AC 1
R1 in n1 1k
C1 n1 0 100n
E1 out 0 n1 0 10
.noise V(out) VIN dec 20 10 1Meg
.end""",
            "Run → Add Trace → V(onoise)（输出噪声密度）与 V(inoise)（等效输入噪声）。",
            "1 kΩ 电阻在室温下约 4 nV/√Hz；经 10 倍增益后输出噪声密度约 40 nV/√Hz，并在 RC 截止频率后随信号一起滚降。"),
       sim("sim/18-thd.cir", "实验 18-2：削顶失真的频谱与 THD",
           """* Ch18 THD of a hard-clipped sine via .four
VIN in 0 SINE(0 1 1k)
B1 out 0 V=max(-0.8,min(0.8,V(in)))
.tran 0 20m 0 2u
.four 1k V(out)
.options plotwinsize=0
.end""",
            "Run → Add Trace → V(out) 看削顶波形；View → SPICE Error Log 读 Fourier 分析结果与 THD。",
            "对称削顶只产生奇次谐波（3f、5f…）；THD 随削顶深度上升。也可在波形窗口右键 → View → FFT 交互查看。")],
  pitfalls=["用理想源做噪声分析，得到 0 噪声却以为电路无噪声。", "波形压缩开启时做 FFT，频谱出现不应有的杂散。",
            "把各项误差直接相加：独立随机误差应按均方根合成。"],
  exercises=["把实验 18-1 的 R1 增大 100 倍，验证噪声密度按 √R 增长。", "把削顶电平从 0.8 V 改到 0.5 V，比较 THD。"],
  further=["<a href='../../part3/22-robustness/index.html'>第 22 章 鲁棒性与误差预算</a>",
           "<a href='../../part3/21-simulation-method/index.html'>第 21 章 仿真方法论</a>"]),
]

# ============================ 第三篇 ============================
CHAPTERS += [

C("19", P3, "part3/19-read-circuit", "如何读懂一个陌生电路",
  "本书的核心章之一。把“看懂”从玄学变成一套可重复执行、可检查、可用仿真验证的十步流程，并完整解剖一个真实电路。",
  status="done", hours="4 学时",
  goals=["能对任意陌生电路独立完成分块、认模块、找通路、找反馈环",
         "能画出直流通路与交流小信号通路两套等效图", "能用数量级估算快速判断电路是否合理",
         "会用 .op 反查自己对工作区的假设", "能写出一份可交付的电路阅读笔记"],
  points=["先找电源与地", "模块识别词汇表", "直流 / 交流两条通路", "反馈环的正负判断",
          "标注法与节点命名", "数量级估算", "用 .op 反查假设", "完整案例解剖"],
  svg="""<svg viewBox="0 0 470 220" width="470" role="img" aria-label="五管 OTA 的模块分块示意">
  <rect class="part" x="20" y="40" width="100" height="50" rx="5"/>
  <text class="lbl" x="34" y="70">偏置 / 电流镜</text>
  <rect class="part" x="140" y="40" width="120" height="50" rx="5"/>
  <text class="lbl" x="154" y="70">差分输入对</text>
  <rect class="part" x="280" y="40" width="120" height="50" rx="5"/>
  <text class="lbl" x="294" y="70">有源负载镜像</text>
  <rect class="part" x="280" y="130" width="120" height="50" rx="5"/>
  <text class="lbl" x="300" y="160">单端输出</text>
  <g class="wire"><path d="M120 65 H140 M260 65 H280 M340 90 V130 M400 180 H400 V190 H220 V105 H200 V90"/></g>
  <path class="arrow" d="M400 180 l-6 -8 l12 0 z"/>
  <text class="lbl-s" x="228" y="200">负反馈：输出回到另一输入端</text>
  <text class="lbl-s" x="20" y="115">① 找电源/地</text>
  <text class="lbl-s" x="140" y="115">② 认模块</text>
  <text class="lbl-s" x="280" y="115">③ 找信号通路</text>
</svg>""",
  sections=[
      ("19.1", "为什么“看懂”这么难", """<p>一张模拟电路图上，至少叠了四层信息，而它们共用同一批线条：</p>
<ol><li><strong>直流供电与偏置</strong>：谁给谁提供电流，静态工作点在哪；</li>
<li><strong>信号通路</strong>：输入从哪进来、经过几级增益、从哪出去；</li>
<li><strong>反馈环路</strong>：哪条线把输出又送回输入，是正还是负；</li>
<li><strong>辅助与保护</strong>：启动电路、补偿电容、去耦、限流、ESD、关断控制。</li></ol>
<p>新手常犯的错是“顺着线从头看到尾”，结果在电源线和反馈线之间迷路。<strong>正确做法是按层分块，一次只看一层</strong>。下面十步就是固定的分层顺序。</p>"""),
      ("19.2", "十步拆解法", """<table><thead><tr><th>步</th><th>动作</th><th>要写下的产物</th></tr></thead><tbody>
<tr><td>1</td><td>圈出所有电源、地、参考电位，标出电源范围</td><td>电源树：VDD / VSS / VREF 各接到哪些模块</td></tr>
<tr><td>2</td><td>找输入端与输出端（最左/最右、接插件名、芯片引脚名）</td><td>信号流方向的粗箭头</td></tr>
<tr><td>3</td><td>按“功能块”切图：偏置、输入级、增益级、输出级、反馈网络、保护</td><td>方框草图，每块一句话说明功能</td></tr>
<tr><td>4</td><td>画<strong>直流通路</strong>：电容开路、电感短路、交流源置零</td><td>直流等效图 + 各节点电位数量级</td></tr>
<tr><td>5</td><td>画<strong>交流小信号通路</strong>：电源接交流地、大电容短路、器件换小信号模型</td><td>小信号等效图 + 增益表达式</td></tr>
<tr><td>6</td><td>找所有<strong>环路</strong>，逐个判正负（沿环走一圈数反相次数）</td><td>环路清单：主负反馈 / 局部反馈 / 正反馈 / 启动环</td></tr>
<tr><td>7</td><td>识别辅助支路：启动、补偿、去耦、限流、保护、修调</td><td>每个“看不懂的元件”给出存在理由</td></tr>
<tr><td>8</td><td>做数量级估算：电流、gm、增益、带宽、摆幅</td><td>一张手算表（不追求精确，只求量级对）</td></tr>
<tr><td>9</td><td>用 <code>.op</code> 反查假设：每个管子的工作区、Id、gm、Vov</td><td>假设 vs 实测对照，标出矛盾处</td></tr>
<tr><td>10</td><td>用 <code>.tran</code> / <code>.ac</code> 回答“它到底做什么"</td><td>功能结论一句话 + 关键波形</td></tr>
</tbody></table>
<div class="card tip"><span class="card-label">可打印检查单</span><p style="margin-bottom:0">电源地 → 输入输出 → 分块 → 直流图 → 交流图 → 环路正负 → 辅助支路 → 数量级 → .op 反查 → 波形结论。做完十步仍读不懂，通常不是能力问题，而是<strong>缺前置知识</strong>：回到第一、二篇查对应模块。</p></div>"""),
      ("19.3", "模块识别词汇表", """<table><thead><tr><th>图形特征</th><th>多半是</th><th>为什么存在</th></tr></thead><tbody>
<tr><td>栅漏短接的 MOS / 集电极基极短接的 BJT</td><td>二极管连接器件，电流镜的“基准支路"</td><td>产生一个可被复制的 VGS / VBE</td></tr>
<tr><td>两个管子栅极相连、源极共接</td><td>电流镜 或 差分对</td><td>看源极是接地（镜像）还是接尾电流源（差分）</td></tr>
<tr><td>两个输入管源极共接、下面挂一个电流源</td><td>差分输入级</td><td>放大差模、抑制共模</td></tr>
<tr><td>PMOS 栅极相连、源极接 VDD，作差分对负载</td><td>电流镜有源负载</td><td>双端转单端，增益翻倍</td></tr>
<tr><td>跨接在两级之间的一只小电容</td><td>密勒补偿电容</td><td>极点分裂、保证相位裕度</td></tr>
<tr><td>电源到地之间一串二极管/电阻，且只在启动时导通</td><td>启动电路</td><td>把基准推出零电流平衡点</td></tr>
<tr><td>一只管子叠在另一只管子上、栅极接固定偏置</td><td>cascode</td><td>提高输出阻抗 / 屏蔽电压变化</td></tr>
<tr><td>输出经电阻分压回到输入</td><td>负反馈网络</td><td>用增益换稳定与线性</td></tr>
<tr><td>电源脚附近的小电容</td><td>去耦 / 旁路</td><td>提供瞬态电流、稳住电源</td></tr>
</tbody></table>
<p>这份词汇表与<a href="../../index.html#toc">第二篇的章节目录</a>一一对应：认出模块，就知道去哪一章查公式。</p>"""),
      ("19.4", "标注法：把图“重写”一遍", """<p>不要在原图上冥思苦想，动手重画一遍，并用三种标记分层：</p>
<ul><li>给每个节点<strong>起名字</strong>（<code>bias</code>、<code>tail</code>、<code>dn</code>、<code>dp</code>），名字本身带上功能信息；</li>
<li>用一种颜色/线型画<strong>直流电流路径</strong>（VDD → 负载 → 管子 → 尾电流源 → VSS），另一种画<strong>信号路径</strong>（输入 → 差分对 → 增益级 → 输出）；</li>
<li>把<strong>反馈环</strong>单独画成箭头闭环，并在旁边写“负（1 次反相）”或“正”。</li></ul>
<p>本书所有网表都用功能化节点名，就是为了和这个习惯对齐。读别人的 <code>.asc</code> 原理图时，第一步也应是把 <code>N001</code> 之类改成有意义的标签。</p>"""),
      ("19.5", "数量级估算：先粗后细", """<p>在打开仿真器之前，先做 60 秒估算，能挡掉绝大部分理解错误：</p>
<ul><li>电源 5 V、电阻 kΩ 级 ⇒ 电流约 mA 级；电流镜 µA 级 ⇒ 电阻一般 MΩ 或管子很小。</li>
<li>MOS 过驱动 V<sub>ov</sub> 常取 0.1～0.3 V；<code>g<sub>m</sub> = 2I<sub>D</sub>/V<sub>ov</sub></code> ⇒ 100 µA 对应约 1 mS。</li>
<li>单级增益 <code>g<sub>m</sub>·R<sub>out</sub></code> 常在 5～50；两级 100～10000；主极点常在 kΩ × pF = ns～µs 量级。</li>
<li>摆幅预算：电源电压减去各管所需的最小 V<sub>DS</sub>，通常每只管子留 0.2～0.3 V。</li></ul>
<p>估出来的数如果和仿真差 10 倍以上，几乎一定是<strong>工作区假设错了</strong>，而不是模型不准。</p>"""),
      ("19.6", "用 .op 反查假设", """<p><code>.op</code> 的输出里，对每个 MOS 会列出 <code>Id</code>、<code>Vgs</code>、<code>Vds</code>、<code>Vth</code>、<code>Vov</code>、<code>gm</code>、<code>ro</code> 与工作区。检查顺序：</p>
<ol><li><code>Vov &gt; 0</code> 且 <code>Vds ≥ Vov</code> ⇒ 饱和（放大区）。若不满足，直流假设要重来。</li>
<li>各支路电流是否满足 KCL？尾电流是否等于两支路之和？镜像比例对不对？</li>
<li>静态输出电压是否落在预期摆幅中间？给正负信号各留了多少余量？</li>
<li><code>gm</code> 是否与 <code>2Id/Vov</code> 一致？不一致说明模型比你用的公式复杂（这是好事，记下来）。</li></ol>"""),
      ("19.7", "完整案例：五管 OTA 单位增益跟随器", """<p>下方实验 19-1 是一个“看起来陌生”的电路：2 个电源、1 路偏置、4 只镜子/差分管、1 只输出管，还把输出接回了输入。按十步法走一遍：</p>
<ol>
<li><strong>电源/地</strong>：VDD = +2.5 V、VSS = −2.5 V，地是信号参考，不是电源中点。</li>
<li><strong>输入输出</strong>：VIN 接 <code>inp</code>；输出取 <code>dp</code>；<code>VFB</code>（0 V 源）把 <code>dp</code> 短接到 <code>inn</code>，因此是<strong>单位增益反馈</strong>。</li>
<li><strong>分块</strong>：<code>IB + MB</code> 是偏置基准；<code>MT</code> 是尾电流镜（W 翻倍 ⇒ 100 µA）；<code>M1/M2</code> 是差分对；<code>M3/M4</code> 是 PMOS 电流镜负载；输出在 <code>dp</code>。</li>
<li><strong>直流通路</strong>：IB(50 µA) → MB → VSS；MT 复制出 100 µA 尾电流；差分对平衡时各 50 µA；M3 二极管连接产生约 1.68 V 的栅压，M4 复制 50 µA。</li>
<li><strong>交流通路</strong>：VDD/VSS 是交流地；差分对把 <code>v(inp)−v(inn)</code> 变成漏极电流差，电流镜把两路差合并到 <code>dp</code>，等效跨导约 g<sub>m</sub>；输出阻抗 = r<sub>o2</sub>∥r<sub>o4</sub>。</li>
<li><strong>环路</strong>：<code>dp</code> → <code>inn</code> 只有一条。沿环走：输入升高 → M1 电流增 → <code>dn</code> 降 → M4 电流增 → <code>dp</code> 升 → <code>inn</code> 升 → M2 电流增，<strong>抵消原变化</strong>，故为负反馈。</li>
<li><strong>辅助支路</strong>：<code>VFB</code> 是 0 V 源，用于把两根线连起来并顺便测电流，不是放大器；本例未画补偿电容（单级、高输出阻抗，实际集成电路需要）。</li>
<li><strong>估算</strong>：每支路 50 µA，V<sub>ov</sub> ≈ 0.16 V，g<sub>m</sub> ≈ 0.6 mS，r<sub>o</sub> ≈ 1/(0.02×50µ) = 1 MΩ ⇒ 开环增益约 g<sub>m</sub>(r<sub>o</sub>/2) ≈ 300。闭环增益 ≈ 1。</li>
<li><strong>.op 反查</strong>：检查 M1～M4 是否都在饱和区、<code>dp</code> 是否接近 0 V、IB/MT 电流比是否 1:2。</li>
<li><strong>结论</strong>：这是一个<strong>五管 OTA 构成的电压跟随器</strong>，用高开环增益换取精确的单位增益缓冲。</li>
</ol>
<div class="card note"><p style="margin-bottom:0">把 <code>VIN</code> 的 DC 改成 0.5 V，输出也会跟到约 0.5 V——这就是“读懂了”之后能做出的预测。能预测，才算真懂。</p></div>"""),
  ],
  sims=[sim("sim/19-ota-follower.cir", "实验 19-1：待解剖的五管 OTA（先别看结论，自己走十步）",
            """* Ch19 Case study: five-transistor OTA wired as a voltage follower
.model NM1 NMOS(Vto=0.5 Kp=200u Lambda=0.02)
.model PM1 PMOS(Vto=-0.5 Kp=100u Lambda=0.02)
VDD vdd 0 DC 2.5
VSS vss 0 DC -2.5
IB vdd bias 50u
MB bias bias vss vss NM1 W=10u L=2u
MT tail bias vss vss NM1 W=20u L=2u
M1 dn inp tail vss NM1 W=40u L=2u
M2 dp inn tail vss NM1 W=40u L=2u
M3 dn dn vdd vdd PM1 W=20u L=2u
M4 dp dn vdd vdd PM1 W=20u L=2u
VFB dp inn DC 0
VIN inp 0 DC 0 AC 0.1 SINE(0 0.1 1k)
.op
.tran 0 5m 0 2u
.end""",
            "Run → View → SPICE Error Log 逐管核对工作区与电流；Add Trace → V(dp) 与 V(inp)。",
            "MT 尾电流约 100 µA，差分对每支路 50 µA，M3/M4 镜像 50 µA；V(dp) 跟随 V(inp)，闭环增益约 1。若看到某管 Vds 小于 Vov，说明共模范围被突破。")],
  pitfalls=["顺着线从头看到尾，没有先分层分块。", "把反馈线当成信号线，或漏掉局部反馈环。",
            "看到不认识的元件就跳过：启动、补偿、去耦往往正是理解设计意图的钥匙。",
            "直接跑仿真看波形，跳过手算与 .op，得到“看起来合理”却解释不通的结论。"],
  exercises=["把 VIN 的 DC 改成 0.5 V，先预测 V(dp)，再仿真核对。",
             "删掉 VFB（把 dp 与 inn 断开并给 inn 接固定 2 V），说明电路变成什么、输出会怎样。",
             "把 MT 的 W 改成 40u，预测尾电流、gm 与开环增益的变化。",
             "找一张数据手册里的框图（如运放、LDO），用十步法写一份不超过一页的阅读笔记。"],
  further=["<a href='../../index.html#toc'>第二篇全部模块章节（词汇表来源）</a>",
           "<a href='../20-design-circuit/index.html'>第 20 章 如何从规格设计电路</a>",
           "<a href='https://github.com/JesseHardingMurillo/LTspice_Ecircuit' target='_blank' rel='noopener'>GitHub：LTspice_Ecircuit（37 类现成电路，练读图用）</a>",
           "<a href='https://github.com/Khannister/Electronic-simulations-with-LTspice' target='_blank' rel='noopener'>GitHub：Electronic-simulations-with-LTspice（.asc 读图素材）</a>"]),

C("20", P3, "part3/20-design-circuit", "如何从规格设计电路",
  "本书的另一个核心章。把“我要一个放大器”变成一份可验收的规格、一棵指标分解树、一组手算参数和一个自动化的仿真验收脚本。",
  status="done", hours="4 学时",
  goals=["能把模糊需求转成可测量的规格条目", "会做指标分解与拓扑选型",
         "能用闭环流程手算定出元件参数", "会用 .step + .meas 写自动化验收脚本", "能写出一份设计文档"],
  points=["规格澄清与边界条件", "指标分解树", "拓扑选型矩阵", "手算定参数",
          ".step 参数寻优", ".meas 自动验收", "设计文档模板"],
  sections=[
      ("20.1", "规格先于拓扑", """<p>新手最先问“用哪个电路”，工程师最先问“要满足什么”。一份可验收的规格至少包含：</p>
<table><thead><tr><th>类别</th><th>要写清的条目</th><th>例子</th></tr></thead><tbody>
<tr><td>信号</td><td>源阻抗、幅度范围、频率范围、共模电平</td><td>10 kΩ 源，±0.5 V，10 Hz～100 kHz</td></tr>
<tr><td>增益 / 精度</td><td>标称增益、误差、线性度、失调</td><td>−10 V/V，误差 ≤ 2%</td></tr>
<tr><td>频域</td><td>带宽、相位裕度、噪声、滤波要求</td><td>−3 dB ≥ 200 kHz</td></tr>
<tr><td>负载 / 电源</td><td>负载阻抗、可用电源、功耗上限</td><td>10 kΩ ∥ 10 pF，±5 V，≤ 20 mW</td></tr>
<tr><td>环境</td><td>温度范围、器件公差、批量一致性</td><td>0～70 ℃，电阻 1%</td></tr>
<tr><td>验收</td><td>怎么测、测哪几个点、判据</td><td>1 kHz 增益、100 kHz 增益、阶跃过冲</td></tr>
</tbody></table>
<p><strong>没有验收方法的规格等于没有规格</strong>。写规格时就要想好后面 <code>.meas</code> 测什么。</p>"""),
      ("20.2", "指标分解树与选型矩阵", """<p>把总指标拆到每个模块头上，让每个模块只承担一两项要求：</p>
<pre class="spice" data-file="inline"><code>总指标: |Av|=10, BW>=200kHz, 误差<=2%, Rin>=10k
  ├─ 输入级/电阻网络: Rin, 噪声增益, 电阻比精度
  ├─ 放大核心: 开环增益 A0, GBW, 相位裕度
  └─ 输出级: 摆幅, 负载驱动, 功耗</code></pre>
<p class="code-hint">上面是分解示意（非网表）。</p>
<table><thead><tr><th>需求</th><th>候选拓扑</th><th>选择理由</th></tr></thead><tbody>
<tr><td>高输入阻抗、同相</td><td>同相运放 / 仪表放大</td><td>输入不取电流</td></tr>
<tr><td>增益由电阻比精确决定、可求和</td><td>反相运放</td><td>虚地使增益 ≈ −Rf/Rin</td></tr>
<tr><td>单电源、微弱差分信号</td><td>仪表放大器 / 差分 ADC 驱动</td><td>共模抑制与电平搬移</td></tr>
<tr><td>极低功耗、单片集成</td><td>OTA / 两级 CMOS 运放</td><td>可自主分配电流与补偿</td></tr>
</tbody></table>
<p>选型的本质是<strong>取舍</strong>：增益、带宽、噪声、功耗、面积、成本不可能同时最优。把选与不选的理由写下来，比选型结果本身更重要。</p>"""),
      ("20.3", "手算定参数：一个完整案例", """<p><strong>规格</strong>：反相放大器，增益 −10 V/V，带宽 ≥ 200 kHz，输入电阻 ≥ 10 kΩ，信号 ±0.5 V，电源 ±5 V（行为级模型）。</p>
<ol>
<li><strong>定电阻</strong>：Rin = 10 kΩ ⇒ Rf = 100 kΩ。噪声增益 <code>NG = 1 + Rf/Rin = 11</code>。</li>
<li><strong>定运放带宽</strong>：闭环带宽 ≈ GBW/NG，故 GBW ≥ 200 k × 11 = 2.2 MHz。自建模型的 <code>A0 = 1e5</code>、主极点 159 Hz ⇒ GBW ≈ 15.9 MHz，裕量充足。</li>
<li><strong>校核精度</strong>：有限开环增益带来的相对误差 ≈ NG/A0 = 11/1e5 = 0.011%，远小于 2%；主要误差来自电阻公差，用 0.1% 电阻即可。</li>
<li><strong>校核摆幅</strong>：输出峰值 = 10 × 0.5 = 5 V，正好贴住电源轨 ⇒ <strong>规格冲突</strong>，必须把电源提高到 ±7 V 或把增益需求下调。这一步正是手算的价值：仿真会给你一条“看起来没问题”的波形，而规格审查提前发现了问题。</li>
<li><strong>定验收点</strong>：1 kHz 增益、100 kHz 增益、1 MHz 增益、阶跃过冲；写成 .meas 断言。</li>
</ol>"""),
      ("20.4", "把验收写成自动化脚本", """<p>实验 20-1 用 <code>.step param RFv</code> 一次跑三组候选值，用 <code>.meas AC ... FIND mag(V(oa)) AT 频率</code> 把验收结果写成数字。这就是模拟电路里的<strong>回归测试</strong>：以后每次改参数，跑一次脚本，看数字是否仍在规格内。</p>
<div class="card tip"><p style="margin-bottom:0">把这一步接到 <a href='https://github.com/nunobrum/PyLTSpice' target='_blank' rel='noopener'>PyLTSpice</a> 上，可以用 Python 循环上百组参数、读取 <code>.log</code> 里的 <code>.meas</code> 结果、自动画趋势图。对计算机专业学生，这是最容易发挥既有优势的地方。</p></div>"""),
      ("20.5", "公差、裕量与文档", """<ul><li><strong>公差</strong>：电阻 1%、电容 10%、Vos、温漂；按第 22 章方法做蒙特卡洛。</li>
<li><strong>裕量</strong>：环路增益留 10 倍、相位裕度留 45°～60°、摆幅留 10%～20%、功耗留 20%。没有裕量的设计只在典型条件下成立。</li>
<li><strong>设计文档模板</strong>：规格表 → 分解树 → 选型与理由 → 手算过程 → 原理图/网表 → 仿真验收表（目标/实测/通过）→ 公差与最坏情况 → 遗留风险 → 实测计划。</li></ul>"""),
  ],
  sims=[sim("sim/20-design-verification.cir", "实验 20-1：候选参数扫描 + 自动验收",
            """* Ch20 Design verification: inverting amplifier, target gain -10
.param RFv=100k
VIN in 0 DC 0 AC 1
RG in minus 10k
RF oa minus {RFv}
E1 int 0 0 minus 1e5
R1 int oa 1k
C1 oa 0 1u
.step param RFv list 50k 100k 150k
.ac dec 20 10 10Meg
.meas AC gain1k FIND mag(V(oa)) AT 1k
.meas AC gain100k FIND mag(V(oa)) AT 100k
.meas AC gain1meg FIND mag(V(oa)) AT 1Meg
.end""",
            "Run → View → SPICE Error Log，把 3 组 × 3 个频点的结果填进验收表。",
            "RFv = 100k 时 1 kHz 增益 ≈ 10（20 dB），100 kHz 仍接近 10，1 MHz 开始滚降（GBW/NG ≈ 1.45 MHz）；RFv = 50k / 150k 分别得到约 5 / 15。只有 100k 满足规格。")],
  pitfalls=["先选电路再补规格，导致做出来不知道算不算成功。", "只验证典型条件，没做公差、温度、电源变化。",
            "规格之间互相冲突却在最后才发现（例如增益 × 输入幅度超出电源轨）。",
            "把仿真波形截图当验收证据，没有可复现的数字断言。"],
  exercises=["把规格改成增益 −5、输入 ±1 V，重新走一遍五步并修改网表。",
             "给 RG、RF 各加 1% 公差，用 .step 估计增益的最坏偏差。",
             "补一条 .meas 测量 100 kHz 处的相位，解释它为何影响稳定性。"],
  further=["<a href='../19-read-circuit/index.html'>第 19 章 如何读懂一个陌生电路</a>",
           "<a href='../21-simulation-method/index.html'>第 21 章 仿真方法论</a>",
           "<a href='../22-robustness/index.html'>第 22 章 鲁棒性：PVT 与蒙特卡洛</a>",
           "<a href='https://www.ti.com/' target='_blank' rel='noopener'>TI · Analog Engineer's Circuit Cookbook（业界选型与裕量惯例）</a>"]),

C("21", P3, "part3/21-simulation-method", "仿真方法论",
  "仿真器永远会给你一条曲线。本章解决更难的问题：这条曲线是否回答了你真正想问的问题。",
  status="done", hours="3 学时",
  goals=["能为不同问题选对分析类型", "会搭建带激励、负载、探针与隔离的测试台",
         "会用 .meas 写自动断言", "能识别仿真“看起来对其实错”的典型陷阱",
         "知道仿真与实测必然存在的差异清单"],
  points=["五类分析的选择", "测试台与激励设计", ".meas 断言", "模型可信度",
          "收敛问题排查", "仿真 ≠ 实测 清单"],
  sections=[
      ("21.1", "先问问题，再选分析", """<table><thead><tr><th>我想知道</th><th>用</th><th>别误用</th></tr></thead><tbody>
<tr><td>偏置对不对、管子在哪个区</td><td><code>.op</code></td><td>不要靠 .tran 的起始段猜</td></tr>
<tr><td>输入变化时的非线性传输关系</td><td><code>.dc</code></td><td>不要用于含电容的动态过程</td></tr>
<tr><td>增益、带宽、相位、阻抗随频率</td><td><code>.ac</code></td><td>不能看失真、饱和、压摆</td></tr>
<tr><td>波形、摆幅、失真、启动、振荡</td><td><code>.tran</code></td><td>不能用小信号线性化替代</td></tr>
<tr><td>噪声、THD、稳定性</td><td><code>.noise</code> / <code>.four</code> + 环路分析</td><td>THD 需要足够长且稳定的时间窗</td></tr>
</tbody></table>"""),
      ("21.2", "测试台：把被测电路和测量仪器分开", """<ol><li><strong>激励</strong>：小信号用 <code>AC 1</code>，瞬态用 <code>PULSE/SINE</code> 并给有限边沿；源阻抗要显式写出（理想源常被误当成零阻抗）。</li>
<li><strong>负载</strong>：把后级输入阻抗、探头电容都画进去（见第 23 章）。</li>
<li><strong>隔离</strong>：用跟随器或大电阻把“测量”与“被测”隔开，避免测试电路改变工作点。</li>
<li><strong>探针</strong>：给关键节点起名字，只保存需要的量（<code>.save</code>）可大幅缩小 .raw。</li>
<li><strong>基准</strong>：先用最简单的理想电路跑一遍，确认测试台本身没写错，再换成真实模型。</li></ol>"""),
      ("21.3", ".meas 就是断言", """<p>把“眼睛看曲线”换成“数字过阈值”：增益、−3 dB 频率、上升时间、过冲、功耗、静态误差都能写成 <code>.meas</code>，结果进 Error Log，可被脚本解析。配合 <code>.step</code> 就是参数化的回归测试。</p>
<pre class="spice" data-file="inline"><code>.meas TRAN trise TRIG V(out) VAL=0.1 RISE=1 TARG V(out) VAL=0.9 RISE=1
.meas TRAN vfinal FIND V(out) AT 4m
.meas AC gain1k FIND mag(V(out)) AT 1k</code></pre>
<p class="code-hint">语法片段（非完整网表），可直接粘进实验 21-1。</p>"""),
      ("21.4", "八个“看起来对其实错”的陷阱", """<ol>
<li><strong>用理想源</strong>：没有内阻、没有噪声、没有寄生，结果天生过于漂亮。</li>
<li><strong>忘了模型边界</strong>：Level-1 MOS 不含短沟道效应；运放宏模型可能不含压摆或输入共模限制。</li>
<li><strong>AC 分析掩盖非线性</strong>：<code>.ac</code> 把电路在工作点线性化，饱和、削顶、交越失真一律看不见。</li>
<li><strong>波形压缩</strong>：默认压缩会让 FFT 出现虚假杂散，做频谱前写 <code>.options plotwinsize=0</code>。</li>
<li><strong>时间窗太短 / 步长太大</strong>：THD、启动过程、慢极点都需要足够长的稳态窗口。</li>
<li><strong>初始条件</strong>：振荡器或双稳态电路可能停在零解，需要 <code>.ic</code> 或噪声扰动（见第 16 章）。</li>
<li><strong>收敛失败被“修好"</strong>：把容差放宽到能跑，往往是掩盖了悬浮节点或理想开关。</li>
<li><strong>单位与量纲</strong>：<code>m</code> 与 <code>Meg</code>、dB 与倍数、峰值与 RMS，每年都坑人。</li>
</ol>"""),
      ("21.5", "仿真 ≠ 实测：差异清单", """<table><thead><tr><th>仿真里没有（或过于理想）</th><th>实测中会出现</th><th>对策</th></tr></thead><tbody>
<tr><td>PCB 走线电阻/电感、过孔、寄生电容</td><td>高频增益偏差、振铃</td><td>加估计寄生参数再仿真</td></tr>
<tr><td>元件公差与温漂</td><td>批量个体差异</td><td>蒙特卡洛 / 最坏情况（第 22 章）</td></tr>
<tr><td>电源内阻、地线阻抗、去耦不足</td><td>低频振荡、串扰</td><td>显式建电源与地网络</td></tr>
<tr><td>探头负载、仪器带宽</td><td>被测点被探头改变</td><td>把探头模型放进测试台（第 23 章）</td></tr>
<tr><td>器件老化、ESD 损伤、焊接问题</td><td>无法复现的异常</td><td>分模块上电、故障树排除</td></tr>
</tbody></table>
<p>结论应当是<strong>条件式</strong>的：“在这些模型与假设下，增益为 10、带宽 1.4 MHz"，而不是无条件的“增益就是 10”。</p>"""),
      ("21.6", "实验记录模板", """<p>每次仿真写六行：目的 / 测试台（激励·负载·模型） / 手算预期 / 仿真实测 / 偏差原因 / 下一步改哪个参数。积累起来的记录，比任何一张波形截图都值钱。</p>"""),
  ],
  sims=[sim("sim/21-testbench-meas.cir", "实验 21-1：带自动测量的 RC 测试台",
            """* Ch21 Testbench: parameter sweep with .meas assertions
.param R=1k
VIN in 0 PULSE(0 1 0 1n 1n 2m 4m)
R1 in out {R}
C1 out 0 100n
.step param R list 1k 2k 5k
.tran 0 5m 0 1u
.meas TRAN trise TRIG V(out) VAL=0.1 RISE=1 TARG V(out) VAL=0.9 RISE=1
.meas TRAN vfinal FIND V(out) AT 4m
.end""",
            "Run → Error Log 读 3 组 trise / vfinal；把结果与 2.2·R·C 手算值对照。",
            "10%→90% 上升时间 = 2.2RC：R=1k/2k/5k 时约 220 µs / 440 µs / 1.1 ms；终值均为 1 V。"),
       sim("sim/21-fft-setup.cir", "实验 21-2：正确的频谱分析设置",
           """* Ch21 FFT setup: disable waveform compression
VIN in 0 SINE(0 1 1k)
R1 in out 1k
C1 out 0 100n
.tran 0 20m 0 2u
.four 1k V(out)
.options plotwinsize=0
.end""",
            "Run → Error Log 读 Fourier 结果；波形窗口右键 → View → FFT 交互查看。",
            "1 kHz 基波被 RC 低通衰减约 0.85 倍并相移；删掉 .options 行后再做 FFT，可观察到压缩对频谱底噪的影响。")],
  pitfalls=["只会用 .tran 一种分析看所有问题。", "测试台里的理想电压源直接并到电容上，导致不收敛或 unrealistic 结果。",
            "仿真结果和手算差 10 倍仍照单全收。", "把仿真结论写成无条件事实，没有标注模型与假设。"],
  exercises=["给实验 21-1 增加 .meas 测过冲，并解释为何 RC 电路没有过冲。",
             "把实验 21-2 的 .tran 时长改成 2m，比较 THD 数值的稳定性。"],
  further=["<a href='../../part0/02-spice-netlist/index.html'>第 2 章 SPICE 网表语法与仿真指令</a>",
           "<a href='../20-design-circuit/index.html'>第 20 章 如何从规格设计电路</a>",
           "<a href='../22-robustness/index.html'>第 22 章 鲁棒性：PVT 与蒙特卡洛</a>",
           "<a href='https://github.com/nunobrum/PyLTSpice' target='_blank' rel='noopener'>PyLTSpice：批量仿真与 .log 结果解析</a>"]),

C("22", P3, "part3/22-robustness", "鲁棒性：PVT、蒙特卡洛与最坏情况",
  "典型条件下成立不算设计完成。让电路在工艺、电源、温度与元件公差的全部组合下仍满足规格，才是工程。",
  hours="3 学时",
  goals=["能列出 PVT 与工艺角的组合", "会用 mc() / gauss() 与 .step 做蒙特卡洛",
         "会做灵敏度分析找出主误差项", "理解最坏情况与统计方法的差别"],
  points=["PVT 与工艺角", "mc() / gauss()", ".step 批量运行", "直方图与 σ", "最坏情况组合", "良率与规格裕量"],
  sections=[("22.1", "核心概念速览", """<ul>
<li><strong>PVT</strong>：Process（工艺角 TT/FF/SS/FS/SF）、Voltage（电源 ±10%）、Temperature（−40/25/125 ℃）；集成电路还要角 + 蒙特卡洛两套检查。</li>
<li>LTspice 内置 <code>mc(x,tol)</code>（均匀随机）、<code>gauss(x)</code>（正态随机），配合 <code>.step param run 1 N 1</code> 让每个元件独立抖动。</li>
<li><strong>最坏情况</strong>把所有参数同时取极限，保守但组合数爆炸；<strong>蒙特卡洛</strong>给分布与良率，更接近量产。</li>
<li><strong>灵敏度分析</strong>：一次只改一个参数，找出对输出影响最大的那一两项，把预算花在它们身上。</li>
<li>规格必须留裕量：典型值居中、公差带内不越界，才算通过。</li></ul>""")],
  sims=[sim("sim/22-monte-carlo.cir", "实验 22-1：分压器公差的 50 次蒙特卡洛",
            """* Ch22 Monte-Carlo of resistor tolerances
.param run=1
.param R1v=mc(10k,0.01)
.param R2v=mc(10k,0.05)
V1 in 0 DC 5
R1 in out {R1v}
R2 out 0 {R2v}
.step param run 1 50 1
.op
.meas OP vout FIND V(out)
.end""",
            "Run → Error Log 读出 50 个 vout；把数据粘进表格或 Python 画直方图。",
            "标称 2.500 V；R2 的 5% 公差主导输出离散，分布宽度约 ±0.06 V 量级。把 R2 公差改成 1% 再跑一次，对比 σ 的变化。")],
  pitfalls=["只跑一次典型仿真就下结论。", "把 mc() 的结果当成“最坏情况”：统计不等于边界。",
            "所有元件用同一个随机数，导致误差被错误地相关化。"],
  exercises=["给 V1 加 ±5% 公差，观察分布如何平移。", "设计一组最坏情况（R1 最大 / R2 最小等），与蒙特卡洛极值比较。"],
  further=["<a href='../21-simulation-method/index.html'>第 21 章 仿真方法论</a>",
           "<a href='../../part2/18-noise-distortion/index.html'>第 18 章 误差预算</a>",
           "<a href='https://github.com/nunobrum/PyLTSpice' target='_blank' rel='noopener'>PyLTSpice · Montecarlo / WorstCaseAnalysis 工具箱</a>"]),

C("23", P3, "part3/23-lab-debug", "从仿真到实物：PCB、仪器与调试",
  "仿真里没有焊点、探头和走线。这一章把“纸面正确”过渡到“上电也正确”。",
  hours="3 学时",
  goals=["能说明接地、回流路径与去耦的基本原则", "知道探头 10× 档的负载效应",
         "会按分模块上电、先直流后信号的顺序调试", "能把实测差异映射回仿真模型"],
  points=["接地与回流路径", "去耦与旁路", "探头 10× 与负载", "测量带宽与噪声", "分模块上电调试", "故障树"],
  sections=[("23.1", "核心概念速览", """<ul>
<li>电流永远走<strong>闭合回路</strong>，“地”不是无底洞；高频回流路径紧贴信号走线下方，地平面被切开会造出天线。</li>
<li>去耦电容提供瞬态电流，位置比容量更重要；容量越大往往自谐振频率越低，常见做法是大小电容并联。</li>
<li>示波器 10× 探头约 10 MΩ ∥ 10～15 pF：在 1 MHz 时容抗仅约 10 kΩ，足以改变高阻节点的频响（见下方实验）。</li>
<li>调试顺序：目视/连通性 → 上电前测短路 → 限流上电 → 只查电源电压 → 查每级静态工作点 → 注入小信号逐级跟波形。</li>
<li>实测与仿真不符时，先补寄生与仪器模型，再怀疑原理图，最后才怀疑器件损坏。</li></ul>""")],
  sims=[sim("sim/23-probe-loading.cir", "实验 23-1：探头电容如何改变被测电路",
            """* Ch23 Scope probe loading at a high-impedance node
.param Cprobe=0p
VIN in 0 DC 0 AC 1
R1 in out 100k
C1 out 0 10p
RPROBE out 0 1Meg
CPROBE out 0 {Cprobe}
.step param Cprobe list 0p 10p 100p
.ac dec 30 1k 100Meg
.end""",
            "Run → Add Trace → V(out)，比较 3 条频响曲线。",
            "无探头时 fc ≈ 1/(2π·100k·10p) ≈ 159 kHz；接入 10 pF 探头后带宽约减半，100 pF 时降到约 14 kHz——“测到的带宽“其实是探头与电路共同的结果。")],
  pitfalls=["用长接地线探头测高速信号，引入振铃。", "忽略万用表/信号源的内阻与 50 Ω 端接。",
            "一次性焊完整板上电，故障时无法定位。"],
  exercises=["把 R1 降到 1k，重跑实验 23-1，解释为何探头影响变小。", "列出一份分模块上电调试的检查表。"],
  further=["<a href='../21-simulation-method/index.html'>第 21 章 仿真 ≠ 实测 清单</a>",
           "<a href='https://www.ti.com/' target='_blank' rel='noopener'>TI 应用笔记（去耦、接地与测量）</a>"]),
]

# ============================ 第四篇 ============================
CHAPTERS += [
C("24", P4, "part4/24-projects", "综合实验与课程设计课题",
  "把全书知识串成一条信号链。三个课题都给出规格、模块划分、验收方法与可运行的测试台。",
  hours="8～12 学时",
  goals=["能把一个系统需求拆成若干模拟模块", "会为每个模块定规格并写验收断言",
         "能完成从手算、仿真到设计文档的完整流程"],
  points=["传感器信号链", "音频功率放大器", "带隙基准与 LDO", "规格与验收表", "报告模板"],
  sections=[("24.1", "三个课程设计课题", """<table><thead><tr><th>课题</th><th>规格示例</th><th>用到的章节</th><th>验收方式</th></tr></thead><tbody>
<tr><td><strong>A. 传感器信号链</strong></td><td>桥式传感器 ±10 mV，输出 0～2 V，带宽 ≤ 100 Hz，共模抑制 ≥ 60 dB</td><td>3、8、11、15、18、21、23</td><td>.ac 增益与截止频率；.tran 阶跃响应；共模注入测 CMRR</td></tr>
<tr><td><strong>B. 音频放大器</strong></td><td>8 Ω 负载 1 W，20 Hz～20 kHz，THD ≤ 1%</td><td>8、13、16、17、18</td><td>.four 测 THD；.tran 看削顶；功耗与热估算</td></tr>
<tr><td><strong>C. 基准与 LDO</strong></td><td>输出 3.3 V，负载 0～100 mA，电源抑制 ≥ 40 dB</td><td>5、10、13、17、22</td><td>.dc 扫描输入/负载；温度扫描；蒙特卡洛</td></tr>
</tbody></table>
<p>下方测试台是课题 A 的最小可运行版本：传感器等效源 → RC 抗混叠滤波 → 同相放大（增益 10）。按<a href="../../part3/20-design-circuit/index.html">第 20 章</a>的文档模板补齐规格、手算、验收表与公差分析，就是一个完整的大作业。</p>""")],
  sims=[sim("sim/24-sensor-chain.cir", "实验 24-1：传感器信号链最小系统",
            """* Ch24 Project A: sensor + anti-alias filter + gain of 10
VSENS sens 0 DC 0.1 AC 0.05 SINE(0.1 0.05 10)
RTH sens n1 1k
CF n1 0 1u
E1 int 0 n1 minus 1e5
R1 int oa 1k
C1 oa 0 1u
R2 oa minus 9k
R3 minus 0 1k
.op
.tran 0 500m 0 200u
.ac dec 20 1 100k
.meas AC gain10 FIND mag(V(oa)) AT 10
.end""",
            "Run → .tran 看 10 Hz 信号被放大；.ac 看低频增益约 20 dB、高频被 CF 与运放主极点限制。",
            "闭环增益 1 + 9k/1k = 10；CF 与 RTH 形成约 159 Hz 的低通；VSENS 的 50 mV 交流分量在输出约 0.5 V。")],
  pitfalls=["课题一开始就画完整电路，没有先分模块定规格。", "只交仿真截图，没有验收表与设计文档。",
            "忽略模块之间的阻抗与电平匹配。"],
  exercises=["把 CF 改成使 −3 dB 恰好落在 100 Hz，并写 .meas 验证。", "为课题 B 写一份规格表与验收点清单。"],
  further=["<a href='../../part3/20-design-circuit/index.html'>第 20 章 设计文档模板</a>",
           "<a href='../../part3/19-read-circuit/index.html'>第 19 章 十步读图法</a>",
           "<a href='https://github.com/TongenShen/electronics-learning' target='_blank' rel='noopener'>GitHub：electronics-learning（同类综合信号链课程）</a>"]),
]

# ============================ 附录 ============================
CHAPTERS += [
C("A", PA, "appendix", "附录 · 公式、指令与术语速查",
  "一页查表：常用公式、单位前缀、SPICE 元件与点指令、中英术语，以及本书的维护方式。",
  status="done", hours="查阅",
  goals=["能快速查到常用公式与 SPICE 语法", "知道中英术语对应关系，便于读英文资料",
         "知道如何给本书新增章节与仿真实验"],
  points=["常用公式", "SPICE 指令表", "单位前缀", "术语中英对照", "推荐教材", "如何新增章节"],
  sections=[
      ("A.1", "常用公式速查", """<table><thead><tr><th>主题</th><th>公式</th><th>出处</th></tr></thead><tbody>
<tr><td>分压 / 戴维南</td><td><code>V<sub>out</sub> = V<sub>in</sub>·R<sub>2</sub>/(R<sub>1</sub>+R<sub>2</sub>)</code>；<code>R<sub>th</sub> = R<sub>1</sub>∥R<sub>2</sub></code></td><td>第 3 章</td></tr>
<tr><td>RC 时间常数 / 截止频率</td><td><code>τ = RC</code>；<code>f<sub>c</sub> = 1/(2πRC)</code>；10%→90% 上升时间 ≈ 2.2τ</td><td>第 4、21 章</td></tr>
<tr><td>二极管</td><td><code>I = I<sub>S</sub>(e<sup>V/(nV<sub>T</sub>)</sup>−1)</code>，<code>V<sub>T</sub> ≈ 26 mV</code>，<code>r<sub>d</sub> = nV<sub>T</sub>/I<sub>D</sub></code></td><td>第 5 章</td></tr>
<tr><td>MOS 饱和区</td><td><code>I<sub>D</sub> = ½K<sub>p</sub>(W/L)V<sub>ov</sub>²(1+λV<sub>DS</sub>)</code></td><td>第 6 章</td></tr>
<tr><td>MOS 小信号</td><td><code>g<sub>m</sub> = 2I<sub>D</sub>/V<sub>ov</sub></code>；<code>r<sub>o</sub> ≈ 1/(λI<sub>D</sub>)</code>；<code>A<sub>0</sub> = g<sub>m</sub>r<sub>o</sub></code></td><td>第 6 章</td></tr>
<tr><td>BJT 小信号</td><td><code>g<sub>m</sub> = I<sub>C</sub>/V<sub>T</sub></code>；<code>r<sub>π</sub> = β/g<sub>m</sub></code></td><td>第 7 章</td></tr>
<tr><td>运放闭环</td><td>同相 <code>1+R<sub>2</sub>/R<sub>3</sub></code>；反相 <code>−R<sub>f</sub>/R<sub>in</sub></code></td><td>第 8 章</td></tr>
<tr><td>反馈 / 带宽</td><td><code>A<sub>cl</sub> = A/(1+Aβ)</code>；<code>BW<sub>cl</sub> ≈ GBW/NG</code></td><td>第 13、20 章</td></tr>
<tr><td>密勒等效</td><td>跨接反相增益 −A 两端的 C ⇒ 输入等效 <code>C(1+A)</code></td><td>第 12 章</td></tr>
<tr><td>热噪声</td><td><code>v<sub>n</sub> = √(4kTR·B)</code>；1 kΩ ≈ 4 nV/√Hz（室温）</td><td>第 18 章</td></tr>
<tr><td>整流纹波</td><td><code>ΔV ≈ I<sub>load</sub>/(f·C)</code></td><td>第 5、17 章</td></tr>
</tbody></table>"""),
      ("A.2", "单位前缀与记数法", """<table><thead><tr><th>写法</th><th>倍率</th><th>写法</th><th>倍率</th></tr></thead><tbody>
<tr><td><code>f</code></td><td>10⁻¹⁵</td><td><code>k</code></td><td>10³</td></tr>
<tr><td><code>p</code></td><td>10⁻¹²</td><td><code>Meg</code></td><td>10⁶</td></tr>
<tr><td><code>n</code></td><td>10⁻⁹</td><td><code>G</code></td><td>10⁹</td></tr>
<tr><td><code>u</code></td><td>10⁻⁶</td><td><code>T</code></td><td>10¹²</td></tr>
<tr><td><code>m</code></td><td>10⁻³</td><td><code>mil</code></td><td>25.4 µm</td></tr>
</tbody></table>
<p><strong>切记</strong>：SPICE 中 <code>m</code> = 毫，<code>Meg</code> = 兆，大小写不敏感，<code>1M</code> 仍是 1 毫。dB 换算：电压 20·log₁₀(倍数)，功率 10·log₁₀(倍数)。</p>"""),
      ("A.3", "SPICE 元件与点指令速查", """<table><thead><tr><th>类别</th><th>语法 / 指令</th><th>说明</th></tr></thead><tbody>
<tr><td>无源</td><td><code>R/C/L 名 节点+ 节点- 值</code></td><td>可加 <code>ic=</code> 初始条件</td></tr>
<tr><td>独立源</td><td><code>V/I 名 节点+ 节点- DC 值 AC 幅值 波形</code></td><td><code>SINE()</code> / <code>PULSE()</code> / <code>PWL()</code></td></tr>
<tr><td>半导体</td><td><code>D/Q/M</code></td><td>M 为 <code>D G S B 模型 W= L=</code></td></tr>
<tr><td>受控源</td><td><code>E/G/F/H</code>；行为源 <code>B ... V=表达式</code></td><td>E 可自建理想运放</td></tr>
<tr><td>分析</td><td><code>.op .dc .ac .tran .noise .tf .four</code></td><td>见第 1、21 章</td></tr>
<tr><td>扫描与测量</td><td><code>.param .step .meas .save</code></td><td>参数化回归测试</td></tr>
<tr><td>模型</td><td><code>.model .subckt .ends .include .lib</code></td><td>本书全部自包含</td></tr>
<tr><td>控制</td><td><code>.ic .options .end</code></td><td><code>.options plotwinsize=0</code> 用于 FFT</td></tr>
</tbody></table>
<p>最小可用模板（可直接复制改名）：</p>"""),
      ("A.4", "中英术语对照", """<table><thead><tr><th>中文</th><th>English</th><th>中文</th><th>English</th></tr></thead><tbody>
<tr><td>工作点 / 偏置</td><td>operating point / bias</td><td>过驱动电压</td><td>overdrive voltage</td></tr>
<tr><td>小信号</td><td>small-signal</td><td>跨导</td><td>transconductance (gm)</td></tr>
<tr><td>共模 / 差模</td><td>common-mode / differential-mode</td><td>共模抑制比</td><td>CMRR</td></tr>
<tr><td>负反馈</td><td>negative feedback</td><td>环路增益</td><td>loop gain</td></tr>
<tr><td>相位裕度</td><td>phase margin</td><td>增益带宽积</td><td>gain-bandwidth product</td></tr>
<tr><td>主极点 / 补偿</td><td>dominant pole / compensation</td><td>压摆率</td><td>slew rate</td></tr>
<tr><td>摆幅 / 合规电压</td><td>swing / compliance voltage</td><td>失调</td><td>offset</td></tr>
<tr><td>电源抑制比</td><td>PSRR</td><td>纹波</td><td>ripple</td></tr>
<tr><td>工艺角</td><td>process corner</td><td>蒙特卡洛</td><td>Monte Carlo</td></tr>
<tr><td>去耦 / 旁路</td><td>decoupling / bypass</td><td>网表</td><td>netlist</td></tr>
</tbody></table>"""),
      ("A.5", "推荐书目与资料索引", """<p>完整清单（含已核实的 GitHub 仓库、厂商资料与教材）见<a href="../index.html#resources">总目录的「参考资源」章节</a>。速记：</p>
<ul><li>主干教材：Sedra &amp; Smith；康华光；童诗白 / 华成英</li>
<li>工程直觉：Horowitz &amp; Hill《The Art of Electronics》</li>
<li>集成电路：Razavi；Gray &amp; Meyer；Allen &amp; Holberg</li>
<li>仿真与流程：Baker；ADI《Op Amp Applications Handbook》；PyLTSpice 文档</li></ul>"""),
      ("A.6", "维护本书", """<ol><li>补写某章正文：直接编辑对应 <code>index.html</code> 的 <code>&lt;section&gt;</code>，把状态徽章与 <code>assets/toc.js</code> 里的 <code>status</code> 一起改成 <code>done</code>。</li>
<li>加仿真实验：在页面里加 <code>&lt;pre class="spice" data-file="sim/xxx.cir"&gt;&lt;code&gt;…&lt;/code&gt;&lt;/pre&gt;</code>，运行 <code>python3 tools/extract_netlists.py</code> 生成 <code>.cir</code>。</li>
<li>加章节：在 <a href="../index.html#toc">总目录</a> 加链接与知识点标签，建文件夹与页面，再在 <code>assets/toc.js</code> 追加一条（侧栏与上下章自动更新）。</li>
<li>自检：<code>python3 tools/check_book.py</code>。</li>
<li>批量重建骨架：<code>python3 tools/build_book.py</code>（默认不覆盖已有文件，<code>--force</code> 才覆盖）。</li></ol>"""),
  ],
  sims=[sim("sim/A-template.cir", "模板 A-1：最小可用网表",
            """* Appendix: minimal netlist template
* 1 title | 2 sources | 3 components | 4 analysis | 5 end
V1 in 0 DC 5
R1 in out 1k
R2 out 0 1k
.op
.end""",
            "复制保存为任意 .cir，用 LTspice 打开并 Run。",
            "V(out) = 2.5 V。所有实验都可以在这个骨架上增删元件与分析指令。")],
  pitfalls=["把附录当正文读：它只负责查表，公式的适用条件在对应章节。"],
  exercises=["从模板 A-1 出发，改成 RC 低通并加 .ac 分析。", "把 A.1 里任一公式用 .op 或 .ac 验证一次。"],
  further=["<a href='../index.html#toc'>返回总目录</a>",
           "<a href='../index.html#resources'>参考资源清单</a>"]),
]

# ==================== 正文补写与扩展资源合并 ====================
import sys
sys.path.insert(0, str(ROOT / "tools"))
from book_expansion import EXTRA_SECTIONS  # noqa: E402
from book_resources import links_for_point, chapter_links_html, all_resources_html  # noqa: E402

for _ch in CHAPTERS:
    if _ch["id"] in EXTRA_SECTIONS:
        _ch["sections"] = _ch["sections"] + EXTRA_SECTIONS[_ch["id"]]
        _ch["status"] = "done"
    if _ch["id"] == "A":
        _ch["sections"].append(("A.7", "扩展学习链接总表", all_resources_html()))

# ============================ 渲染与生成 ============================
STATUS_LABEL = {"done": "已完稿", "skeleton": "框架待补", "todo": "待建"}

# 每页页脚共用的署名与 AI 使用声明（index.html 中也使用同一段文字）
CREDITS_HTML = (
    '<p class="credits"><strong>作者</strong>：汪亮（bertonwang）　'
    '<strong>联系邮箱</strong>：<a href="mailto:47608843@qq.com">47608843@qq.com</a></p>\n'
    '<p class="ai-note"><strong>AI 使用说明</strong>：本教材的知识框架、正文与 LTspice 示例代码'
    '在 AI 辅助下整理生成，并经人工校订与静态自检。公式、数值与仿真结论请以 LTspice 实际运行结果'
    '及权威教材为准；发现错漏欢迎通过上方邮箱勘误。</p>'
)


def esc(s):
    return html_mod.escape(s, quote=False)


def li(items):
    return "\n".join("<li>" + x + "</li>" for x in items)


def render(ch):
    folder = pathlib.PurePosixPath(ch["folder"])
    root = "../" * len(folder.parts)
    is_appendix = ch["id"] == "A"
    chapter_attr = ' data-chapter="' + ch["id"] + '"'
    if is_appendix:
        chapter_attr += ' data-page="appendix"'
    head_title = ("附录 A · " + ch["title"]) if is_appendix else ("第 " + ch["id"] + " 章 · " + ch["title"])

    out = []
    out.append("<!DOCTYPE html>")
    out.append('<html lang="zh-CN">')
    out.append("<head>")
    out.append('<meta charset="utf-8">')
    out.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    out.append("<title>" + esc(head_title) + " | " + BOOK_TITLE + "</title>")
    out.append('<link rel="stylesheet" href="' + root + 'assets/style.css">')
    out.append('<script src="' + root + 'assets/toc.js" defer></script>')
    out.append('<script src="' + root + 'assets/app.js" defer></script>')
    out.append("</head>")
    out.append('<body data-root="' + root + '"' + chapter_attr + ">")
    out.append('<aside id="sidebar"></aside>')
    out.append('<main class="book-page">')
    if is_appendix:
        out.append('<nav class="breadcrumb"><a href="' + root + 'index.html">总目录</a> / 附录</nav>')
    else:
        out.append('<nav class="breadcrumb" data-autofill>总目录</nav>')

    out.append('<header class="chapter-head">')
    out.append('<span class="kicker">' + esc(ch["part"]) + "</span>")
    if is_appendix:
        out.append("<h1><span class=\"ch-num\">附录 A</span>" + esc(ch["title"]) + "</h1>")
    else:
        out.append('<h1><span class="ch-num">第 ' + ch["id"] + " 章</span>" + esc(ch["title"]) + "</h1>")
    out.append('<p class="lede">' + esc(ch["lede"]) + "</p>")
    out.append('<div class="meta">')
    out.append('<span class="badge ' + ch["status"] + '">' + STATUS_LABEL[ch["status"]] + "</span>")
    out.append("<span>建议 " + esc(ch["hours"]) + "</span>")
    out.append("<span>" + str(len(ch["sims"])) + " 个 LTspice 实验</span>")
    out.append("<span>" + BOOK_TITLE + "</span>")
    out.append("</div></header>")

    if ch["goals"]:
        out.append('<div class="card objectives"><span class="card-label">学习目标</span><ul>')
        out.append(li([esc(g) for g in ch["goals"]]))
        out.append("</ul></div>")

    if ch["status"] == "skeleton":
        out.append('<div class="card stub"><span class="card-label">本章状态</span>'
                   '<p style="margin-bottom:0">知识框架、知识点细目、学习目标与可运行的 LTspice 实验已经就位，'
                   '正文正在逐节补写。你可以直接按下方实验做“先手算 → 再仿真 → 改参数”的练习，'
                   '并按 <a href="' + root + 'index.html#contribute">总目录的维护约定</a>补充内容。</p></div>')

    out.append('<section id="map"><h2><span class="sec-num">§</span>知识点地图</h2>')
    out.append('<p class="code-hint">每个知识点都配了 1～2 个扩展学习链接，可直接点开精读；'
               '本章的完整资源清单见 <a href="#extra-links">扩展学习</a>。</p>')
    out.append('<table><thead><tr><th style="width:44px">#</th><th style="width:24%">知识点</th>'
               '<th>扩展学习</th><th style="width:100px">状态</th></tr></thead><tbody>')
    for i, p in enumerate(ch["points"], 1):
        state = "正文已覆盖" if ch["status"] == "done" else "待展开为小节"
        out.append("<tr><td>" + str(i) + "</td><td>" + esc(p) + "</td><td>" +
                   links_for_point(ch["id"], p) + "</td><td>" + state + "</td></tr>")
    out.append("</tbody></table></section>")

    for num, title, body in ch["sections"]:
        sid = "s" + num.replace(".", "-")
        out.append('<section id="' + sid + '"><h2><span class="sec-num">§' + num + "</span>" + esc(title) + "</h2>")
        out.append(body)
        out.append("</section>")

    out.append('<section id="lab"><h2><span class="sec-num">§</span>仿真实验</h2>')
    if ch["svg"]:
        out.append('<figure class="circuit">' + ch["svg"] +
                   '<figcaption>电路示意图（内联 SVG，随 HTML 一起阅读、可缩放、可打印）</figcaption></figure>')
    for i, s in enumerate(ch["sims"], 1):
        out.append("<h3>" + esc(s["title"]) + "</h3>")
        out.append('<pre class="spice" data-file="' + s["file"] + '"><code>' + esc(s["code"]) + "</code></pre>")
        out.append('<p class="code-hint"><strong>操作：</strong>' + esc(s["steps"]) +
                   "　<strong>预期与判读：</strong>" + esc(s["expect"]) +
                   "　文件位置：<code>" + esc(ch["folder"] + "/" + s["file"]) + "</code></p>")
    out.append('<div class="card note"><p style="margin-bottom:0">代码块右上角可一键复制；'
               '本仓库 <code>sim/*.cir</code> 由 <code>tools/extract_netlists.py</code> 从这些代码块自动抽取，'
               '因此页面与可运行网表永远一致。网表注释统一使用 ASCII 英文。</p></div>')
    out.append("</section>")

    if ch["pitfalls"]:
        out.append('<section id="pitfalls"><h2><span class="sec-num">§</span>常见误区</h2>'
                   '<div class="card warn"><ul>' + li([esc(x) for x in ch["pitfalls"]]) + "</ul></div></section>")
    if ch["exercises"]:
        out.append('<section id="exercises"><h2><span class="sec-num">§</span>习题与思考</h2><ol>' +
                   li([esc(x) for x in ch["exercises"]]) + "</ol></section>")
    out.append('<section id="extra-links"><h2><span class="sec-num">§</span>扩展学习</h2>')
    out.append(chapter_links_html(ch["id"], root))
    out.append("</section>")
    if ch["further"]:
        out.append('<section id="further"><h2><span class="sec-num">§</span>延伸阅读与内链</h2><ul>' +
                   li(ch["further"]) + "</ul></section>")

    out.append('<footer class="pager" data-autofill></footer>')
    out.append('<footer class="site-foot">')
    out.append(CREDITS_HTML)
    out.append('<p class="imprint">' + BOOK_TITLE +
               ' · 每章一个文件夹：index.html 讲知识，sim/*.cir 供 LTspice 直接运行'
               ' · LTspice 为 Analog Devices 的免费仿真工具，本书与之无从属关系。</p>')
    out.append('</footer>')
    out.append("</main>")
    out.append("</body>")
    out.append("</html>")
    return "\n".join(out) + "\n"


def build(force=False):
    created, skipped = [], []
    for ch in CHAPTERS:
        target = ROOT / ch["folder"] / "index.html"
        if target.exists() and not force:
            skipped.append(str(target.relative_to(ROOT)))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(ch), encoding="utf-8")
        created.append(str(target.relative_to(ROOT)))
    return created, skipped


def main():
    ap = argparse.ArgumentParser(description="生成教材章节页")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的章节页（会丢失手工修改）")
    ap.add_argument("--list", action="store_true", help="只列出章节清单")
    args = ap.parse_args()

    if args.list:
        for ch in CHAPTERS:
            print(ch["id"].rjust(2), STATUS_LABEL[ch["status"]].ljust(6), ch["folder"].ljust(42), ch["title"])
        return

    created, skipped = build(force=args.force)
    for p in created:
        print("生成", p)
    print("共 %d 章：新建 %d，跳过 %d（已存在，使用 --force 可重建）" % (len(CHAPTERS), len(created), len(skipped)))


if __name__ == "__main__":
    main()
