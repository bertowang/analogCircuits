#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「框架待补」章节的正文补写内容，按章节顺序组织。

build_book.py 在生成页面前把这里的 EXTRA_SECTIONS 追加到对应章节的
sections 末尾，并把这些章节的 status 统一置为 done。
后续要继续细化某章，直接在对应列表里加一节即可。
"""
from __future__ import annotations

EXTRA_SECTIONS = {

# ==================== 卷首 / 第一篇 ====================
"00": [
    ("0.4", "符号、单位与绘图约定", """<p>模拟电路的符号混乱是初学者的第一道坎，本书统一如下：</p>
<table><thead><tr><th>写法</th><th>含义</th><th>例子</th></tr></thead><tbody>
<tr><td><code>V<sub>GS</sub></code>、<code>I<sub>D</sub></code></td><td>直流总量 / 静态工作点</td><td><code>I<sub>D</sub> = 1 mA</code></td></tr>
<tr><td><code>v<sub>gs</sub></code>、<code>i<sub>d</sub></code></td><td>交流小信号量</td><td><code>i<sub>d</sub> = g<sub>m</sub>v<sub>gs</sub></code></td></tr>
<tr><td><code>v<sub>GS</sub>(t)</code></td><td>含直流偏置的瞬时总量</td><td><code>v<sub>GS</sub>(t) = V<sub>GS</sub> + v<sub>gs</sub>(t)</code></td></tr>
<tr><td><code>V(s)</code>、<code>H(s)</code></td><td>s 域 / 频域复数量</td><td><code>H(s) = 1/(1+sRC)</code></td></tr>
</tbody></table>
<p>其他约定：电流箭头默认指<strong>正电荷</strong>方向；算出负值说明实际方向相反，不必改方程。电压下标 <code>V<sub>ab</sub></code> 表示 a 点相对 b 点。参考地符号只表示<strong>人为选定的零电位</strong>，不等同于大地或机壳。工程记数法见<a href="../../appendix/index.html">附录 A.2</a>，特别注意 <code>m</code> 与 <code>Meg</code>。</p>
<div class="card note"><p style="margin-bottom:0">画图规范：电源在上、地在下，信号从左到右，反馈画出清晰的闭环，节点起有意义的名字。规范不只是好看——它直接决定别人（以及三个月后的你）能不能读懂这张图，参见<a href="../../part3/19-read-circuit/index.html">第 19 章</a>。</p></div>"""),
    ("0.5", "先修知识与学习节奏", """<p>本书只需要四块数学工具，缺哪块补哪块即可，不必先修完一整门课：</p>
<ol><li><strong>线性方程组</strong>：节点电压法就是列 KCL 方程组（第 3 章）。</li>
<li><strong>复数与相量</strong>：阻抗 <code>Z = R + jX</code>、幅角与模，用于 <code>.ac</code> 分析（第 4 章）。</li>
<li><strong>一阶常微分方程</strong>：RC/RL 充放电的指数解 <code>e<sup>−t/τ</sup></code>；会用三要素法就不用每次解微分方程。</li>
<li><strong>拉普拉斯变换的<em>结论</em></strong>：只要知道「电容 → 1/sC、电感 → sL」以及极零点与波特图的对应关系就够用；严格推导可留到信号与系统课。</li></ol>
<p>建议节奏：每章 2～3 学时，其中<strong>手算 1/3、仿真 1/3、改参数与记录 1/3</strong>。做完每章的四步闭环（手算 → 仿真 → 改参数 → 写结论）比多看三章但不做实验有效得多。</p>"""),
    ("0.6", "教材、数据手册与仿真：三种语言", """<p>同一个电路，在三种场合有三种写法，学会互相翻译才算入门：</p>
<table><thead><tr><th>场合</th><th>表达方式</th><th>关注点</th></tr></thead><tbody>
<tr><td>教材</td><td>小信号等效电路 + 符号推导</td><td>因果、趋势、可迁移的结论</td></tr>
<tr><td>数据手册 / 应用笔记</td><td>框图、参数表、典型应用电路</td><td>边界条件、裕量、外围元件怎么选</td></tr>
<tr><td>SPICE 网表</td><td>元件 + 节点 + 模型 + 分析指令</td><td>可执行的精确数值、非理想效应</td></tr>
</tbody></table>
<p>工业界的常见顺序是：先用教材公式圈定拓扑，再查数据手册确认边界，最后用仿真验证并留出裕量；反过来「先跑仿真再解释」很容易得出只在该模型下成立的结论。<a href="../../part3/20-design-circuit/index.html">第 20 章</a>与<a href="../../part3/21-simulation-method/index.html">第 21 章</a>会把这个顺序固化成流程。</p>"""),
],

"04": [
    ("4.2", "一阶电路的三要素法", """<p>任何只含一个储能元件的线性电路，响应都可以用三个数写出来，不必解微分方程：</p>
<span class="eq">v(t) = v(∞) + [ v(0⁺) − v(∞) ] · e<sup>−t/τ</sup></span>
<ul><li><strong>初值 v(0⁺)</strong>：电容电压（或电感电流）不能突变，等于换路前的 v(0⁻)。</li>
<li><strong>终值 v(∞)</strong>：把电容开路、电感短路，按直流电路求解。</li>
<li><strong>时间常数 τ</strong>：把独立源置零（电压源短路、电流源开路），从储能元件两端看进去的等效电阻 R<sub>th</sub>，一阶 RC 有 <code>τ = R<sub>th</sub>C</code>，RL 有 <code>τ = L/R<sub>th</sub></code>。</li></ul>
<p>常用结论：t = τ 时完成 63.2%，t = 3τ 约 95%，t = 5τ 约 99.3%；10%→90% 上升时间 ≈ 2.2τ。实验 4-1 与<a href="../../part3/21-simulation-method/index.html">第 21 章</a>的 <code>.meas</code> 都会用到这些数。</p>"""),
    ("4.3", "二阶系统、阻尼与谐振", """<p>含 L、C 两个储能元件的电路由二阶微分方程描述，标准形式为：</p>
<span class="eq">H(s) = H<sub>0</sub> ω<sub>0</sub>² / ( s² + (ω<sub>0</sub>/Q)s + ω<sub>0</sub>² )，　ω<sub>0</sub> = 1/√(LC)</span>
<p>也可以写成 <code>s² + 2ζω<sub>0</sub>s + ω<sub>0</sub>²</code>，其中阻尼比 <code>ζ = 1/(2Q)</code>：</p>
<table><thead><tr><th>阻尼</th><th>条件</th><th>阶跃响应</th><th>频域</th></tr></thead><tbody>
<tr><td>过阻尼</td><td>ζ &gt; 1（Q &lt; 0.5）</td><td>缓慢单调上升，无过冲</td><td>无谐振峰</td></tr>
<tr><td>临界阻尼</td><td>ζ = 1</td><td>最快无过冲</td><td>平坦</td></tr>
<tr><td>欠阻尼</td><td>ζ &lt; 1（Q &gt; 0.5）</td><td>过冲与振铃</td><td>出现谐振峰，峰值 ≈ Q</td></tr>
</tbody></table>
<p>串联 RLC 中 <code>Q = (1/R)√(L/C)</code>：R 越小 Q 越大、峰越尖、振铃越久。这与<a href="../../part2/13-feedback-stability/index.html">第 13 章</a>的相位裕度／阶跃过冲是完全对应的直觉，只是那里的「阻尼」由反馈环路提供。</p>"""),
    ("4.4", "阻抗、相量与传递函数", """<p>正弦稳态下把微分运算换成乘法，是频域分析的全部技巧：</p>
<table><thead><tr><th>元件</th><th>时域</th><th>s 域阻抗</th><th>正弦稳态</th></tr></thead><tbody>
<tr><td>电阻</td><td><code>v = Ri</code></td><td><code>R</code></td><td><code>R</code></td></tr>
<tr><td>电容</td><td><code>i = C dv/dt</code></td><td><code>1/(sC)</code></td><td><code>1/(jωC)</code></td></tr>
<tr><td>电感</td><td><code>v = L di/dt</code></td><td><code>sL</code></td><td><code>jωL</code></td></tr>
</tbody></table>
<p>于是分压公式直接给出 RC 低通的传递函数 <code>H(s) = 1/(1+sRC)</code>，一个实极点 <code>s = −1/RC</code>。画波特图的规则：每个极点从它的转折频率起贡献 −20 dB/dec 与最多 −90° 相移，每个零点贡献 +20 dB/dec 与最多 +90°；多个极零点的作用在对数坐标上直接相加。</p>
<div class="card tip"><p style="margin-bottom:0">这一节是<a href="../../part2/12-frequency-response/index.html">第 12 章</a>与<a href="../../part2/15-active-filters/index.html">第 15 章</a>的共同前置。能把「一个电容 + 一个电阻」翻译成「一个极点」，后面的多路反馈电路就只是把这句话重复几次。</p></div>"""),
    ("4.5", "实际元件的寄生参数", """<p>仿真与实测的差异，一半来自这里：</p>
