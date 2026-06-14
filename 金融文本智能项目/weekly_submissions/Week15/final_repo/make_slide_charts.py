from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager, rcParams


OUT_DIR = Path(__file__).with_name("slides_assets")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsunb.ttf",
    r"C:\Windows\Fonts\Deng.ttf",
]


def configure_chinese_font() -> None:
    for font_path in FONT_CANDIDATES:
        path = Path(font_path)
        if path.exists():
            font_manager.fontManager.addfont(str(path))
            rcParams["font.family"] = path.stem
            rcParams["axes.unicode_minus"] = False
            return


def workflow_chart() -> None:
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.axis("off")

    labels = ["metadata", "audit", "parse", "route", "extract", "validate", "final result"]
    xs = [0.4, 2.0, 3.6, 5.2, 6.8, 8.4, 10.0]
    width = 1.3
    height = 0.8

    for x, label in zip(xs, labels):
        box = FancyBboxPatch(
            (x, 1.1),
            width,
            height,
            boxstyle="round,pad=0.03,rounding_size=0.08",
            linewidth=1.4,
            edgecolor="#1f4e79",
            facecolor="#eaf2fb",
        )
        ax.add_patch(box)
        ax.text(x + width / 2, 1.5, label, ha="center", va="center", fontsize=11, color="#103a5d")

    for i in range(len(xs) - 1):
        arrow = FancyArrowPatch(
            (xs[i] + width, 1.5),
            (xs[i + 1], 1.5),
            arrowstyle="->",
            mutation_scale=14,
            linewidth=1.4,
            color="#406c8f",
        )
        ax.add_patch(arrow)

    ax.text(6, 2.45, "Workflow: 从 metadata 到结构化结果", ha="center", fontsize=15, weight="bold", color="#163b5c")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "workflow_chart.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def demo_chain_chart() -> None:
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")

    steps = [
        ("PDF 公告", "原始证据"),
        ("metadata", "标题/日期/PDF路径"),
        ("parsed text", "解析后的文本"),
        ("section", "中标情况/风险提示"),
        ("JSON result", "字段 + evidence"),
        ("validated row", "最终结构化结果"),
    ]
    xs = [0.3, 2.2, 4.2, 6.2, 8.2, 10.1]
    width = 1.4
    height = 1.05

    for x, (title, sub) in zip(xs, steps):
        box = FancyBboxPatch(
            (x, 1.35),
            width,
            height,
            boxstyle="round,pad=0.04,rounding_size=0.08",
            linewidth=1.3,
            edgecolor="#7f4f24",
            facecolor="#fff1e6",
        )
        ax.add_patch(box)
        ax.text(x + width / 2, 2.0, title, ha="center", va="center", fontsize=11, weight="bold", color="#6b3d16")
        ax.text(x + width / 2, 1.62, sub, ha="center", va="center", fontsize=9.5, color="#8c5a2b")

    for i in range(len(xs) - 1):
        arrow = FancyArrowPatch(
            (xs[i] + width, 1.88),
            (xs[i + 1], 1.88),
            arrowstyle="->",
            mutation_scale=14,
            linewidth=1.4,
            color="#aa6c39",
        )
        ax.add_patch(arrow)

    ax.text(6, 3.2, "Demo 证据链：一条公告如何变成最终结果", ha="center", fontsize=15, weight="bold", color="#6b3d16")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "demo_chain_chart.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def evaluation_chart() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    metrics = ["metadata记录", "本地PDF", "缺失PDF", "重复doc_id"]
    values = [80, 80, 0, 0]
    colors = ["#2a9d8f", "#457b9d", "#e76f51", "#9d4edd"]
    axes[0].bar(metrics, values, color=colors)
    axes[0].set_title("Week 12 数据审计结果", fontsize=13)
    axes[0].set_ylabel("数量")
    axes[0].tick_params(axis="x", rotation=15)

    labels = ["字段可回证据", "金额需保留原文", "section仍需扩样本"]
    vals = [4, 1, 1]
    colors2 = ["#3a86ff", "#ff006e", "#8338ec"]
    axes[1].bar(labels, vals, color=colors2)
    axes[1].set_title("当前展示链主要观察", fontsize=13)
    axes[1].set_ylabel("条目数")
    axes[1].tick_params(axis="x", rotation=15)

    fig.suptitle("评估结果与当前局限", fontsize=16, weight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "evaluation_chart.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    configure_chinese_font()
    workflow_chart()
    demo_chain_chart()
    evaluation_chart()
    print(OUT_DIR)


if __name__ == "__main__":
    main()
