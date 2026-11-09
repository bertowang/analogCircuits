/* 全书目录唯一数据源（侧边栏、面包屑、上下章导航共用）
   新增章节：在对应 parts[].chapters 追加一项，并在 index.html 中补一条目录即可。
   status: done = 已完稿 | skeleton = 框架已建、正文待补充 | todo = 仅有标题 */
window.BOOK_TOC = {
  title: "模拟电路：从读懂到设计",
  subtitle: "一本配 LTspice 实验的本科教材",
  parts: [
    {
      id: "p0", title: "卷首 · 工具与约定",
      chapters: [
        { id: "00", title: "绪论：如何阅读这本教材", path: "part0/00-preface/index.html", status: "done" },
        { id: "01", title: "LTspice 快速上手", path: "part0/01-ltspice-quickstart/index.html", status: "done" },
        { id: "02", title: "SPICE 网表语法与仿真指令", path: "part0/02-spice-netlist/index.html", status: "done" }
      ]
    },
    {
      id: "p1", title: "第一篇 · 电路基础与器件",
      chapters: [
        { id: "03", title: "电路定律与读图第一步", path: "part1/03-circuit-laws/index.html", status: "done" },
        { id: "04", title: "无源元件、暂态与频域", path: "part1/04-passive-dynamics/index.html", status: "done" },
        { id: "05", title: "二极管与整流、限幅电路", path: "part1/05-diode/index.html", status: "done" },
        { id: "06", title: "MOSFET 与两级模型", path: "part1/06-mosfet/index.html", status: "done" },
        { id: "07", title: "BJT 与三种基本组态", path: "part1/07-bjt/index.html", status: "done" },
        { id: "08", title: "理想运放与负反馈入门", path: "part1/08-opamp-basics/index.html", status: "done" }
      ]
    },
    {
      id: "p2", title: "第二篇 · 核心模拟电路模块",
      chapters: [
        { id: "09", title: "单级放大器", path: "part2/09-single-stage/index.html", status: "done" },
        { id: "10", title: "电流源、电流镜与基准", path: "part2/10-current-mirror/index.html", status: "done" },
        { id: "11", title: "差分放大器", path: "part2/11-diff-amp/index.html", status: "done" },
        { id: "12", title: "频率响应与极点", path: "part2/12-frequency-response/index.html", status: "done" },
        { id: "13", title: "反馈与稳定性", path: "part2/13-feedback-stability/index.html", status: "done" },
        { id: "14", title: "运算放大器设计", path: "part2/14-opamp-design/index.html", status: "done" },
        { id: "15", title: "有源滤波器", path: "part2/15-active-filters/index.html", status: "done" },
        { id: "16", title: "比较器、施密特触发与振荡器", path: "part2/16-comparator-oscillator/index.html", status: "done" },
        { id: "17", title: "电源与功率电路", path: "part2/17-power-supply/index.html", status: "done" },
        { id: "18", title: "噪声、失真与误差预算", path: "part2/18-noise-distortion/index.html", status: "done" }
      ]
    },
    {
      id: "p3", title: "第三篇 · 方法论：从读懂到设计",
      chapters: [
        { id: "19", title: "如何读懂一个陌生电路", path: "part3/19-read-circuit/index.html", status: "done" },
        { id: "20", title: "如何从规格设计电路", path: "part3/20-design-circuit/index.html", status: "done" },
        { id: "21", title: "仿真方法论", path: "part3/21-simulation-method/index.html", status: "done" },
        { id: "22", title: "鲁棒性：PVT、蒙特卡洛与最坏情况", path: "part3/22-robustness/index.html", status: "done" },
        { id: "23", title: "从仿真到实物：PCB、仪器与调试", path: "part3/23-lab-debug/index.html", status: "done" }
      ]
    },
    {
      id: "p4", title: "第四篇 · 综合课程设计",
      chapters: [
        { id: "24", title: "综合实验与课程设计课题", path: "part4/24-projects/index.html", status: "done" }
      ]
    },
    {
      id: "pa", title: "附录",
      chapters: [
        { id: "A", title: "附录 · 公式、指令与术语速查", path: "appendix/index.html", status: "done" }
      ]
    }
  ]
};

window.BOOK_FLAT = (function () {
  const out = [];
  (window.BOOK_TOC.parts || []).forEach(function (part) {
    (part.chapters || []).forEach(function (ch) {
      out.push(Object.assign({ partId: part.id, partTitle: part.title }, ch));
    });
  });
  return out;
})();