<ul><li><strong>电阻</strong>：引线电感、并联寄生电容、公差（1%/5%）、温度系数 ppm/℃；高阻值电阻在高频已不再是纯电阻。</li>
<li><strong>电容</strong>：等效串联电阻 ESR、等效串联电感 ESL、漏电流、介质吸收；ESR 决定纹波与整流尖峰，ESL 决定自谐振频率，超过后电容<em>变成电感</em>。</li>
<li><strong>电感</strong>：绕组直流电阻、匝间电容、磁芯饱和与损耗。</li>
<li><strong>PCB</strong>：走线约 1 nH/mm、焊盘到地平面几 pF；这些在几十 MHz 以上就会改变频响（见<a href="../../part3/23-lab-debug/index.html">第 23 章</a>）。</li></ul>
<p>做实验时先跑理想模型确认公式，再逐个加寄生参数看曲线怎么变——这比一上来就用复杂模型更能建立因果直觉。</p>"""),
],

"07": [
    ("7.2", "工作区判据与指数关系", """<p>BJT 与 MOS 的推理框架完全一样，只是控制量从 <code>V<sub>GS</sub></code> 换成 <code>V<sub>BE</sub></code>、输入从「开路」变成「有电流」：</p>
<table><thead><tr><th>工作区</th><th>判据（NPN）</th><th>行为</th></tr></thead><tbody>
<tr><td>截止</td><td>V<sub>BE</sub> 低于约 0.6 V，且 V<sub>BC</sub> 反偏</td><td>I<sub>C</sub> ≈ 0，开关断开</td></tr>
<tr><td>放大区</td><td>V<sub>BE</sub> ≈ 0.6～0.8 V，且 <code>V<sub>BC</sub></code> 反偏（V<sub>CE</sub> &gt; V<sub>CE,sat</sub>）</td><td><code>I<sub>C</sub> = I<sub>S</sub> e<sup>V<sub>BE</sub>/V<sub>T</sub></sup></code>，<strong>放大器必须在此</strong></td></tr>
<tr><td>饱和区</td><td>发射结与集电结都正偏</td><td>V<sub>CE</sub> ≈ 0.2 V，开关闭合</td></tr>
</tbody></table>
<p>与 MOS 一样，判断顺序是「先假设工作区 → 线性化 → 算电压电流 → 验证结偏置」，即<a href="../05-diode/index.html">第 5 章</a>的假设—验证法。差别在于 BJT 基极<strong>要取电流</strong> <code>I<sub>B</sub> = I<sub>C</sub>/β</code>，因此前级会被加载。</p>"""),
    ("7.3", "小信号模型与三种组态", """<span class="eq">g<sub>m</sub> = I<sub>C</sub>/V<sub>T</sub>，　r<sub>π</sub> = β/g<sub>m</sub>，　r<sub>o</sub> ≈ V<sub>A</sub>/I<sub>C</sub></span>
<p>室温下 <code>V<sub>T</sub> ≈ 26 mV</code>，所以 <code>I<sub>C</sub> = 1 mA</code> 时 <code>g<sub>m</sub> ≈ 38 mS</code> —— 同样电流下 BJT 的跨导远大于 MOS（<code>g<sub>m</sub> = 2I<sub>D</sub>/V<sub>ov</sub></code>），这是它在低噪声、高精度场合仍被使用的原因。</p>
<table><thead><tr><th>组态</th><th>电压增益</th><th>输入阻抗</th><th>输出阻抗</th><th>相位</th></tr></thead><tbody>
<tr><td>共射 CE</td><td>高，<code>−g<sub>m</sub>R<sub>C</sub></code></td><td>≈ r<sub>π</sub>（中）</td><td>≈ R<sub>C</sub></td><td>反相</td></tr>
<tr><td>共集 CC（射随）</td><td>≈ 1</td><td>高，≈ (β+1)R<sub>E</sub></td><td>低，≈ 1/g<sub>m</sub></td><td>同相</td></tr>
<tr><td>共基 CB</td><td>高</td><td>低，≈ 1/g<sub>m</sub></td><td>高</td><td>同相</td></tr>
</tbody></table>
<p>三者与 MOS 的共源/共漏/共栅一一对应，只需把 <code>r<sub>π</sub></code> 换成「无穷大」、把 <code>V<sub>BE</sub></code> 换成 <code>V<sub>GS</sub></code>。建议把这张表和<a href="../06-mosfet/index.html">第 6 章</a>的表并排抄一次。</p>"""),
    ("7.4", "分压偏置：让电路不依赖 β", """<p>β 随器件、温度、电流可能变化 2～3 倍，所以「一个电阻定基极电流」的偏置不可用。实验 7-1 用的是分压偏置加发射极电阻：</p>
<span class="eq">V<sub>B</sub> ≈ V<sub>CC</sub>·R<sub>2</sub>/(R<sub>1</sub>+R<sub>2</sub>)，　I<sub>E</sub> ≈ (V<sub>B</sub> − 0.7 V)/R<sub>E</sub></span>
<p>成立条件是分压电流远大于基极电流（一般取 <code>I<sub>div</sub> ≥ 10 I<sub>B</sub></code>）。<code>R<sub>E</sub></code> 引入直流负反馈：温度上升 → I<sub>C</sub> 上升 → V<sub>E</sub> 上升 → V<sub>BE</sub> 下降 → 抑制 I<sub>C</sub>，从而稳定工作点。交流增益若要恢复，可给 <code>R<sub>E</sub></code> 并联旁路电容，或只旁路一部分（局部退化，见<a href="../../part2/09-single-stage/index.html">第 9 章</a>）。</p>
<div class="card note"><p style="margin-bottom:0">设计顺序：先定 I<sub>C</sub>（由功耗与 gm 决定）→ 定 V<sub>E</sub>（约 10%～20% V<sub>CC</sub>）→ 算 R<sub>E</sub> → 由 V<sub>B</sub> 选分压比 → 校核分压电流 → 由目标 V<sub>C</sub> 定 R<sub>C</sub> → 最后检查 V<sub>CE</sub> 是否留在放大区。</p></div>"""),
    ("7.5", "BJT 与 MOS 对照表", """<table><thead><tr><th>维度</th><th>BJT</th><th>MOSFET</th></tr></thead><tbody>
<tr><td>控制量</td><td>V<sub>BE</sub>（指数律）</td><td>V<sub>GS</sub>（平方律）</td></tr>
<tr><td>输入阻抗</td><td>有限（r<sub>π</sub>），需基极电流</td><td>极高，栅极几乎不取电流</td></tr>
<tr><td>同电流跨导</td><td>大（I<sub>C</sub>/V<sub>T</sub>）</td><td>较小（2I<sub>D</sub>/V<sub>ov</sub>）</td></tr>
<tr><td>低频噪声 / 失调</td><td>通常更优</td><td>1/f 噪声较明显</td></tr>
<tr><td>开关应用</td><td>有饱和压降、需驱动电流</td><td>导通电阻可控、驱动简单</td></tr>
<tr><td>集成工艺</td><td>双极 / BiCMOS</td><td>主流 CMOS</td></tr>
</tbody></table>
<p>没有谁更好，只有谁更适合：传感器前端、精密基准常见 BJT/双极输入；大规模混合信号与开关电路几乎都用 CMOS。读数据手册时先看输入偏置电流与噪声密度，往往就能猜出输入级用的是哪一种。</p>"""),
],

# ==================== 第二篇（前半） ====================
"09": [
    ("9.2", "三种组态的定量推导", """<p>把小信号模型代入，三种组态的差别可以一页写完（忽略 r<sub>o</sub>）：</p>
