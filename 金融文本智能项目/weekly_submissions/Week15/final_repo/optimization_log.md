# Optimization Log

## Round 1

- 问题：标题筛选过宽，可能混入合同进展类公告
- 调整：关键词保留“中标”“中标通知书”“重大经营合同中标”，并增加人工抽样确认

## Round 2

- 问题：金额字段不稳定，有些公告不披露明确金额
- 调整：将金额字段拆为 `bid_amount_text`，允许为 `null`

## Round 3

- 问题：section 可能命中目录或备查文件
- 调整：在 `section_rules.yaml` 中加入 `exclude_keywords` 和 `min_chars`

## Round 4

- 问题：模型输出阶段字段写法不统一
- 调整：把 `project_stage` 改为枚举值，统一为“预中标 / 中标 / 收到中标通知书 / 签约进展 / 其他”
