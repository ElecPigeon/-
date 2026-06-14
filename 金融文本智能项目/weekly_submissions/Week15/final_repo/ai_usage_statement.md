# AI Usage Statement

## 使用的 AI coding agent

Codex

## AI 帮助完成的内容

- 生成周次提交文件结构和多数说明文档初稿
- 编写抓取、下载、检查、workflow 入口脚本初稿
- 帮助整理 README、AGENTS、评估报告、demo script 和 slides 文案
- 根据选题生成 schema、section rules、prompt 和 evidence 结构初稿

## 学生人工完成的内容

- 确定选题和金融问题
- 检查公告是否真实来自巨潮
- 决定字段定义、难度档位和评估标准
- 运行脚本、检查输出、记录错误并修正
- 核对关键字段是否能回到原始 PDF 文本
- 决定哪些内容属于演示链路，哪些属于真实批量抓取结果

## 我们如何验证 AI 生成内容

- 人工检查 metadata、PDF 路径和公告标题是否匹配
- 人工检查 evidence_text 是否出现在输入文本中
- 查看 Pydantic 校验结果和 validation error
- 抽样检查 section 是否命中正文
- 对比 `metadata.csv`、`data/pdf/`、`dataset_check_report.md` 的记录数是否一致

## 发现过的 AI 错误

- 生成的字段说明过于宽泛，需要人工改成更明确的金融字段定义
- 某些默认示例会遗漏 null rule，需要人工补充
- workflow 初稿偏向展示成功路径，失败记录需要人工加上
- 初版 PDF 幻灯片使用的字体不兼容中文，重新嵌入系统字体后才修复乱码

## API Key 与数据合规说明

- API Key 只放在本地 `.env`
- 仓库中只保留 `.env.example`
- 项目只使用巨潮公开可访问数据
- 抓取过程中未绕过登录、验证码或访问限制