<table><thead><tr><th>组态</th><th>电压增益</th><th>输入电阻</th><th>输出电阻</th></tr></thead><tbody>
<tr><td>共源 / 共射</td><td><code>−g<sub>m</sub>(R<sub>D</sub> ∥ R<sub>L</sub>)</code></td><td>∞（MOS）/ r<sub>π</sub>（BJT）</td><td><code>R<sub>D</sub> ∥ r<sub>o</sub></code></td></tr>
<tr><td>共漏 / 共集</td><td><code>g<sub>m</sub>R<sub>S</sub>/(1+g<sub>m</sub>R<sub>S</sub>) ≈ 1</code></td><td>∞（MOS）</td><td><code>(1/g<sub>m</sub>) ∥ R<sub>S</sub></code></td></tr>
<tr><td>共栅 / 共基</td><td><code>+g<sub>m</sub>(R<sub>D</sub> ∥ R<sub>L</sub>)</code></td><td><code>≈ 1/g<sub>m</sub></code></td><td>高（cascode 后更高）</td></tr>
</tbody></table>
<p>推导只需两步：在输入回路写 KVL 得到控制电压（如 <code>v<sub>gs</sub></code>），在输出节点写 KCL 得到 <code>g<sub>m</sub>v<sub>gs</sub></code> 与负载的关系。任何陌生单级电路都可以这样拆，参见<a href="../../part3/19-read-circuit/index.html">第 19 章</a>。</p>"""),
    ("9.3", "偏置设计与摆幅预算", """<p>增益算得再漂亮，静态点不对也白搭。设计一只共源级的固定顺序：</p>
<ol><li>由功耗预算定 <code>I<sub>D</sub></code>；由线性度与面积定过驱动 <code>V<sub>ov</sub></code>（常取 0.1～0.3 V）。</li>
<li>由 <code>I<sub>D</sub> = ½K<sub>p</sub>(W/L)V<sub>ov</sub>²</code> 求 W/L，由 <code>g<sub>m</sub> = 2I<sub>D</sub>/V<sub>ov</sub></code> 得到跨导。</li>
<li>由目标增益定 <code>R<sub>D</sub></code>，检查直流压降：<code>V(out) = V<sub>DD</sub> − I<sub>D</sub>R<sub>D</sub></code>。</li>
<li><strong>摆幅校核</strong>：输出最低不能低于 <code>V<sub>ov</sub></code>（否则管子进线性区），最高不能超过 <code>V<sub>DD</sub></code>；把静态点放在两者中间可得到最大对称摆幅。</li>
<li>输入共模电平必须让管子导通，并给信号留够余量。</li></ol>
<div class="card warn"><p style="margin-bottom:0">最常见的失败：为了高增益把 R<sub>D</sub> 取得太大，静态 V(out) 被压到 <code>V<sub>ov</sub></code> 以下，管子掉进线性区，增益公式整个失效。先跑一次 <code>.op</code> 再谈增益。</p></div>"""),
    ("9.4", "源极退化：用增益换线性与确定性", """<p>源极串 <code>R<sub>S</sub></code> 后，栅压变化不会全部落到 <code>v<sub>gs</sub></code> 上：</p>
<span class="eq">A<sub>v</sub> ≈ − R<sub>D</sub> / ( R<sub>S</sub> + 1/g<sub>m</sub> )　（g<sub>m</sub>R<sub>S</sub> ≫ 1 时 ≈ −R<sub>D</sub>/R<sub>S</sub>）</span>
<p>这是<strong>局部负反馈</strong>：输出电流增大 → R<sub>S</sub> 上压降增大 → v<sub>gs</sub> 减小 → 抑制电流。收益是增益几乎只由两个电阻的比决定，对器件参数、温度、工艺不敏感，线性度明显改善；代价是增益下降、噪声略增、消耗一部分电压余量。</p>
<p>把 <code>R<sub>S</sub></code> 换成电容或分段旁路，就能在直流稳定与交流增益之间分别取舍——这种「直流负反馈、交流旁路」的手法在<a href="../14-opamp-design/index.html">第 14 章</a>与<a href="../17-power-supply/index.html">第 17 章</a>会反复出现。</p>"""),
    ("9.5", "有源负载：把电阻换成电流源", """<p>增益 <code>−g<sub>m</sub>R<sub>out</sub></code> 想做大，要么加电流（费功耗、降摆幅），要么提高 <code>R<sub>out</sub></code>。用<a href="../10-current-mirror/index.html">电流镜</a>作负载可得到 <code>R<sub>out</sub> = r<sub>on</sub> ∥ r<sub>op</sub></code>，通常比电阻大一个数量级，于是单级增益可达几十到上百。</p>
<p>代价有三：需要额外的偏置支路、输出摆幅受两管饱和电压挤压、带宽因高阻节点而变窄（该节点的极点变低，见<a href="../12-frequency-response/index.html">第 12 章</a>）。<strong>单级高增益必然伴随高阻节点</strong>，这是模拟设计中最基本的取舍之一。</p>"""),
],

"10": [
    ("10.2", "基本电流镜的定量分析", """<p>实验 10-1 的电路里，M1 栅漏短接，因此 <code>V<sub>GS</sub></code> 由基准电流唯一决定：</p>
<span class="eq">V<sub>GS</sub> = V<sub>to</sub> + √( 2I<sub>REF</sub> / (K<sub>p</sub>(W/L)<sub>1</sub>) )，　I<sub>OUT</sub> = I<sub>REF</sub> · (W/L)<sub>2</sub>/(W/L)<sub>1</sub></span>
<p>三条误差来源按重要性排序：</p>
<ol><li><strong>沟道长度调制</strong>：两管 V<sub>DS</sub> 不同，<code>I ∝ (1+λV<sub>DS</sub>)</code> 使镜像电流随输出电压漂移；L 取大、λ 取小可缓解。</li>
<li><strong>阈值与尺寸失配</strong>：工艺偏差使两管不再完全相同，是精密电路的主要误差。</li>
<li><strong>合规电压</strong>：输出管必须保持饱和，<code>V<sub>out</sub> ≥ V<sub>ov</sub></code>，低于此值电流塌陷。</li></ol>
<p>用 <code>.dc VOUT 0 5</code> 扫出来的曲线斜率，正是第一条误差的直接测量；把 <code>Lambda</code> 改成 0 再跑一次，曲线会变平。</p>"""),
    ("10.3", "cascode 与宽摆幅镜像", """<p>在输出管上再叠一只共栅管，把它栅极接固定偏置，输出管漏极电压被「钉住」，几乎不随 V<sub>out</sub> 变化：</p>
<span class="eq">R<sub>out, cascode</sub> ≈ g<sub>m</sub> r<sub>o</sub>²　（比单管 r<sub>o</sub> 高约 g<sub>m</sub>r<sub>o</sub> 倍）</span>
<p>镜像精度与增益因此大幅提高，代价是<strong>损失摆幅</strong>：输出最低电压从 <code>V<sub>ov</sub></code> 抬高到约 <code>2V<sub>ov</sub> + V<sub>bias</sub> 余量</code>。低电源电压设计里常用「宽摆幅 / 低压 cascode」把偏置电压精确设为 <code>V<sub>ov</sub> + V<sub>to</sub></code>，在保住输出阻抗的同时把摆幅损失压回一个 V<sub>ov</sub>。</p>
<p>这类「多叠一层管子换性能、再想办法把电压余量找回来」的套路，是<a href="../14-opamp-design/index.html">第 14 章</a>运放设计的主线。</p>"""),
    ("10.4", "带隙基准与启动电路", """<p>目标是一个与温度、电源、工艺都弱相关的电压。把两种相反温度系数的量加权求和：</p>
<ul><li><strong>CTAT</strong>：双极管的 <code>V<sub>BE</sub></code> 随温度约 −2 mV/℃；</li>
<li><strong>PTAT</strong>：两个不同电流密度 BJT 的 <code>ΔV<sub>BE</sub> = V<sub>T</sub>ln(n)</code> 随温度<em>正比</em>上升。</li></ul>
<span class="eq">V<sub>REF</sub> = V<sub>BE</sub> + K·ΔV<sub>BE</sub> ≈ 1.2 V（零温度系数，一阶抵消）</span>
<p>为什么一定要启动电路？因为「所有支路电流为零」也是这个电路的合法直流解：没有电流就没有 ΔV<sub>BE</sub>，误差放大器毫无理由把电路推离零点。启动支路在上电瞬间注入一股小电流，待基准建立后自动关断，避免影响正常工作。</p>
<div class="card tip"><p style="margin-bottom:0">读基准电路时，先找 PTAT 支路（不同面积的 BJT + 电阻），再找把 PTAT 与 CTAT 相加的运放，最后找那条「看起来多余」的启动管——这三块认清，图就读懂了（<a href="../../part3/19-read-circuit/index.html">第 19 章</a>）。</p></div>"""),
],

"11": [
    ("11.2", "大信号传输特性", """<p>实验 11-1 的 S 形曲线可以直接从平方律推出来。设尾电流为 I<sub>SS</sub>、过驱动为 V<sub>ov</sub>，则两支路电流差为：</p>
