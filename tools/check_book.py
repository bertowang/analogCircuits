#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全书自检：目录一致性、内部链接、代码块与 .cir 同步、SPICE 基本语法。

用法: python3 tools/check_book.py
退出码 0 表示全部通过；非 0 时逐条打印问题。
"""
from __future__ import annotations

import html as html_mod
import pathlib
import re
import sys
from html.parser import HTMLParser

VOID_TAGS = {"meta", "link", "br", "hr", "img", "input", "source", "area",
             "base", "col", "embed", "param", "track", "wbr"}


class TagBalance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            self.problems.append("标签交叉：期望 </%s>，实际 </%s>" % (self.stack[-1], tag))
            while self.stack and self.stack[-1] != tag:
                self.stack.pop()
            if self.stack:
                self.stack.pop()
        else:
            self.problems.append("多余的 </%s>" % tag)

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extract_netlists import BLOCK, collect  # noqa: E402

ANALYSES = {".op", ".dc", ".ac", ".tran", ".noise", ".tf", ".four"}
DOT_CMDS = ANALYSES | {
    ".step", ".param", ".meas", ".model", ".subckt", ".ends", ".include",
    ".lib", ".ic", ".options", ".save", ".func", ".temp", ".global", ".end",
}
SKIP_SCHEMES = ("http://", "https://", "mailto:", "data:", "#")

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def all_pages():
    return sorted(ROOT.rglob("*.html"))


# ---------- 1. toc.js 与页面文件 ----------
toc_text = (ROOT / "assets/toc.js").read_text(encoding="utf-8")
toc_paths = re.findall(r'path:\s*"([^"]+)"', toc_text)
toc_ids = re.findall(r'id:\s*"([^"]+)"\s*,\s*title:', toc_text)
if not toc_paths:
    err("assets/toc.js 中未解析到任何 path")
for p in toc_paths:
    if not (ROOT / p).is_file():
        err("toc.js 指向的页面不存在: " + p)
if len(set(toc_paths)) != len(toc_paths):
    err("toc.js 中存在重复 path")

index_text = (ROOT / "index.html").read_text(encoding="utf-8")
index_toc_links = re.findall(r'class="toc-title"\s+href="([^"]+)"', index_text)
for p in toc_paths:
    if p not in index_toc_links:
        err("总目录缺少章节链接: " + p)
for p in index_toc_links:
    if p not in toc_paths:
        err("总目录链接不在 toc.js 中: " + p)

# ---------- 2. 内部链接与资源 ----------
for page in all_pages():
    text = page.read_text(encoding="utf-8")
    rel_page = str(page.relative_to(ROOT))
    if 'class="site-foot"' not in text:
        err("缺少页脚: " + rel_page)
    for token in ("汪亮", "bertonwang", "47608843@qq.com", "AI 使用说明"):
        if token not in text:
            err("页脚缺少署名信息 [%s]: %s" % (token, rel_page))
    for attr in re.findall(r'(?:href|src)\s*=\s*(["\'])([^"\']+)\1', text):
        attr = attr[1]
        if attr.startswith(SKIP_SCHEMES):
            continue
        path_part = attr.split("#", 1)[0]
        if not path_part:
            continue
        target = (page.parent / path_part).resolve()
        if not target.exists():
            err("失效链接 %s -> %s" % (page.relative_to(ROOT), attr))
    if page.parent != ROOT:
        if "data-chapter=" not in text:
            err("章节页缺少 data-chapter: " + str(page.relative_to(ROOT)))
        if "</html>" not in text:
            err("HTML 未闭合: " + str(page.relative_to(ROOT)))
    parser = TagBalance()
    parser.feed(text)
    parser.close()
    for problem in parser.problems[:5]:
        err("HTML 标签 %s: %s" % (page.relative_to(ROOT), problem))
    if parser.stack:
        err("HTML 标签未闭合 %s: %s" % (page.relative_to(ROOT), ", ".join(parser.stack[:5])))

# ---------- 3. 代码块与 .cir 同步 ----------
found = collect()
if not found:
    err("没有抽取到任何 LTspice 代码块")
for target, code in sorted(found.items()):
    rel = str(target.relative_to(ROOT))
    if not target.exists():
        err("缺少网表文件（请运行 extract_netlists.py）: " + rel)
        continue
    if target.read_text(encoding="utf-8") != code:
        err("网表与 HTML 代码块不一致: " + rel)

# ---------- 4. SPICE 基本语法 ----------
for target in sorted(found):
    rel = str(target.relative_to(ROOT))
    lines = target.read_text(encoding="utf-8").splitlines()
    lines = [l.rstrip() for l in lines if l.strip()]
    if not lines:
        err("空网表: " + rel)
        continue
    if not lines[0].lstrip().startswith("*"):
        err("首行应为 * 开头的标题行: " + rel)
    if not any(l.lower().startswith(".end") for l in lines):
        err("缺少 .end: " + rel)
    if not any(l.lower().split()[0] in ANALYSES for l in lines if l.lower().split()):
        err("缺少分析指令(.op/.dc/.ac/.tran/.noise/.tf): " + rel)
    for n, line in enumerate(lines, 1):
        if any(ord(c) > 127 for c in line):
            err("网表含非 ASCII 字符（LTspice 注释请统一用英文）: %s:%d" % (rel, n))
            break
        s = line.lstrip()
        if s.startswith("*"):
            continue
        if s.startswith("."):
            cmd = s.split()[0].lower()
            if cmd not in DOT_CMDS:
                warn("未知点指令 %s（可能是 LTspice 扩展）: %s:%d" % (cmd, rel, n))
            continue
        parts = s.split()
        if len(parts) < 4:
            err("元件行字段不足: %s:%d -> %s" % (rel, n, s))
        if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", parts[0]):
            err("元件名不合法: %s:%d -> %s" % (rel, n, parts[0]))

# ---------- 5. 报告 ----------
for w in warnings:
    print("提示:", w)
for e in errors:
    print("错误:", e)
print("自检：%d 个 HTML 页面，%d 个章节，%d 个网表，%d 条错误，%d 条提示" %
      (len(all_pages()), len(toc_paths), len(found), len(errors), len(warnings)))
sys.exit(1 if errors else 0)
