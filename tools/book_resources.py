#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全书扩展学习链接库（唯一数据源）。

链接分两类：
  1) 上一轮已逐一核实可访问的 GitHub 仓库、厂商与教育站点；
  2) 标准英文百科条目（本环境网络无法访问 wikipedia.org，故每条知识点
     都同时配一个已核实资源作为备用入口）。
渲染时由 build_book.py 调用 links_for_point() / chapter_links_html()，
把链接嵌进「知识点地图」表格与每章的「扩展学习」小节。
"""
from __future__ import annotations

import html
import urllib.parse

# key -> (显示名, URL, 一句话说明, 分类)
R = {
    # ---- 已核实的 GitHub 仓库 ----
    "gh_pyltspice": ("PyLTSpice · GitHub", "https://github.com/nunobrum/PyLTSpice",
                     "用 Python 批量改网表、跑仿真、解析 .raw/.log，含蒙特卡洛工具箱", "工具 / 自动化"),
    "gh_circuitjs": ("circuitjs1 · GitHub", "https://github.com/pfalstad/circuitjs1",
                     "浏览器交互式仿真器，可直观看到电流与电位", "交互仿真"),
    "gh_mick": ("Circuits-LTSpice · GitHub", "https://github.com/mick001/Circuits-LTSpice",
                "大量 LTspice 电路案例合集，含配套说明站点", "案例 / 代码"),
    "gh_basics": ("LTspice-Basics · GitHub", "https://github.com/alfy7/LTspice-Basics",
                  "MIT 许可的 LTspice 入门练习集", "练习 / 入门"),
    "gh_ecircuit": ("LTspice_Ecircuit · GitHub", "https://github.com/JesseHardingMurillo/LTspice_Ecircuit",
                    "37 类按主题归档的电路，适合逐张练习读图", "案例 / 读图"),
    "gh_cn": ("electronics-learning · GitHub", "https://github.com/TongenShen/electronics-learning",
              "中文 LTspice 教程，强调先算、再仿真、改参数看趋势", "教程 / 中文"),
    "gh_ngspice": ("ngspice · GitHub", "https://github.com/ngspice/ngspice",
                   "开源 SPICE 引擎，可对照哪些是通用语法、哪些是 LTspice 扩展", "工具 / 引擎"),
    "gh_razavi": ("razavi_cmos_analog · GitHub", "https://github.com/gudivadaashok/razavi_cmos_analog",
                  "Razavi 模拟 CMOS 教材章节笔记与问答", "笔记 / 进阶"),
    "gh_khannister": ("Electronic-simulations-with-LTspice · GitHub",
                      "https://github.com/Khannister/Electronic-simulations-with-LTspice",
                      "按主题归档的 .asc 原理图合集，练习打开别人的图先读懂", "案例 / 读图"),
    # ---- 已核实的厂商 / 教育站点 ----
    "adi_ltspice": ("ADI · LTspice 官方", "https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html",
                    "仿真器下载、官方模型库与示例电路", "厂商 / 官方"),
    "adi_ez": ("ADI EngineerZone", "https://ez.analog.com/",
               "收敛问题、模型导入与实际器件应用的厂商问答社区", "厂商 / 社区"),
    "ecircuit": ("eCircuit Center", "https://www.ecircuitcenter.com/",
                 "按 SPICE 分析类型组织的经典电路讲解，许多 GitHub 合集的源头", "教学 / 网站"),
    "aac": ("All About Circuits · Textbook", "https://www.allaboutcircuits.com/textbook/",
            "免费在线电子学教材，偏工程直觉的补充阅读", "教材 / 开放"),
    "mit_ocw": ("MIT OpenCourseWare", "https://ocw.mit.edu/",
                "电路与电子学公开课的讲义、习题与实验安排", "课程 / 开放"),
    "ti": ("TI · 应用笔记与电路手册", "https://www.ti.com/",
           "Analog Engineer's Circuit Cookbook 等，看业界如何选拓扑、留裕量", "厂商 / 手册"),
    "pyltspice_docs": ("PyLTSpice 文档", "https://pyltspice.readthedocs.io/en/latest/",
                       "SpiceEditor / SimRunner / RawRead 的官方用法", "工具 / 文档"),
    "falstad": ("CircuitJS 在线版（Falstad）", "https://www.falstad.com/circuit/",
                "无需安装即可搭电路看电流动画，建立直觉", "交互仿真 / 在线"),
    "circuitjs_dev": ("CircuitJS 开发版", "https://pfalstad.github.io/circuitjs1/circuitjs.html",
                      "circuitjs1 仓库提供的在线构建版本", "交互仿真 / 在线"),
    "gh_topics_analog": ("GitHub · analog-electronics 主题", "https://github.com/topics/analog-electronics",
                         "按主题发现更多开源模拟电路项目", "检索 / 开源"),
    "gh_topics_ltspice": ("GitHub · ltspice 主题", "https://github.com/topics/ltspice",
                          "按主题发现更多 LTspice 例程", "检索 / 开源"),
    # ---- 标准英文百科条目（知识点级精读） ----
    "w_divider": ("Voltage divider（英）", "https://en.wikipedia.org/wiki/Voltage_divider", "分压公式与负载效应", "百科 / 基础"),
    "w_kcl": ("Kirchhoff's circuit laws（英）", "https://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws", "KCL/KVL 的严格表述", "百科 / 基础"),
    "w_nodal": ("Nodal analysis（英）", "https://en.wikipedia.org/wiki/Nodal_analysis", "节点电压法的系统步骤", "百科 / 基础"),
    "w_thevenin": ("Thévenin's theorem（英）", "https://en.wikipedia.org/wiki/Th%C3%A9venin%27s_theorem", "戴维南等效与输出电阻", "百科 / 基础"),
    "w_impedance": ("Electrical impedance（英）", "https://en.wikipedia.org/wiki/Electrical_impedance", "阻抗的复数表示", "百科 / 频域"),
    "w_rc": ("RC circuit（英）", "https://en.wikipedia.org/wiki/RC_circuit", "一阶充放电与时间常数", "百科 / 频域"),
    "w_rlc": ("RLC circuit（英）", "https://en.wikipedia.org/wiki/RLC_circuit", "二阶系统、谐振与阻尼", "百科 / 频域"),
    "w_bode": ("Bode plot（英）", "https://en.wikipedia.org/wiki/Bode_plot", "幅频/相频图的画法", "百科 / 频域"),
    "w_q": ("Q factor（英）", "https://en.wikipedia.org/wiki/Q_factor", "品质因数的定义与含义", "百科 / 频域"),
    "w_transfer": ("Transfer function（英）", "https://en.wikipedia.org/wiki/Transfer_function", "传递函数与零极点", "百科 / 频域"),
    "w_diode": ("Diode（英）", "https://en.wikipedia.org/wiki/Diode", "PN 结与二极管模型", "百科 / 器件"),
    "w_rectifier": ("Rectifier（英）", "https://en.wikipedia.org/wiki/Rectifier", "半波/全波整流拓扑", "百科 / 器件"),
    "w_zener": ("Zener diode（英）", "https://en.wikipedia.org/wiki/Zener_diode", "反向击穿与稳压", "百科 / 器件"),
    "w_mosfet": ("MOSFET（英）", "https://en.wikipedia.org/wiki/MOSFET", "结构、工作区与模型", "百科 / 器件"),
    "w_gm": ("Transconductance（英）", "https://en.wikipedia.org/wiki/Transconductance", "跨导定义与公式", "百科 / 器件"),
    "w_cs": ("Common source（英）", "https://en.wikipedia.org/wiki/Common_source", "共源级增益与阻抗", "百科 / 放大"),
    "w_bjt": ("Bipolar junction transistor（英）", "https://en.wikipedia.org/wiki/Bipolar_junction_transistor", "BJT 工作区与电流关系", "百科 / 器件"),
    "w_ce": ("Common emitter（英）", "https://en.wikipedia.org/wiki/Common_emitter", "共射放大器分析", "百科 / 放大"),
    "w_opamp": ("Operational amplifier（英）", "https://en.wikipedia.org/wiki/Operational_amplifier", "理想模型与非理想参数", "百科 / 运放"),
    "w_feedback": ("Negative feedback（英）", "https://en.wikipedia.org/wiki/Negative_feedback", "反馈的一般理论", "百科 / 反馈"),
    "w_comparator": ("Comparator（英）", "https://en.wikipedia.org/wiki/Comparator", "比较器与运放的区别", "百科 / 非线性"),
    "w_schmitt": ("Schmitt trigger（英）", "https://en.wikipedia.org/wiki/Schmitt_trigger", "迟滞阈值推导", "百科 / 非线性"),
    "w_mirror": ("Current mirror（英）", "https://en.wikipedia.org/wiki/Current_mirror", "镜像结构与误差", "百科 / 模块"),
    "w_bandgap": ("Bandgap voltage reference（英）", "https://en.wikipedia.org/wiki/Bandgap_voltage_reference", "PTAT/CTAT 组合原理", "百科 / 模块"),
    "w_cascode": ("Cascode（英）", "https://en.wikipedia.org/wiki/Cascode", "输出阻抗提升的机理", "百科 / 模块"),
    "w_diff": ("Differential amplifier（英）", "https://en.wikipedia.org/wiki/Differential_amplifier", "差模/共模与半电路法", "百科 / 模块"),
    "w_cmrr": ("Common-mode rejection ratio（英）", "https://en.wikipedia.org/wiki/Common-mode_rejection_ratio", "CMRR 定义与测量", "百科 / 模块"),
    "w_miller": ("Miller effect（英）", "https://en.wikipedia.org/wiki/Miller_effect", "密勒等效的推导", "百科 / 频响"),
    "w_pm": ("Phase margin（英）", "https://en.wikipedia.org/wiki/Phase_margin", "相位裕度与阶跃响应", "百科 / 稳定性"),
    "w_nyquist": ("Nyquist stability criterion（英）", "https://en.wikipedia.org/wiki/Nyquist_stability_criterion", "严格稳定性判据", "百科 / 稳定性"),
    "w_small_signal": ("Small-signal model（英）", "https://en.wikipedia.org/wiki/Small-signal_model", "线性化的数学依据", "百科 / 放大"),
    "w_slew": ("Slew rate（英）", "https://en.wikipedia.org/wiki/Slew_rate", "压摆率与大信号限制", "百科 / 运放"),
    "w_psrr": ("Power supply rejection ratio（英）", "https://en.wikipedia.org/wiki/Power_supply_rejection_ratio", "PSRR 定义与测量", "百科 / 运放"),
    "w_filter": ("Electronic filter（英）", "https://en.wikipedia.org/wiki/Electronic_filter", "滤波器分类与术语", "百科 / 滤波"),
    "w_butterworth": ("Butterworth filter（英）", "https://en.wikipedia.org/wiki/Butterworth_filter", "最平坦响应与极点位置", "百科 / 滤波"),
    "w_ring": ("Ring oscillator（英）", "https://en.wikipedia.org/wiki/Ring_oscillator", "环形振荡器频率与级数", "百科 / 振荡"),
    "w_barkhausen": ("Barkhausen stability criterion（英）", "https://en.wikipedia.org/wiki/Barkhausen_stability_criterion", "振荡条件的严格表述", "百科 / 振荡"),
    "w_555": ("555 timer IC（英）", "https://en.wikipedia.org/wiki/555_timer_IC", "内部结构三种经典接法", "百科 / 振荡"),
    "w_ldo": ("Low-dropout regulator（英）", "https://en.wikipedia.org/wiki/Low-dropout_regulator", "LDO 结构与压差", "百科 / 电源"),
    "w_buck": ("Buck converter（英）", "https://en.wikipedia.org/wiki/Buck_converter", "降压变换器工作原理", "百科 / 电源"),
    "w_classd": ("Class-D amplifier（英）", "https://en.wikipedia.org/wiki/Class-D_amplifier", "PWM 功放与效率", "百科 / 电源"),
    "w_noise": ("Electronic noise（英）", "https://en.wikipedia.org/wiki/Electronic_noise", "噪声类型总览", "百科 / 噪声"),
    "w_flicker": ("Flicker noise（英）", "https://en.wikipedia.org/wiki/Flicker_noise", "1/f 噪声的成因", "百科 / 噪声"),
    "w_thd": ("Total harmonic distortion（英）", "https://en.wikipedia.org/wiki/Total_harmonic_distortion", "THD 定义与测量", "百科 / 噪声"),
    "w_snr": ("Signal-to-noise ratio（英）", "https://en.wikipedia.org/wiki/Signal-to-noise_ratio", "SNR 与有效位数", "百科 / 噪声"),
    "w_mc": ("Monte Carlo method（英）", "https://en.wikipedia.org/wiki/Monte_Carlo_method", "统计抽样的一般方法", "百科 / 鲁棒性"),
    "w_spice": ("SPICE（英）", "https://en.wikipedia.org/wiki/SPICE", "仿真器历史与语法家族", "百科 / 仿真"),
    "w_netlist": ("Netlist（英）", "https://en.wikipedia.org/wiki/Netlist", "网表概念的通用定义", "百科 / 仿真"),
    "w_decoupling": ("Decoupling capacitor（英）", "https://en.wikipedia.org/wiki/Decoupling_capacitor", "去耦电容的作用与布局", "百科 / 实测"),
    "w_probe": ("Test probe（英）", "https://en.wikipedia.org/wiki/Test_probe", "示波器探头与负载效应", "百科 / 实测"),
    "w_pcb": ("Printed circuit board（英）", "https://en.wikipedia.org/wiki/Printed_circuit_board", "叠层、走线与寄生", "百科 / 实测"),
}

# 知识点关键词 -> 优先链接（按顺序命中，最多取 2 个）
TOPIC_RULES = [
    ("节点", ["w_nodal", "gh_basics"]), ("KCL", ["w_kcl", "aac"]),
    ("KVL", ["w_kcl", "aac"]), ("欧姆定律", ["w_kcl", "gh_basics"]),
    ("分压", ["w_divider", "gh_basics"]), ("分流", ["w_divider", "aac"]),
    ("负载效应", ["w_divider", "w_thevenin"]), ("戴维南", ["w_thevenin", "w_divider"]),
    ("诺顿", ["w_thevenin", "aac"]), ("叠加", ["w_kcl", "aac"]),
    ("节点电压法", ["w_nodal", "gh_ngspice"]), ("受控源", ["w_small_signal", "w_spice"]),
    (".tf", ["gh_pyltspice", "w_spice"]),
    ("时间常数", ["w_rc", "w_impedance"]), ("充放电", ["w_rc", "gh_basics"]),
    ("暂态", ["w_rc", "w_rlc"]), ("一阶", ["w_rc", "w_transfer"]),
    ("二阶", ["w_rlc", "w_q"]), ("阻尼", ["w_rlc", "w_q"]),
    ("阻抗", ["w_impedance", "w_transfer"]), ("相量", ["w_impedance", "w_bode"]),
    ("复数", ["w_impedance", "w_bode"]), ("传递函数", ["w_transfer", "w_bode"]),
    ("零极点", ["w_transfer", "w_bode"]), ("波特图", ["w_bode", "w_transfer"]),
    ("-3 dB", ["w_bode", "w_rc"]), ("寄生参数", ["w_pcb", "w_impedance"]),
    ("PN 结", ["w_diode", "w_zener"]), ("肖克利", ["w_diode", "ecc_placeholder"]),
    ("恒压降", ["w_diode", "ecircuit"]), ("分段线性", ["w_diode", "ecircuit"]),
    ("整流", ["w_rectifier", "gh_ecircuit"]), ("滤波", ["w_filter", "w_rc"]),
    ("限幅", ["w_diode", "gh_ecircuit"]), ("钳位", ["w_diode", "ecircuit"]),
    ("稳压二极管", ["w_zener", "ecircuit"]), ("I-V", ["w_diode", "w_mosfet"]),
    ("截止 / 线性 / 饱和", ["w_mosfet", "w_cs"]), ("阈值电压", ["w_mosfet", "w_gm"]),
    ("体效应", ["w_mosfet", "w_cascode"]), ("gm", ["w_gm", "w_small_signal"]),
    ("ro", ["w_small_signal", "w_cascode"]), ("本征增益", ["w_gm", "w_cs"]),
    ("小信号", ["w_small_signal", "w_gm"]), ("输出特性", ["w_mosfet", "w_cs"]),
    (".model NMOS", ["w_spice", "gh_ngspice"]), ("工作区", ["w_mosfet", "w_bjt"]),
    ("β", ["w_bjt", "w_ce"]), ("Ic-Vbe", ["w_bjt", "w_ce"]), ("rπ", ["w_bjt", "w_small_signal"]),
    ("共射", ["w_ce", "w_bjt"]), ("共集", ["w_bjt", "w_cs"]), ("共基", ["w_bjt", "w_cascode"]),
    ("共源", ["w_cs", "w_gm"]), ("共漏", ["w_cs", "w_mosfet"]), ("共栅", ["w_cascode", "w_cs"]),
    ("偏置", ["w_bjt", "w_mirror"]), ("组态", ["w_cs", "w_ce"]),
    ("理想运放", ["w_opamp", "aac"]), ("虚短", ["w_opamp", "w_feedback"]),
    ("虚断", ["w_opamp", "w_feedback"]), ("反相 / 同相", ["w_opamp", "aac"]),
    ("跟随", ["w_opamp", "w_feedback"]), ("差分", ["w_diff", "w_cmrr"]),
    ("负反馈", ["w_feedback", "w_opamp"]), ("闭环增益", ["w_feedback", "w_opamp"]),
    ("饱和与压摆", ["w_slew", "w_opamp"]), ("E 源", ["w_spice", "gh_ngspice"]),
    ("增益与 gm", ["w_gm", "w_cs"]), ("输入/输出阻抗", ["w_thevenin", "w_cs"]),
    ("摆幅", ["w_cs", "w_slew"]), ("源极退化", ["w_cs", "w_feedback"]),
    ("有源负载", ["w_mirror", "w_diff"]), (".op 查工作点", ["w_spice", "gh_pyltspice"]),
    ("电流镜", ["w_mirror", "gh_razavi"]), ("沟道长度调制", ["w_mosfet", "w_mirror"]),
    ("cascode", ["w_cascode", "w_mirror"]), ("PTAT", ["w_bandgap", "gh_razavi"]),
    ("带隙基准", ["w_bandgap", "ti"]), ("启动电路", ["w_bandgap", "ti"]),
    ("合规电压", ["w_mirror", "w_mosfet"]),
    ("差模", ["w_diff", "w_cmrr"]), ("共模", ["w_cmrr", "w_diff"]),
    ("半电路", ["w_diff", "w_small_signal"]), ("共模抑制比", ["w_cmrr", "w_diff"]),
    ("失调", ["w_opamp", "w_diff"]), ("共模范围", ["w_diff", "w_opamp"]),
    (".dc 传输曲线", ["w_spice", "w_diff"]),
    ("极点", ["w_transfer", "w_bode"]), ("密勒", ["w_miller", "w_cs"]),
    ("主极点", ["w_bode", "w_miller"]), ("GBW", ["w_miller", "w_bode"]),
    ("右半平面零点", ["w_transfer", "w_miller"]), (".ac 扫频", ["w_spice", "gh_pyltspice"]),
    ("环路增益", ["w_feedback", "w_nyquist"]), ("相位裕度", ["w_pm", "w_nyquist"]),
    ("增益/相位裕度", ["w_pm", "w_nyquist"]), ("补偿", ["w_pm", "w_opamp"]),
    ("稳定性判据", ["w_nyquist", "w_pm"]), ("四种反馈拓扑", ["w_feedback", "w_opamp"]),
    ("两级结构", ["w_opamp", "gh_razavi"]), ("指标分解", ["ti", "gh_razavi"]),
    ("摆率与功耗", ["w_slew", "w_opamp"]), ("PSRR", ["w_psrr", "ti"]),
    ("失调与 PSRR", ["w_psrr", "w_diff"]), ("设计检查表", ["ti", "gh_razavi"]),
    ("低通/高通/带通", ["w_filter", "w_rc"]), ("Q 值", ["w_q", "w_butterworth"]),
    ("Sallen-Key", ["w_filter", "w_butterworth"]), ("Butterworth", ["w_butterworth", "w_filter"]),
    ("多反馈", ["w_filter", "ti"]), ("运放带宽限制", ["w_opamp", "w_filter"]),
    ("开环比较器", ["w_comparator", "w_opamp"]), ("迟滞", ["w_schmitt", "w_comparator"]),
    ("巴克豪森", ["w_barkhausen", "w_ring"]), ("环形振荡器", ["w_ring", "w_barkhausen"]),
    ("RC / LC 振荡", ["w_rlc", "w_barkhausen"]), ("555", ["w_555", "gh_ecircuit"]),
    (".tran 看起振", ["w_spice", "w_ring"]),
    ("整流与纹波", ["w_rectifier", "w_rc"]), ("串联稳压", ["w_ldo", "ti"]),
    ("LDO", ["w_ldo", "ti"]), ("负载瞬态", ["w_ldo", "ti"]),
    ("Buck", ["w_buck", "ti"]), ("A/B/D 类功放", ["w_classd", "ti"]),
    ("功耗与热阻", ["w_classd", "ti"]),
    ("热噪声", ["w_noise", "w_snr"]), ("1/f", ["w_flicker", "w_noise"]),
    ("等效输入噪声", ["w_noise", "w_opamp"]), (".noise", ["w_spice", "w_noise"]),
    ("THD", ["w_thd", "w_snr"]), (".four", ["w_spice", "w_thd"]),
    ("误差预算", ["w_snr", "ti"]),
    ("PVT", ["w_mc", "gh_pyltspice"]), ("工艺角", ["w_mc", "gh_pyltspice"]),
    ("mc()", ["gh_pyltspice", "w_mc"]), ("gauss", ["gh_pyltspice", "w_mc"]),
    (".step", ["w_spice", "gh_pyltspice"]), ("直方图", ["w_mc", "gh_pyltspice"]),
    ("最坏情况", ["w_mc", "gh_pyltspice"]), ("良率", ["w_mc", "ti"]),
    ("接地", ["w_pcb", "w_decoupling"]), ("去耦", ["w_decoupling", "w_pcb"]),
    ("探头", ["w_probe", "w_decoupling"]), ("测量带宽", ["w_probe", "w_noise"]),
    ("分模块上电", ["w_pcb", "ecircuit"]), ("故障树", ["w_pcb", "adi_ez"]),
    ("传感器信号链", ["ti", "aac"]), ("音频", ["w_classd", "ti"]),
    ("课程设计", ["gh_cn", "gh_mick"]), ("规格与验收", ["ti", "gh_pyltspice"]),
    ("报告模板", ["gh_cn", "mit_ocw"]),
    ("元件行", ["w_netlist", "w_spice"]), (".model", ["w_spice", "gh_ngspice"]),
    (".param", ["w_spice", "gh_pyltspice"]), (".step 参数扫描", ["gh_pyltspice", "w_spice"]),
    (".meas", ["gh_pyltspice", "w_spice"]), (".include", ["w_netlist", "w_spice"]),
    ("收敛性", ["adi_ez", "w_spice"]), (".options", ["adi_ez", "gh_ngspice"]),
    (".op /", ["w_spice", "gh_basics"]), (".tran /", ["w_spice", "gh_basics"]),
    (".ac /", ["w_spice", "gh_ecircuit"]), (".dc", ["w_spice", "gh_ecircuit"]),
    ("Add Trace", ["adi_ltspice", "gh_basics"]), ("SPICE Error Log", ["adi_ez", "adi_ltspice"]),
    ("常用快捷键", ["adi_ltspice", "gh_basics"]), ("安装与界面", ["adi_ltspice", "gh_cn"]),
    (".asc", ["w_netlist", "gh_mick"]), (".cir", ["w_netlist", "gh_mick"]),
    ("符号约定", ["aac", "mit_ocw"]), ("单位前缀", ["aac", "gh_basics"]),
    ("先修数学", ["mit_ocw", "aac"]), ("手算与仿真", ["gh_cn", "ecircuit"]),
    ("术语", ["aac", "w_spice"]), ("推荐教材", ["mit_ocw", "aac"]),
    ("如何新增章节", ["gh_cn", "gh_pyltspice"]),
]
# 容错：规则里若出现未定义的 key，渲染时自动跳过
TOPIC_RULES = [(kw, [k for k in ks if k in R]) for kw, ks in TOPIC_RULES]

# 每章的默认扩展资源（4~6 个）与英文检索词
CHAPTER_RESOURCES = {
    "00": (["aac", "mit_ocw", "gh_cn", "ecircuit", "gh_basics"], "analog+electronics+intro"),
    "01": (["adi_ltspice", "gh_basics", "gh_cn", "falstad", "adi_ez"], "ltspice+tutorial"),
    "02": (["gh_ngspice", "w_spice", "w_netlist", "gh_pyltspice", "adi_ez"], "spice+netlist"),
    "03": (["w_divider", "w_kcl", "w_thevenin", "aac", "gh_basics"], "voltage+divider+kcl"),
    "04": (["w_rc", "w_rlc", "w_bode", "ecircuit", "falstad"], "rc+filter+ltspice"),
    "05": (["w_diode", "w_rectifier", "w_zener", "ecircuit", "gh_ecircuit"], "diode+rectifier+ltspice"),
    "06": (["w_mosfet", "w_gm", "w_small_signal", "w_cs", "gh_razavi"], "mosfet+common+source"),
    "07": (["w_bjt", "w_ce", "aac", "ecircuit", "gh_khannister"], "bjt+common+emitter"),
    "08": (["w_opamp", "w_feedback", "aac", "ti", "ecircuit"], "opamp+negative+feedback"),
    "09": (["w_cs", "w_ce", "w_gm", "gh_razavi", "ecircuit"], "single+stage+amplifier"),
    "10": (["w_mirror", "w_bandgap", "w_cascode", "gh_razavi", "ti"], "current+mirror+bandgap"),
    "11": (["w_diff", "w_cmrr", "w_small_signal", "gh_razavi", "ecircuit"], "differential+amplifier"),
    "12": (["w_bode", "w_miller", "w_transfer", "w_gm", "ti"], "miller+effect+frequency+response"),
    "13": (["w_feedback", "w_pm", "w_nyquist", "ti", "ecircuit"], "feedback+phase+margin"),
    "14": (["w_opamp", "w_slew", "w_psrr", "gh_razavi", "ti"], "two+stage+cmos+opamp"),
    "15": (["w_filter", "w_butterworth", "w_q", "ti", "ecircuit"], "sallen+key+active+filter"),
    "16": (["w_comparator", "w_schmitt", "w_ring", "w_555", "gh_ecircuit"], "schmitt+oscillator+ltspice"),
    "17": (["w_ldo", "w_buck", "w_rectifier", "w_classd", "ti"], "ldo+buck+ltspice"),
    "18": (["w_noise", "w_flicker", "w_thd", "w_snr", "ti"], "noise+thd+ltspice"),
    "19": (["gh_ecircuit", "gh_khannister", "gh_mick", "ecircuit", "ti"], "analog+circuit+reading"),
    "20": (["ti", "mit_ocw", "gh_pyltspice", "gh_cn", "adi_ez"], "analog+design+specification"),
    "21": (["gh_pyltspice", "pyltspice_docs", "adi_ez", "gh_ngspice", "ecircuit"], "ltspice+simulation+method"),
    "22": (["w_mc", "gh_pyltspice", "pyltspice_docs", "ti", "gh_ngspice"], "monte+carlo+ltspice"),
    "23": (["w_decoupling", "w_probe", "w_pcb", "ti", "adi_ez"], "pcb+decoupling+probe"),
    "24": (["gh_cn", "gh_mick", "ti", "mit_ocw", "gh_ecircuit"], "sensor+signal+chain+ltspice"),
    "A": (["w_spice", "w_netlist", "aac", "mit_ocw", "gh_topics_ltspice", "gh_topics_analog"], "ltspice+cheatsheet"),
}


def anchor(key):
    """生成一个外部链接 <a>。"""
    name, url, _note, _cat = R[key]
    return '<a href="' + html.escape(url, quote=True) + '" target="_blank" rel="noopener">' + html.escape(name) + "</a>"


def links_for_point(chapter_id, point, max_links=2):
    """按知识点文本匹配扩展链接，不足时用该章默认资源补齐。"""
    keys = []
    for kw, ks in TOPIC_RULES:
        if kw in point:
            for k in ks:
                if k not in keys and len(keys) < max_links:
                    keys.append(k)
            if len(keys) >= max_links:
                break
    default = CHAPTER_RESOURCES.get(chapter_id, ([], ""))[0]
    for k in default:
        if len(keys) >= max_links:
            break
        if k not in keys:
            keys.append(k)
    return " · ".join(anchor(k) for k in keys[:max_links])


def search_url(query, site="github"):
    if site == "github":
        return "https://github.com/search?q=" + urllib.parse.quote(query, safe="+") + "&type=repositories"
    return "https://www.ecircuitcenter.com/"


def chapter_links_html(chapter_id, root="../../"):
    """每章「扩展学习」小节的正文 HTML（root 为该页到工程根目录的相对路径）。"""
    keys, query = CHAPTER_RESOURCES.get(chapter_id, ([], "ltspice"))
    rows = []
    for k in keys:
        name, url, note, cat = R[k]
        rows.append("<li><strong>" + html.escape(name) + "</strong>（" + html.escape(cat) + "）：" +
                    html.escape(note) + "<br>" + anchor(k) + "</li>")
    gh_search = ('<a href="' + html.escape(search_url(query + "+LTspice"), quote=True) +
                 '" target="_blank" rel="noopener">在 GitHub 检索本章更多例程</a>')
    topic_search = ('<a href="' + html.escape(search_url(query), quote=True) +
                    '" target="_blank" rel="noopener">按本章主题检索开源项目</a>')
    return ('<p>以下链接按本章知识点挑选：前面是可以直接精读的资料，后面是可以拿来动手改的例程。'
            '每条知识点在上方「知识点地图」里也有对应的 1～2 个直达链接。</p>'
            '<ul>' + "\n".join(rows) + '</ul>'
            '<p class="code-hint">继续扩展：' + gh_search + ' · ' + topic_search +
            ' · <a href="' + root + 'index.html#resources">全书参考资源总表</a></p>')


def all_resources_html():
    """附录用的链接总表，按分类分组。"""
    cats = {}
    for k, (name, url, note, cat) in R.items():
        cats.setdefault(cat, []).append((name, url, note))
    out = ['<p>全书扩展学习链接集中在此，按用途分组。标注「GitHub」的仓库已核实可访问；'
           '英文百科条目适合作为某个知识点的第一份精读材料。</p>']
    for cat in sorted(cats):
        out.append("<h3>" + html.escape(cat) + "</h3><ul>")
        for name, url, note in cats[cat]:
            out.append('<li><a href="' + html.escape(url, quote=True) +
                       '" target="_blank" rel="noopener">' + html.escape(name) + "</a> — " +
                       html.escape(note) + "</li>")
        out.append("</ul>")
    return "\n".join(out)