<span class="eq">ΔI = I<sub>SS</sub> · (v<sub>id</sub>/V<sub>ov</sub>) · √( 1 − (v<sub>id</sub>/(2V<sub>ov</sub>))² )　（|v<sub>id</sub>| ≤ √2 V<sub>ov</sub>）</span>
<p>结论比公式重要：</p>
<ul><li>在 <code>|v<sub>id</sub>| ≪ V<sub>ov</sub></code> 时近似线性，差分增益 ≈ <code>g<sub>m</sub>R<sub>D</sub></code>；</li>
<li><code>|v<sub>id</sub>| ≥ √2 V<sub>ov</sub></code> 时电流全部流向一侧，输出饱和——这段正是<strong>比较器</strong>与限幅放大器的工作区（<a href="../16-comparator-oscillator/index.html">第 16 章</a>）；</li>
<li>增大 V<sub>ov</sub>（或减小 W/L）可扩大线性输入范围，但会牺牲 gm 与增益。</li></ul>"""),
    ("11.3", "半电路法：把差分化成单管问题", """<p>对称电路可以在对称面切开，这是本章最有用的技巧：</p>
<table><thead><tr><th>激励</th><th>对称面</th><th>等效半电路</th><th>结论</th></tr></thead><tbody>
<tr><td>差模 v<sub>id</sub></td><td>交流地（虚地）</td><td>普通共源级，源极接地</td><td><code>A<sub>d</sub> = −g<sub>m</sub>(R<sub>D</sub> ∥ r<sub>o</sub>)</code></td></tr>
<tr><td>共模 v<sub>ic</sub></td><td>开路（无电流跨过）</td><td>带源极电阻 2R<sub>SS</sub> 的共源级</td><td><code>A<sub>c</sub> ≈ −R<sub>D</sub>/(2R<sub>SS</sub>)</code></td></tr>
</tbody></table>
<p>于是 <code>CMRR = |A<sub>d</sub>/A<sub>c</sub>| ≈ 2g<sub>m</sub>R<sub>SS</sub></code>：<strong>尾电流源的输出阻抗越大，共模抑制越好</strong>。这解释了为什么高性能运放要用 cascode 尾电流源，也解释了理想电流源（R<sub>SS</sub> → ∞）下共模增益为零。</p>"""),
    ("11.4", "有源负载、失调与共模范围", """<p>把两个漏极电阻换成 PMOS 电流镜（<a href="../10-current-mirror/index.html">第 10 章</a>），双端输出自动合并为单端：一侧电流增加、另一侧减少，经镜像相减后<strong>差模增益翻倍</strong>，同时共模增益进一步被抑制。这个结构就是<a href="../../part3/19-read-circuit/index.html">第 19 章</a>解剖的五管 OTA。</p>
<p>实际 CMRR 往往不由理论增益限制，而被<strong>失配</strong>限制：两管 V<sub>to</sub>、W/L、两个负载电阻的微小差异都会把共模泄漏成差模输出，并表现为输入失调电压 <code>V<sub>OS</sub></code>。增大输入管面积、采用共质心版图、加修调（trim）是常见对策。</p>
<p>输入共模范围（ICMR）：下限由尾电流管离开饱和区决定，上限由输入管或负载管离开饱和区决定。它和电源轨、摆幅一起构成运放数据手册的三项必查边界。</p>"""),
],

"12": [
    ("12.2", "单极点系统的波特图", """<p>把 <code>H(s) = A<sub>0</sub>/(1+s/ω<sub>p</sub>)</code> 中的 <code>s = jω</code> 代入：</p>
<span class="eq">|H| = A<sub>0</sub>/√(1+(ω/ω<sub>p</sub>)²)，　φ = −arctan(ω/ω<sub>p</sub>)</span>
<table><thead><tr><th>频率</th><th>幅度</th><th>相位</th></tr></thead><tbody>
<tr><td>ω ≪ ω<sub>p</sub></td><td>≈ A<sub>0</sub>（0 dB 平坦）</td><td>≈ 0°</td></tr>
<tr><td>ω = ω<sub>p</sub></td><td>A<sub>0</sub>/√2（−3 dB）</td><td>−45°</td></tr>
<tr><td>ω ≫ ω<sub>p</sub></td><td>−20 dB/dec 下降</td><td>→ −90°</td></tr>
</tbody></table>
<p>高频段 <code>|H| ≈ A<sub>0</sub>ω<sub>p</sub>/ω</code>，所以 <code>GBW = A<sub>0</sub>·f<sub>p</sub></code> 是常数：闭环增益降一半，带宽就翻倍。这条守恒关系是<a href="../13-feedback-stability/index.html">第 13 章</a>稳定性分析与<a href="../../part3/20-design-circuit/index.html">第 20 章</a>运放选型的核心依据。</p>"""),
    ("12.3", "密勒等效的推导", """<p>设电容 C 跨接在增益为 <code>A<sub>v</sub> = −A</code>（A &gt; 0）的反相级输入 x 与输出 y 之间。流过它的电流：</p>
<span class="eq">i = sC(v<sub>x</sub> − v<sub>y</sub>) = sC(1+A)v<sub>x</sub>　⇒　Z<sub>in</sub> = 1/[sC(1+A)]</span>
<p>即<strong>输入端看到一个被放大 (1+A) 倍的电容</strong>；输出端等效约 C/(1+1/A) ≈ C。一个 0.1 pF 的 <code>C<sub>gd</sub></code> 在增益 −4 的共源级里会变成 0.5 pF，若前级是 100 kΩ 高阻节点，主极点立刻降到几百 kHz。</p>
<p>因此判断主极点的实用口诀是：<strong>找「高节点阻抗 × 大等效电容 × 附近有大增益」的那个节点</strong>，而不是单纯找电容量最大的电容。实验 12-1 用 <code>.step param CGD</code> 把这条结论直接画出来。</p>"""),
    ("12.4", "主极点近似、零点与极点分裂", """<p>多级电路有多个极点，但若最低极点远低于其余（一般差 3 倍以上），可只保留它：</p>
<span class="eq">H(s) ≈ A<sub>0</sub> / [ (1+s/ω<sub>p1</sub>)(1+s/ω<sub>p2</sub>)… ] ≈ A<sub>0</sub>/(1+s/ω<sub>p1</sub>)</span>
<p>两条必须记住的例外：</p>
<ul><li><strong>右半平面零点</strong>（<code>s = +ω<sub>z</sub></code>）：幅度按 +20 dB/dec 上升，相位却像极点一样继续滞后，对稳定性伤害最大。共源级 <code>C<sub>gd</sub></code> 的前馈通路就产生 <code>ω<sub>z</sub> = g<sub>m</sub>/C<sub>gd</sub></code>；密勒补偿常串联调零电阻把它推到左半平面或推到高频。</li>
<li><strong>极点分裂</strong>：加补偿电容后主极点变低、次极点变高，二者被「推开」，这正是<a href="../13-feedback-stability/index.html">第 13 章</a>改善相位裕度的物理机制。</li></ul>"""),
],

"13": [
    ("13.2", "四种反馈拓扑与闭环增益", """<table><thead><tr><th>拓扑</th><th>输出采样</th><th>输入混合</th><th>典型电路</th><th>对阻抗的影响</th></tr></thead><tbody>
<tr><td>电压串联</td><td>电压</td><td>串联</td><td>同相放大器</td><td>R<sub>in</sub>↑、R<sub>out</sub>↓</td></tr>
<tr><td>电压并联</td><td>电压</td><td>并联</td><td>反相放大器</td><td>R<sub>in</sub>↓、R<sub>out</sub>↓</td></tr>
<tr><td>电流串联</td><td>电流</td><td>串联</td><td>跨导级</td><td>R<sub>in</sub>↑、R<sub>out</sub>↑</td></tr>
<tr><td>电流并联</td><td>电流</td><td>并联</td><td>电流放大器</td><td>R<sub>in</sub>↓、R<sub>out</sub>↑</td></tr>
</tbody></table>
<span class="eq">A<sub>cl</sub> = A/(1+Aβ)，　Aβ ≫ 1 时　A<sub>cl</sub> ≈ 1/β</span>
<p>「串联混合提高输入阻抗、并联混合降低输入阻抗；电压采样降低输出阻抗、电流采样提高输出阻抗」——记住这四句，就能从反馈类型反推电路适合驱动什么、被什么驱动。这也是<a href="../09-single-stage/index.html">第 9 章</a>三种组态阻抗差异的统一解释。</p>"""),
    ("13.3", "环路增益、相位裕度与判据", """<p>稳定性看的不是开环增益 A，而是<strong>环路增益 T = Aβ</strong>。在 <code>|T| = 1</code>（0 dB 交越频率）处：</p>
