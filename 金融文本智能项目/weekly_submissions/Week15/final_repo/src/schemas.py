from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    field_name: Literal["project_name", "counterparty", "project_stage", "bid_amount_text", "risk_notice"]
    evidence_text: str
    page_no: Optional[int] = None
    confidence: float = Field(ge=0, le=1)


class BiddingAnnouncementExtract(BaseModel):
    doc_id: str
    company_name: str
    stock_code: str
    announcement_date: str
    project_name: Optional[str] = None
    counterparty: Optional[str] = None
    project_stage: Literal["预中标", "中标", "收到中标通知书", "签约进展", "其他"]
    bid_amount_text: Optional[str] = None
    risk_notice: Optional[str] = None
    evidence: list[Evidence]
