#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从章节 HTML 中抽取 LTspice 网表，保持页面与 .cir 文件一致。

单一数据源原则：LTspice 代码写在 HTML 的
    <pre class="spice" data-file="sim/xxx.cir"><code>...</code></pre>
里，本脚本把它写成同章节目录下的 sim/xxx.cir，供 LTspice 直接打开运行。
data-file="inline" 的代码块是语法片段，会被跳过。

用法:
    python3 tools/extract_netlists.py            # 同步写入 / 更新
    python3 tools/extract_netlists.py --check   # 只检查是否已同步，不写文件
    python3 tools/extract_netlists.py --clean   # 同步后删除已无对应代码块的旧 .cir
"""
from __future__ import annotations

import argparse
import html as html_mod
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOCK = re.compile(
    r'<pre\s+class="spice"\s+data-file="([^"]+)"\s*><code>(.*?)</code></pre>',
    re.DOTALL,
)


def collect():
    """返回 {目标 .cir 路径: 网表文本}。"""
    found = {}
    pages = [p for p in sorted(ROOT.rglob("index.html")) if p.parent != ROOT]
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for m in BLOCK.finditer(text):
            rel, body = m.group(1), m.group(2)
            if rel == "inline" or "/" not in rel:
                continue
            target = (page.parent / rel).resolve()
            if not target.is_relative_to(ROOT):
                print("跳过越界路径:", rel, file=sys.stderr)
                continue
            code = html_mod.unescape(body).strip("\n")
            if not code.endswith("\n"):
                code += "\n"
            if target in found and found[target] != code:
                print("警告：同名代码块内容不一致 ->", target.relative_to(ROOT), file=sys.stderr)
            found[target] = code
    return found


def main():
    ap = argparse.ArgumentParser(description="从 HTML 代码块同步 LTspice 网表")
    ap.add_argument("--check", action="store_true", help="只检查，不写文件")
    ap.add_argument("--clean", action="store_true", help="删除已无对应代码块的旧 .cir")
    args = ap.parse_args()

    found = collect()
    changed, missing, ok = [], [], 0
    for target, code in sorted(found.items()):
        rel = target.relative_to(ROOT)
        if not target.exists():
            missing.append(str(rel))
        elif target.read_text(encoding="utf-8") != code:
            changed.append(str(rel))
        else:
            ok += 1

    if args.check:
        if missing or changed:
            for p in missing + changed:
                print("需同步:", p)
            print("检查未通过：%d 个缺失，%d 个已变更" % (len(missing), len(changed)))
            return 1
        print("检查通过：%d 个 .cir 与 HTML 代码块一致" % ok)
        return 0

    for target, code in sorted(found.items()):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(code, encoding="utf-8")

    all_cir = set((p.resolve() for p in ROOT.rglob("*.cir")))
    stale = sorted(all_cir - set(found))
    if args.clean:
        for p in stale:
            p.unlink()
            print("删除旧网表:", p.relative_to(ROOT))
    elif stale:
        for p in stale:
            print("提示：存在无对应代码块的旧网表", p.relative_to(ROOT))

    print("同步完成：共 %d 个网表，新建 %d，更新 %d，未变 %d" %
          (len(found), len(missing), len(changed), ok))
    return 0


if __name__ == "__main__":
    sys.exit(main())