<span class="eq">PM = 180° + ∠T(ω<sub>c</sub>)　（工程上取 45°～60°）</span>
<ul><li>两个及更多低频极点各贡献最多 −90°，两级放大器合计可接近 −180°，很容易裕度不足；</li>
<li>PM 越小，闭环阶跃响应过冲越大、振铃越久；PM ≤ 0 时负反馈在该频率变成正反馈，电路自激；</li>
<li>严格判据是 <a href="../../appendix/index.html">Nyquist 判据</a>：对含右半平面极点或复杂环路的系统，光看 PM 不够。</li></ul>
<p>仿真里怎么测环路增益？在反馈环上断开一点，注入小信号 AC 源，测返回信号的比值和相位（返回比分析），或用 <code>.step</code> 扫补偿电容观察阶跃响应趋势——实验 13-1 采用后者，更直观且不易接错。</p>"""),
    ("13.4", "补偿技术与阶跃响应诊断", """<p>补偿的本质是<strong>重新安排极点的位置</strong>，用带宽换稳定：</p>
<table><thead><tr><th>方法</th><th>做法</th><th>代价</th></tr></thead><tbody>
<tr><td>主极点补偿</td><td>在最低极点节点加电容，把它推得更低</td><td>带宽大幅下降</td></tr>
<tr><td>密勒补偿</td><td>电容跨接两级之间，利用极点分裂</td><td>需处理右半平面零点</td></tr>
<tr><td>调零电阻</td><td>与补偿电容串联，移动零点位置</td><td>多一个元件与版图面积</td></tr>
<tr><td>前馈 / 增益分配</td><td>调整各级增益与电流，改变次极点</td><td>功耗与噪声预算变化</td></tr>
</tbody></table>
<p>从 <code>.tran</code> 阶跃波形反推稳定性：无过冲且单调 ≈ 裕度充足；一次过冲后迅速收敛 ≈ 60° 左右；多次等幅衰减振铃 ≈ 30° 以下；持续振荡 ≈ 已失稳。<strong>看到振铃先怀疑相位裕度，再怀疑电源去耦与寄生</strong>（后者见<a href="../../part3/23-lab-debug/index.html">第 23 章</a>）。</p>"""),
],

# ==================== 第二篇（后半） ====================
"14": [
    ("14.2", "两级 CMOS 运放的结构", """<p>经典两级运放由三部分组成，职责非常明确：</p>
<table><thead><tr><th>模块</th><th>电路</th><th>提供什么</th><th>主要代价</th></tr></thead><tbody>
<tr><td>第一级</td><td>NMOS 差分对 + PMOS 电流镜负载</td><td>高增益、高 CMRR、双端转单端</td><td>输入共模范围受限</td></tr>
<tr><td>第二级</td><td>共源放大管 + 电流源负载</td><td>大输出摆幅、驱动能力</td><td>引入第二个低频极点</td></tr>
<tr><td>补偿</td><td>跨接两级的密勒电容 C<sub>c</sub>（常串 R<sub>z</sub>）</td><td>极点分裂、保证相位裕度</td><td>带宽与压摆率下降</td></tr>
</tbody></table>
<p>信号链：差分输入 → 第一级高阻节点 n1 → 第二级 → 输出。<strong>n1 是主极点所在节点，输出是次极点所在节点</strong>；C<sub>c</sub> 跨接这两点，把主极点推向更低频、次极点推向更高频（<a href="../12-frequency-response/index.html">第 12 章</a>）。</p>"""),
    ("14.3", "从指标到尺寸：一次手算", """<p>规格示例：A<sub>0</sub> ≥ 60 dB、GBW = 10 MHz、相位裕度 ≥ 60°、负载 5 pF、电源 3.3 V、功耗 ≤ 1 mW、SR ≥ 10 V/µs。</p>
<ol><li><strong>补偿电容</strong>：次极点 <code>ω<sub>p2</sub> ≈ g<sub>m2</sub>/C<sub>L</sub></code> 需高于约 2.2 倍 GBW，而 <code>C<sub>c</sub> ≈ g<sub>m1</sub>/(2π·GBW)</code>；先估 g<sub>m1</sub> 得 C<sub>c</sub> 约 1～3 pF。</li>
<li><strong>尾电流</strong>：由 <code>SR = I<sub>tail</sub>/C<sub>c</sub></code> 反推 <code>I<sub>tail</sub> = SR·C<sub>c</sub></code>，约 20～30 µA，再定差分对每支路电流与 g<sub>m1</sub>。</li>
<li><strong>增益</strong>：<code>A<sub>0</sub> ≈ (g<sub>m1</sub>r<sub>o1</sub>)(g<sub>m2</sub>r<sub>o2</sub>)</code>；不足则增大管长 L 提高 r<sub>o</sub>，或改用 cascode。</li>
<li><strong>功耗校核</strong>：各支路电流之和乘 3.3 V 与 1 mW 比较，超了就回头调电流或放宽 SR。</li>
<li><strong>噪声与失调</strong>：输入管取大 W·L、小 V<sub>ov</sub> 有利于 1/f 噪声与匹配，但寄生电容变大会拉低次极点——又一处取舍。</li></ol>
<div class="card note"><p style="margin-bottom:0">几乎每一步都与另一步冲突，所以模拟设计不是解方程，而是<strong>反复迭代指标分配</strong>。把每次迭代的理由写进<a href="../../part3/20-design-circuit/index.html">第 20 章</a>的设计文档，比最后那组尺寸值更有价值。</p></div>"""),
    ("14.4", "非理想参数一览", """<table><thead><tr><th>参数</th><th>来源</th><th>影响</th><th>常见对策</th></tr></thead><tbody>
<tr><td>输入失调 V<sub>OS</sub></td><td>差分对与负载失配</td><td>直流误差、温漂</td><td>增大面积、共质心版图、修调、斩波</td></tr>
<tr><td>输入偏置电流</td><td>栅漏电 / 基极电流</td><td>高阻源上的误差</td><td>CMOS 输入、补偿电流</td></tr>
<tr><td>CMRR / PSRR</td><td>尾电流源阻抗有限、电源耦合</td><td>共模与纹波泄漏到输出</td><td>cascode 尾源、预稳压、全差分</td></tr>
<tr><td>压摆率 SR</td><td>尾电流给补偿电容充放电有限</td><td>大信号失真、建立变慢</td><td>增大尾电流、Class AB 输出级</td></tr>
<tr><td>噪声</td><td>热噪声 + 1/f</td><td>小信号分辨率</td><td>大输入管、斩波、相关双采样</td></tr>
<tr><td>共模范围 / 摆幅</td><td>各管饱和条件</td><td>可处理的幅度</td><td>互补差分对、轨到轨输出级</td></tr>
</tbody></table>
<p>读数据手册时按这张表逐行查参数，并注意测试条件（电源、温度、负载），否则「典型值」很容易被误用。</p>"""),
    ("14.5", "设计检查表", """<ol><li>各工艺角与温度下所有管子是否都饱和？用 <code>.op</code> 逐个查 <code>Vds ≥ Vov</code>。</li>
<li>输入共模范围与输出摆幅是否覆盖规格？</li>
<li>直流增益、GBW、相位裕度是否同时达标？<code>.ac</code> 加返回比分析。</li>
<li>阶跃过冲、建立时间、SR 是否达标？<code>.tran</code> 加 <code>.meas</code>。</li>
<li>CMRR / PSRR / 噪声 / 失调是否满足误差预算（<a href="../18-noise-distortion/index.html">第 18 章</a>）？</li>
<li>静态功耗与面积是否在预算内？</li>
<li>蒙特卡洛与最坏情况（<a href="../../part3/22-robustness/index.html">第 22 章</a>）是否仍满足规格？</li>
<li>启动、关断、上电顺序与保护是否考虑？</li></ol>
<p>把这张表作为设计文档最后一页，每轮迭代重跑一次，是工业界与课程设计共通的做法。</p>"""),
],

"15": [
    ("15.2", "二阶传递函数与逼近函数", """<span class="eq">H(s) = H<sub>0</sub> ω<sub>0</sub>² / ( s² + (ω<sub>0</sub>/Q)s + ω<sub>0</sub>² )</span>
<p>同一个分母，Q 取不同值给出不同「性格」：</p>
<table><thead><tr><th>逼近</th><th>Q（二阶节）</th><th>通带</th><th>阶跃 / 相位</th><th>适合</th></tr></thead><tbody>
<tr><td>Bessel</td><td>≈ 0.58</td><td>滚降最缓</td><td>近似线性相位，几乎无过冲</td><td>脉冲、音频瞬态</td></tr>
<tr><td>Butterworth</td><td>≈ 0.707</td><td>最平坦</td><td>轻微过冲</td><td>通用测量、抗混叠</td></tr>
<tr><td>Chebyshev</td><td>大于 0.707</td><td>有纹波</td><td>过冲较大</td><td>需要陡峭过渡带</td></tr>
</tbody></table>
<p>高阶滤波器由若干二阶节（biquad）级联实现，每节有自己的 ω<sub>0</sub> 与 Q；阶数越高过渡带越陡，但对元件公差与运放带宽越敏感。</p>"""),
    ("15.3", "Sallen-Key 设计步骤", """<p>实验 15-1 用单位增益（电压跟随器型）Sallen-Key，取 R<sub>1</sub> = R<sub>2</sub> = R：</p>
