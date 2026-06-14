from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\simhei.ttf"),
    Path(r"C:\Windows\Fonts\simsunb.ttf"),
    Path(r"C:\Windows\Fonts\Deng.ttf"),
]

ASSET_DIR = Path(__file__).with_name("slides_assets")

SLIDES: list[dict] = [
    {
        "title": "项目题目与金融问题",
        "bullets": [
            "项目题目：上市公司中标公告关键信息抽取与项目台账生成。",
            "研究对象：巨潮资讯网上市公司披露的中标类公告，包括收到中标通知书、中标项目公告、重大经营合同中标公告。",
            "金融问题：中标公告反映公司新增订单、未来收入可见性、客户来源以及履约不确定性，是研究经营质量和订单获取能力的重要文本数据。",
            "项目目标：将项目名称、招标人、中标阶段、金额原文、风险提示等信息转成结构化字段，形成可追溯、可比较的事件台账。",
        ],
    },
    {
        "title": "巨潮数据来源",
        "bullets": [
            "数据入口：巨潮资讯网公开公告检索系统，不使用登录态，不绕过验证码或访问限制。",
            "关键词：关于收到中标通知书的公告、关于项目中标及收到中标通知书的公告、关于中标项目的公告、关于重大经营合同中标的公告。",
            "时间范围：2024-01-01 至 2026-05-29。",
            "样本规模：Week 12 已抓取 80 条真实 metadata，并成功下载 80 份对应 PDF，达到标准档 1.0 的下限。",
            "展示样本：答辩中重点展示 ST 交投 2025-04-12《关于收到中标通知书的公告》的完整证据链。",
        ],
    },
    {
        "title": "难度档位",
        "bullets": [
            "申请难度：标准档 1.0。",
            "理由 1：数据规模达到 80 份 PDF，已经满足课程给出的标准档最低数据量要求。",
            "理由 2：字段数量为 8 个核心字段，位于课程建议的 6-10 个字段区间。",
            "理由 3：除基础抓取外，还包含 section 检查、evidence 回填、Pydantic 校验、人工评估与错误分类。",
            "理由 4：中标公告虽然属于单主题任务，但不同公司在标题、金额表达和风险提示写法上差异较大，具有一定工程复杂度。",
        ],
    },
    {
        "title": "字段与 Schema",
        "bullets": [
            "核心字段：company_name、stock_code、announcement_date、project_name、counterparty、project_stage、bid_amount_text、risk_notice。",
            "字段类型设计：公司名、项目名、招标人为字符串；公告日期为标准日期；project_stage 为枚举值；金额字段当前保留原文表达。",
            "Null rule：如果公告中没有明确写出字段值，或者模型无法确定，就必须输出 null，不能根据常识编造。",
            "为什么要保留 bid_amount_text：中标公告中的“金额”不一定是人民币金额，有时是费率、比例或补偿方式，因此先保留原文更稳健。",
            "Evidence 结构：每个关键字段都回填 evidence_text 和 page_no，保证最后的结构化结果能回到原始 PDF 原文。",
        ],
    },
    {
        "title": "PDF 解析与 Section 检查",
        "bullets": [
            "PDF 解析目标：将公告 PDF 统一整理成可处理文本，便于后续的 section routing 和字段抽取。",
            "目标章节：重点定位“中标情况”“中标项目情况”“风险提示”等段落，而不是把整篇公告直接交给抽取器。",
            "Section routing 规则：通过关键词定位候选段落，例如“项目名称”“项目招标人”“风险提示”“尚未签署正式协议”等。",
            "Section checking：人工复核定位结果，防止规则误命中目录、释义、备查文件或其他无关位置。",
            "当前展示链中，project_name、counterparty、project_stage、bid_amount_text、risk_notice 都能在定位后的文本中找到对应证据。",
        ],
    },
    {
        "title": "Workflow",
        "bullets": [
            "整体流程是：metadata -> audit -> parse -> route -> extract -> validate -> final result。",
            "audit 阶段检查 metadata、重复记录、PDF 缺失和标题相关性，保证后续处理的数据基础可信。",
            "parse 阶段把 PDF 变成统一格式文本，route 阶段只截取与目标任务相关的段落，避免整篇公告噪声过多。",
            "extract 阶段输出结构化字段，validate 阶段再用 Pydantic 统一检查字段类型、枚举值和结果完整性。",
            "Workflow 的价值在于项目可以复现、可定位错误，也便于展示时解释每一步输入和输出。",
        ],
        "image": ASSET_DIR / "workflow_chart.png",
        "image_caption": "图：从 metadata 到 final result 的处理流程",
    },
    {
        "title": "Demo",
        "bullets": [
            "Demo 展示的是一条完整证据链，而不是单独展示 JSON 结果。",
            "展示顺序：原始 PDF -> metadata 记录 -> 解析文本 -> section 检查 -> 抽取 JSON -> Pydantic 校验 -> 最终结构化结果。",
            "最终结果展现了什么：我们把原本散落在公告正文中的项目信息整理成了可比字段，例如项目名称、招标人、中标阶段和风险提示。",
            "这意味着后续可以把多份公告放在同一张表中比较，而不是只能人工逐篇阅读公告。",
            "在答辩中，我们重点解释两个字段：project_name 和 risk_notice，说明它们各自对应哪一页、哪一段原文。",
        ],
        "image": ASSET_DIR / "demo_chain_chart.png",
        "image_caption": "图：一份公告如何转换为最终结构化结果",
    },
    {
        "title": "评估结果",
        "bullets": [
            "数据质量层面：Week 12 已完成 80 条 metadata 和 80 份 PDF，dataset check 报告显示本地缺失 PDF 数为 0，重复 doc_id 数为 0。",
            "字段效果层面：当前展示链中的 project_name、counterparty、project_stage、risk_notice 都能够回到原文 evidence。",
            "主要观察 1：系统已经可以稳定输出带 evidence 的结构化结果，而不是只有模型摘要。",
            "主要观察 2：金额字段目前适合保留原文，不适合强行统一成货币值，因为真实公告中经常出现比例、费率等表达。",
            "主要局限：当前解析和抽取部分仍以展示链路为主，若继续扩样本，需要进一步验证 section 规则和批量稳定性。",
        ],
        "image": ASSET_DIR / "evaluation_chart.png",
        "image_caption": "图：数据审计结果与当前展示链的主要观察",
    },
    {
        "title": "优化过程",
        "bullets": [
            "Prompt 优化：加入 null rule，并要求 evidence_text 必须来自输入原文，减少模型根据常识补全的风险。",
            "Schema 优化：将 project_stage 设为枚举值，把金额字段改成 bid_amount_text，避免把复杂金额表达误标准化。",
            "Section rules 优化：增加“中标情况”“风险提示”等定位词，并排除目录、备查文件等容易误命中的位置。",
            "Workflow 优化：补充 metadata 审计、下载状态检查和统一日志，让项目从分散脚本变成可复现流程。",
            "优化逻辑不是盲目换模型，而是根据错误来源分别修改 prompt、schema、section rules 和 workflow。",
        ],
    },
    {
        "title": "Vibe Coding 反思",
        "bullets": [
            "AI 帮助：生成抓取脚本、README、workflow、schema、slides 初稿和说明文档，提高了项目搭建速度。",
            "学生负责：定义金融问题、筛选巨潮样本、检查 PDF 与 metadata 的对应关系、核对 evidence 是否真实存在于原文中。",
            "我们没有把 AI 输出当作最终事实，而是要求关键字段能回到 PDF 原文，并用 Pydantic 做格式约束。",
            "本项目的经验是：受控 Vibe Coding 最关键的不是生成代码本身，而是学生能否验证、修正并解释这条证据链。",
        ],
    },
]


