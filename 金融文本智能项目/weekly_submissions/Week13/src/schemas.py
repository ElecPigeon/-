from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    field_name: Literal["project_name", "counterparty", "project_stage", "bid_amount_text", "risk_notice"]
    evidence_text: str = Field(description="必须来自输入文本的原文片段")
    page_no: Optional[int] = Field(default=None, description="证据所在页码")
    confidence: float = Field(ge=0, le=1, description="抽取或判断置信度")


class BiddingAnnouncementExtract(BaseModel):
    doc_id: str
    company_name: str = Field(description="上市公司名称")
    stock_code: str = Field(description="证券代码")
    announcement_date: str = Field(description="公告日期，格式 YYYY-MM-DD")
    project_name: Optional[str] = Field(default=None, description="中标或收到通知书对应的项目名称")
    counterparty: Optional[str] = Field(default=None, description="招标人、交易对手方或发包人")
    project_stage: Literal["预中标", "中标", "收到中标通知书", "签约进展", "其他"]
    bid_amount_text: Optional[str] = Field(default=None, description="金额原文表达，不强制标准化")
    risk_notice: Optional[str] = Field(default=None, description="未签正式合同、履约不确定等风险提示")
    evidence: list[Evidence]