<span class="eq">f<sub>c</sub> = 1/(2πRC)，　Q = √(C<sub>1</sub>C<sub>2</sub>) / [ C<sub>2</sub> + C<sub>1</sub>(1−K) ]（K 为运放闭环增益）</span>
<p>设计顺序：</p>
<ol><li>由目标 f<sub>c</sub> 先选一个方便的标准电容 C（如 100 nF 用于低频、100 pF 用于高频）。</li>
<li>算 <code>R = 1/(2πf<sub>c</sub>C)</code>，检查 R 不要太小（加重运放负载）也不要太大（噪声与寄生敏感）。</li>
<li>由目标 Q 选 K 或调整 C<sub>1</sub>/C<sub>2</sub> 比值；单位增益 K = 1 时，等 R 等 C 得到 <code>Q = 1/3</code>（无峰、过阻尼），想要 Butterworth 需 K = 1.586。</li>
<li>确认运放 GBW 至少是 <code>K·f<sub>c</sub></code> 的 20～50 倍，否则实际 Q 与 f<sub>c</sub> 都会偏移。</li>
<li>用 <code>.ac</code> 验证 −3 dB 点、高频斜率（二阶为 −40 dB/dec）与峰值。</li></ol>"""),
    ("15.4", "运放非理想带来的偏差", """<ul><li><strong>有限带宽</strong>：f<sub>c</sub> 附近开环增益不足，跟随器不再「理想」，Q 被抬高或压低，甚至出现意外峰值。</li>
<li><strong>输出阻抗与压摆率</strong>：大信号时滤波器不再是线性系统，阶跃响应被 SR 限制。</li>
<li><strong>输入偏置电流与失调</strong>：高阻 RC 网络上的直流误差，经增益放大后可能吃掉后级动态范围。</li>
<li><strong>元件公差</strong>：Q 对电阻电容比值很敏感，1% 电阻 + 5% 电容足以让精密滤波器的通带纹波明显变化（<a href="../../part3/22-robustness/index.html">第 22 章</a>）。</li></ul>
<p>仿真时把理想 VCVS 换成带主极点的自建模型（<a href="../../part1/08-opamp-basics/index.html">第 8 章</a>）再跑一遍 <code>.ac</code>，是检验设计是否「只在理想世界里成立」的最快方法。</p>"""),
],

"16": [
    ("16.2", "比较器与迟滞阈值推导", """<p>比较器开环使用，输出只有高低两态，<strong>虚短完全不适用</strong>（<a href="../../part1/08-opamp-basics/index.html">第 8 章</a>）。加正反馈分压得到施密特触发器：设输入经 R<sub>1</sub>、输出经 R<sub>2</sub> 汇到比较器输入节点 v<sub>+</sub>，则</p>
<span class="eq">v<sub>+</sub> = (R<sub>2</sub>V<sub>in</sub> + R<sub>1</sub>V<sub>out</sub>)/(R<sub>1</sub>+R<sub>2</sub>)，　β = R<sub>1</sub>/(R<sub>1</sub>+R<sub>2</sub>)</span>
<p>输出为 +V<sub>OH</sub> 时，翻转条件是 <code>V<sub>in</sub> < −βV<sub>OH</sub></code>；输出为 −V<sub>OL</sub> 时，翻转条件是 <code>V<sub>in</sub> > βV<sub>OL</sub></code>。两个阈值之差就是<strong>迟滞宽度</strong>，也就是噪声容限：输入上叠加小于该宽度的噪声不会引起误翻转。</p>
<div class="card note"><p style="margin-bottom:0">慢边沿信号（如温度传感器、机械开关）若不加迟滞，会在阈值附近反复穿越，输出端出现一串毛刺——这是数字系统里最经典的模拟问题之一。</p></div>"""),
    ("16.3", "巴克豪森判据与起振", """<p>环路增益 <code>T(jω) = A(jω)β(jω)</code>。持续振荡需要同时满足：</p>
<span class="eq">|T(jω<sub>0</sub>)| ≥ 1　且　∠T(jω<sub>0</sub>) = 0°（或 360° 的整数倍）</span>
<ul><li>三级反相环：每级反相提供 180°，三级 RC 在 ω<sub>0</sub> 处再提供 180°，合计 360°，满足相位条件；</li>
<li><code>|T| < 1</code> 时扰动衰减，<code>|T| > 1</code> 时扰动指数增长，最终由<strong>非线性限幅</strong>（供电轨、增益压缩）把幅度稳定下来；</li>
<li>仿真中电路可能停在零平衡点不动，因为没有初始扰动——用 <code>.ic</code> 或噪声源踢一脚（实验 16-1）。</li></ul>
<p>振荡频率的粗略估计：N 级环形振荡器 <code>f ≈ 1/(2Nτ·k)</code>，其中 τ 是每级 RC 时间常数、k 为与级数相关的系数；精确值以 <code>.tran</code> 测周期为准。</p>"""),
    ("16.4", "四类振荡器对照", """<table><thead><tr><th>类型</th><th>选频/定时</th><th>频率稳定度</th><th>典型用途</th></tr></thead><tbody>
<tr><td>RC / 环形</td><td>R·C 或门延时</td><td>低，随 PVT 明显变化</td><td>片上时钟、简单时基</td></tr>
<tr><td>LC / 谐振</td><td>1/(2π√LC)</td><td>中，取决于 Q</td><td>射频振荡、VCO</td></tr>
<tr><td>晶体 / MEMS</td><td>机械谐振</td><td>高（ppm 级）</td><td>系统时钟、通信基准</td></tr>
<tr><td>555 定时器</td><td>外部 R、C 充放电</td><td>中低</td><td>PWM、单稳态、教学</td></tr>
</tbody></table>
<p>分析时都问同一组问题：能量从哪里补充（有源器件）、相位条件在哪里满足（选频网络）、幅度靠什么限制（非线性）、起振扰动从哪来。回答完这四问，任何振荡电路都能拆开。</p>"""),
],

"17": [
    ("17.2", "整流纹波的定量估算", """<p>二极管只在输入峰值附近导通给电容充电，其余时间电容独自向负载放电：</p>
<span class="eq">ΔV<sub>pp</sub> ≈ I<sub>load</sub>/(f·C)（半波），全波桥式约 I<sub>load</sub>/(2f·C)</span>
<p>推导只用了 <code>ΔQ = IΔt = CΔV</code>：放电时间约一个周期 1/f。因此减小纹波的三条路：加大 C、提高频率（全波/开关电源）、减小负载电流。</p>
<p>注意两个仿真与实物的差异：二极管只在短时间内导通，充电电流是<strong>窄而高的尖峰</strong>，会带来 EMI 与变压器利用率问题；电容 ESR 会额外叠加 <code>I<sub>peak</sub>·ESR</code> 的纹波，且决定电容寿命。实验 5-2 的 <code>.tran</code> 波形能同时看到这两点。</p>"""),
    ("17.3", "LDO 的环路、调整率与瞬态", """<p>LDO 可拆成四块：基准 V<sub>REF</sub>、误差放大器、调整管、反馈分压。设误差放大器增益 A、分压比 β，则</p>
<span class="eq">V<sub>out</sub> ≈ V<sub>REF</sub>/β · Aβ/(1+Aβ)　（Aβ 越大，静态误差越小）</span>
<p>三条常用指标：</p>
<ul><li><strong>线性调整率</strong>：输入电压变化引起的输出变化，由环路增益与 PSRR 决定。</li>
<li><strong>负载调整率</strong>：负载电流变化引起的输出变化，等于输出阻抗乘以电流变化；实验 17-1 的 0.5 Ω 输出电阻造成的约 10 mV 压降就是它。</li>
<li><strong>负载瞬态</strong>：电流阶跃时，先是输出电容 ESR 与容值决定的<em>瞬时下冲</em>，再由环路在有限带宽内把电压拉回；两者时间尺度不同，要分开看。</li></ul>
<p>输出电容的 ESR 还会在环路中引入一个零点：某些老结构<strong>需要</strong>一定 ESR 才能稳定，换成低 ESR 陶瓷电容反而振荡。这是「照抄应用电路却不能工作」的高频原因。</p>"""),
    ("17.4", "DC-DC 与功率放大", """<p><strong>Buck 变换器</strong>：开关导通时电感储能、关断时经二极管或同步管续流，稳态 <code>V<sub>out</sub> ≈ D·V<sub>in</sub></code>（D 为占空比）。电感电流纹波 <code>ΔI ≈ (V<sub>in</sub>−V<sub>out</sub>)D/(Lf<sub>sw</sub>)</code>，输出纹波由电容与 ESR 决定。效率远高于线性稳压，代价是开关噪声、EMI 与控制环路更复杂。</p>