def register_chinese_font() -> str:
    for font_path in FONT_CANDIDATES:
        if font_path.exists():
            font_name = font_path.stem.replace(" ", "_")
            pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
            return font_name
    raise FileNotFoundError("No usable Chinese font found in C:\\Windows\\Fonts")


def draw_text_lines(
    pdf: canvas.Canvas,
    font_name: str,
    lines: list[str],
    x: float,
    y: float,
    max_width: float,
    font_size: int,
    line_gap: float,
) -> float:
    pdf.setFont(font_name, font_size)
    current_y = y
    for bullet in lines:
        wrapped = simpleSplit(f"- {bullet}", font_name, font_size, max_width)
        for line in wrapped:
            pdf.drawString(x, current_y, line)
            current_y -= line_gap
        current_y -= 6
    return current_y


def draw_slide(
    pdf: canvas.Canvas,
    font_name: str,
    slide_no: int,
    slide: dict,
) -> None:
    width, height = landscape(A4)
    left = 40
    top = height - 42

    pdf.setFillColor(HexColor("#111111"))
    pdf.setFont(font_name, 24)
    pdf.drawString(left, top, f"{slide_no}. {slide['title']}")

    pdf.setStrokeColor(HexColor("#d8d8d8"))
    pdf.line(left, top - 10, width - left, top - 10)

    has_image = slide.get("image") and Path(slide["image"]).exists()
    text_x = left + 4
    text_y = top - 40

    if has_image:
        text_width = width * 0.47
        image_x = width * 0.58
        image_y = 92
        image_w = width * 0.34
        image_h = height * 0.50
        draw_text_lines(pdf, font_name, slide["bullets"], text_x, text_y, text_width, 12, 18)
        pdf.drawImage(
            ImageReader(str(slide["image"])),
            image_x,
            image_y,
            width=image_w,
            height=image_h,
            preserveAspectRatio=True,
            mask="auto",
        )
        if slide.get("image_caption"):
            pdf.setFillColor(HexColor("#555555"))
            pdf.setFont(font_name, 10)
            pdf.drawCentredString(image_x + image_w / 2, image_y - 14, slide["image_caption"])
    else:
        text_width = width - left * 2 - 10
        draw_text_lines(pdf, font_name, slide["bullets"], text_x, text_y, text_width, 13, 20)

    pdf.setFillColor(HexColor("#666666"))
    pdf.setFont(font_name, 10)
    pdf.drawRightString(width - left, 20, "金融文本智能项目 Final Slides")


def main() -> None:
    font_name = register_chinese_font()
    output_path = Path(__file__).with_name("final_slides.pdf")
    pdf = canvas.Canvas(str(output_path), pagesize=landscape(A4))
    pdf.setTitle("final_slides")
    pdf.setAuthor("Codex")
    pdf.setSubject("金融文本智能项目展示材料")

    for idx, slide in enumerate(SLIDES, start=1):
        draw_slide(pdf, font_name, idx, slide)
        pdf.showPage()

    pdf.save()
    print(output_path)


if __name__ == "__main__":
    main()