<table><thead><tr><th>功放类别</th><th>导通角</th><th>理论效率</th><th>主要问题</th></tr></thead><tbody>
<tr><td>A 类</td><td>360°</td><td>25%～50%</td><td>静态功耗大</td></tr>
<tr><td>B / AB 类</td><td>180° / 略大于</td><td>约 70%</td><td>交越失真（AB 缓解）</td></tr>
<tr><td>D 类</td><td>开关工作</td><td>可超 90%</td><td>PWM 量化噪声、需 LC 滤波</td></tr>
</tbody></table>
<p>最后一步永远是热：<code>T<sub>j</sub> = T<sub>a</sub> + P<sub>diss</sub>·R<sub>θJA</sub></code>。线性稳压的压差乘电流、功放的损耗、开关管的导通与开关损耗都要算一遍，再决定散热片与封装。</p>"""),
],

"18": [
    ("18.2", "噪声源与等效输入噪声", """<table><thead><tr><th>类型</th><th>表达式</th><th>特征</th><th>对策</th></tr></thead><tbody>
<tr><td>电阻热噪声</td><td><code>v<sub>n</sub> = √(4kTR·B)</code></td><td>白噪声，1 kΩ ≈ 4 nV/√Hz</td><td>减小阻值、缩小带宽</td></tr>
<tr><td>散粒噪声</td><td><code>i<sub>n</sub> = √(2qI·B)</code></td><td>与直流电流成正比</td><td>降低偏置电流</td></tr>
<tr><td>1/f（闪烁）噪声</td><td><code>∝ 1/f</code></td><td>低频主导，MOS 明显</td><td>增大器件面积、斩波、P 管输入</td></tr>
</tbody></table>
<p>把各级噪声都折算到输入端（除以该级之前的增益），得到<strong>等效输入噪声</strong>，才能在同一个尺度上比较。由此得到模拟前端最重要的结论：<strong>第一级的增益与噪声几乎决定整个系统</strong>，后面各级的噪声被前级增益除掉后通常可以忽略。</p>
<p>带宽要注意：白噪声的积分用的是<strong>噪声带宽</strong>而非 −3 dB 带宽，一阶低通的噪声带宽为 <code>1.57·f<sub>c</sub></code>。实验 18-1 的 <code>.noise</code> 输出里 <code>V(onoise)</code> 是密度、积分曲线是总噪声，二者不要混用。</p>"""),
    ("18.3", "失真、谐波与 THD", """<p>非线性使输出出现输入没有的频率分量。对称削顶（实验 18-2）只产生奇次谐波 3f、5f…，非对称失真还会产生偶次谐波。</p>
<span class="eq">THD = √(V<sub>2</sub>²+V<sub>3</sub>²+…)/V<sub>1</sub></span>
<p>用 <code>.four 1k V(out)</code> 得到各次谐波幅值与 THD，前提是：仿真时间足够长以进入稳态、只取整数个周期、关掉波形压缩（<code>.options plotwinsize=0</code>）。否则频谱会出现本不存在的杂散。</p>
<p>与噪声的区别很关键：噪声与信号幅度<strong>无关</strong>，决定了能分辨的最小信号；失真随信号幅度<strong>急剧增大</strong>，决定了最大不失真信号。两者之间的距离就是动态范围，常用 SNR、SINAD、ENOB 描述（数据转换器接口必查）。</p>"""),
    ("18.4", "误差预算表", """<p>不要凭感觉换运放，先把误差逐项列出来：</p>
<table><thead><tr><th>误差项</th><th>典型来源</th><th>量级示例</th><th>合成方式</th></tr></thead><tbody>
<tr><td>增益误差</td><td>电阻公差、有限开环增益</td><td>0.1% + 0.01%</td><td>系统项，按最坏情况相加</td></tr>
<tr><td>失调与温漂</td><td>V<sub>OS</sub>、dV<sub>OS</sub>/dT</td><td>100 µV + 2 µV/℃</td><td>系统项，按最坏情况相加</td></tr>
<tr><td>噪声</td><td>热噪声、1/f、电源纹波耦合</td><td>10 µV<sub>rms</sub></td><td>随机项，按均方根合成</td></tr>
<tr><td>非线性</td><td>摆幅、压摆率、THD</td><td>0.01%</td><td>单独设上限</td></tr>
<tr><td>PSRR / CMRR</td><td>电源与共模泄漏</td><td>60 dB</td><td>按实际纹波折算</td></tr>
</tbody></table>
<p>两类误差不能简单相加：独立的随机项按 <code>√(Σe<sub>i</sub>²)</code> 合成，系统性偏差按最坏情况直接相加。填完表后，找出最大的一两项去优化，收益远高于把所有器件都升级一档。</p>"""),
],

# ==================== 第三篇 / 第四篇 ====================
"22": [
    ("22.2", "PVT 与工艺角", """<p>典型条件（TT、25 ℃、标称电源）下的漂亮曲线只是起点。批量生产要面对三组变化：</p>
<table><thead><tr><th>维度</th><th>常见取值</th><th>主要影响</th></tr></thead><tbody>
<tr><td>Process（工艺角）</td><td>TT / FF / SS / FS / SF（NMOS 与 PMOS 快、慢组合）</td><td>V<sub>to</sub>、迁移率、增益、带宽</td></tr>
<tr><td>Voltage</td><td>标称 ±10%</td><td>摆幅、静态点、压摆率</td></tr>
<tr><td>Temperature</td><td>−40 / 25 / 125 ℃</td><td>V<sub>BE</sub>、V<sub>to</sub>、迁移率、漏电流</td></tr>
</tbody></table>
<p>穷举全部组合（5 × 3 × 3 = 45 个角）常用脚本批量跑：<a href="../../index.html#resources">PyLTSpice</a> 可以用 Python 循环改 <code>.param</code>、调用 LTspice 命令行、解析 <code>.log</code> 里的 <code>.meas</code> 结果，自动生成一张通过/失败表。</p>"""),
    ("22.3", "蒙特卡洛：从单次仿真到分布", """<p>工艺角描述的是<strong>全局</strong>偏差（整片晶圆一起偏），蒙特卡洛描述的是<strong>局部失配</strong>（同一芯片上两个本应相同的器件不一样）。LTspice 提供：</p>
<ul><li><code>mc(x, tol)</code>：在 x·(1±tol) 内均匀分布随机取值；</li>
<li><code>gauss(x)</code>：正态分布的随机偏移；</li>
<li><code>.step param run 1 N 1</code>：让每次运行取一组新随机数（N 常取 50～1000）。</li></ul>
<p>实验 22-1 里 R1 取 1%、R2 取 5%，输出分布明显由 R2 主导。把 N 组 <code>.meas</code> 结果导出成 CSV，用 Python 算均值、σ、画直方图，就能回答「良率多少」而不是「这次对不对」。</p>
<div class="card warn"><p style="margin-bottom:0">常见错误：多个元件共用同一个随机表达式，导致它们的误差<strong>完全相关</strong>，仿真结果远比现实乐观。每个元件应有独立的 <code>mc()</code> 调用。</p></div>"""),
    ("22.4", "灵敏度、最坏情况与裕量", """<ol><li><strong>灵敏度分析</strong>：一次只改一个参数 ±10%，记录输出变化，按影响大小排序；预算只花在前几项上。</li>
<li><strong>最坏情况（WCA）</strong>：把每个参数取对规格最不利的端点同时组合。它对线性单调系统很保守、组合数按 2ⁿ 增长；<a href="../../index.html#resources">PyLTSpice 的 WorstCaseAnalysis</a> 用位编码自动枚举这些组合。</li>
<li><strong>蒙特卡洛</strong>：给分布与良率，更接近量产，但不能证明「极端情况也过」。</li>
<li><strong>裕量</strong>：规格不是目标值而是边界。典型条件下让增益、带宽、相位裕度、摆幅各留 10%～20%（相位裕度留 45°～60°），公差带内才不会越界。</li></ol>
<p>三者的关系：灵敏度找主因 → 最坏情况保底线 → 蒙特卡洛估良率。只做其中一个，都不足以支撑「可以投产」的结论。</p>"""),
    ("22.5", "把鲁棒性写进验收表", """<p>在<a href="../20-design-circuit/index.html">第 20 章</a>的验收表基础上，把每个指标扩成三列：典型值 / 最坏情况 / 蒙特卡洛 3σ。例如增益一行：<code>10.00 / 9.88～10.12 / σ = 0.02</code>。再加一条明确的判据（如「全部条件下误差不超过 2%」）。</p>
<p>这样仿真就从「画几条曲线」升级成可重复的回归测试：以后改任何一个参数，跑一次脚本就知道是否仍然通过。<a href="../21-simulation-method/index.html">第 21 章</a>的 <code>.meas</code> 断言是这套流程的基础。</p>"""),
],

"23": [
    ("23.2", "接地、回流路径与去耦", """<p>电流总是走<strong>闭合回路</strong>，信号线上的电流必然有一条对应的回流路径。「地」不是无限大的吸收池，而是有阻抗的导体：</p>
<ul><li>低频时回流倾向于走电阻最小的路径，高频时倾向于紧贴信号线正下方（电感最小）；把地平面切开，等于强迫回流绕远路，形成环路天线。</li>
<li>模拟地与数字地不必盲目分割，关键是把<strong>各自的高频回流限制在各自区域</strong>，只在一点汇合。</li>
<li>去耦电容为器件提供本地瞬态电流，<strong>摆放位置比容量更重要</strong>；容量越大往往自谐振频率越低，因此常见大小电容并联，分别覆盖低频与高频。</li>
<li>电源入口的 bulk 电容负责低频能量，芯片脚边的 100 nF / 1 nF 负责高频，布局时先画回流路径再摆件。</li></ul>
<p>把一段走线电感（约 1 nH/mm）、地平面阻抗、去耦 ESR/ESL 加进仿真，很多「仿真正常、上电振荡」的现象就能复现。</p>"""),
    ("23.3", "测量链路：探头也是一种元件", """<p>实验 23-1 说明的核心事实：<strong>测量仪器会改变被测电路</strong>。</p>
<table><thead><tr><th>仪器 / 探头</th><th>等效模型</th><th>容易踩的坑</th></tr></thead><tbody>
<tr><td>示波器 10× 探头</td><td>约 10 MΩ ∥ 10～15 pF</td><td>1 MHz 时容抗仅约 10 kΩ，会拉低高阻节点带宽</td></tr>
<tr><td>1× 探头 / 同轴直连</td><td>约 1 MΩ ∥ 100 pF 以上</td><td>电容更大，高频几乎必然失真</td></tr>
<tr><td>万用表</td><td>约 10 MΩ（电压档）</td><td>测高阻分压点会改变分压比</td></tr>
<tr><td>信号源</td><td>50 Ω 内阻</td><td>未端接时实际幅度可能是设定值的两倍</td></tr>
</tbody></table>
<p>长接地线会引入额外电感，与探头电容构成谐振，测高速边沿时出现「明明没有的振铃」。正确做法是用短接地弹簧、在带宽允许时开启 20 MHz 带宽限制、并把探头模型放进仿真测试台（<a href="../21-simulation-method/index.html">第 21 章</a>）。</p>"""),
    ("23.4", "上电调试流程与故障树", """<ol><li>断电目视：极性元件、短路、虚焊、芯片方向。</li>
<li>万用表测电源到地是否短路；用<strong>限流电源</strong>上电，把电流限到预期的 1.2 倍。</li>
<li>先只测各电源电压是否正确、纹波是否异常，不接信号。</li>
<li>逐级测直流工作点，与 <code>.op</code> 结果对照；某一级不对就先停在这一级。</li>
<li>从输入端注入小信号，用示波器逐级跟踪波形，定位失真/衰减/振荡发生在哪一级。</li>
<li>最后才做全链路指标测试。</li></ol>
<p>故障树示例：输出无信号 → 电源正常？→ 本级静态点正常？→ 输入信号到达本级？→ 反馈环是否接反？→ 是否自激（关掉输入看输出有无振荡）？→ 负载是否过重？每步只排除一种可能，比「整板重焊」快得多。</p>
<div class="card tip"><p style="margin-bottom:0">实测与仿真不符时的排查顺序：<strong>先补寄生与仪器模型，再核对原理图与元件值，最后才怀疑器件损坏</strong>。绝大多数差异来自前两项。</p></div>"""),
],

"24": [
    ("24.2", "课题 A：传感器信号链（完整拆解）", """<p><strong>规格</strong>：桥式传感器差分输出 ±10 mV、共模 1.25 V、源阻抗 1 kΩ；输出 0～2 V 单端；带宽 100 Hz；共模抑制 ≥ 60 dB；电源 3.3 V；总误差 ≤ 2%。</p>
<table><thead><tr><th>模块</th><th>选型</th><th>指标分配</th><th>对应章节</th></tr></thead><tbody>
<tr><td>前置放大</td><td>仪表放大器 / 三运放结构</td><td>增益 100，输入噪声 < 20 nV/√Hz</td><td><a href="../../part2/11-diff-amp/index.html">11</a>、<a href="../../part2/18-noise-distortion/index.html">18</a></td></tr>
<tr><td>电平搬移</td><td>参考电压 + 差分/同相级</td><td>把双极性信号移到 ADC 中点</td><td><a href="../../part1/08-opamp-basics/index.html">8</a></td></tr>
<tr><td>抗混叠滤波</td><td>二阶 Butterworth 低通</td><td>f<sub>c</sub> = 100 Hz，−40 dB/dec</td><td><a href="../../part2/15-active-filters/index.html">15</a></td></tr>
<tr><td>参考与电源</td><td>基准 + LDO + 去耦</td><td>PSRR 与纹波预算</td><td><a href="../../part2/10-current-mirror/index.html">10</a>、<a href="../../part2/17-power-supply/index.html">17</a></td></tr>
</tbody></table>
<p>验收：用 <code>.ac</code> 测通带增益与 −3 dB 点；用 <code>.tran</code> 测阶跃建立；注入共模信号测 CMRR；用 <code>.noise</code> 积分得到输出噪声；最后按<a href="../../part3/20-design-circuit/index.html">第 20 章</a>写规格—实测评审表，并按<a href="../../part3/22-robustness/index.html">第 22 章</a>补公差分析。实验 24-1 是这条链的最小可运行版本。</p>"""),
    ("24.3", "课题 B / C 的关键难点", """<p><strong>课题 B · 音频放大器</strong>（8 Ω、1 W、20 Hz～20 kHz、THD ≤ 1%）：</p>
<ul><li>输出功率换算：<code>V<sub>rms</sub> = √(PR) = 2.83 V</code>，峰值 4 V，需检查电源与输出级摆幅；</li>
<li>难点在交越失真与热：AB 类输出级偏置、负反馈降低 THD、<code>.four</code> 验收、功耗与散热估算；</li>
<li>稳定性：容性负载（扬声器线缆）与输出级易自激，需做相位裕度检查。</li></ul>
<p><strong>课题 C · 基准与 LDO</strong>（3.3 V、0～100 mA、PSRR ≥ 40 dB）：</p>
<ul><li>难点在启动电路与温度系数：用 <code>.dc</code> 扫温度、<code>.step</code> 扫电源与负载；</li>
<li>瞬态：负载阶跃的下冲幅度与恢复时间分别由输出电容和环路带宽决定，要分开优化；</li>
<li>蒙特卡洛：带隙基准的失配直接决定输出电压分布，是本题最值得做的统计实验。</li></ul>"""),
    ("24.4", "报告模板与验收清单", """<ol><li><strong>规格表</strong>：每条指标写清数值与测量方法。</li>
<li><strong>指标分解树与选型理由</strong>：选了什么拓扑、放弃了什么、为什么。</li>
<li><strong>手算过程</strong>：关键公式、参数、数量级校核。</li>
<li><strong>原理图 / 网表</strong>：节点命名、模块标注、测试台与被测电路分开。</li>
<li><strong>仿真验收表</strong>：目标值 / 实测值 / 通过与否 / 使用的分析指令。</li>
<li><strong>公差与最坏情况</strong>：PVT、蒙特卡洛、裕量结论。</li>
<li><strong>波形与判读</strong>：每张图配一句结论，不要只贴截图。</li>
<li><strong>遗留风险与实测计划</strong>：哪些非理想尚未建模、上电时先测什么。</li></ol>
<p>自测清单：所有 <code>.cir</code> 能直接 Run？<code>.op</code> 工作点合理？<code>.meas</code> 断言齐全？改一个参数后结论是否仍成立？把<a href="../../part3/19-read-circuit/index.html">第 19 章</a>十步法反过来用在自己的设计上，能独立讲清每一块的作用，就达到了本科课程设计的要求。</p>"""),
],

}
