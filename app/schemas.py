from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ============ Auth Schemas ============
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============ Facebook Schemas ============
class FacebookAccountResponse(BaseModel):
    id: int
    ad_account_id: str
    token_type: str
    expires_at: Optional[datetime]
    is_system_user: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SystemUserTokenRequest(BaseModel):
    ad_account_id: str = Field(..., pattern=r"^act_\d+$")
    access_token: str


class FetchInsightsResponse(BaseModel):
    rows_ingested: int
    rows_skipped: int
    next_cursor: Optional[str] = None
    status: str = "success"


class MetricSnapshotResponse(BaseModel):
    id: int
    ts: date
    level: str
    entity_id: str
    impressions: int
    clicks: int
    spend: float
    conversions: int
    revenue: float
    ctr: float = 0.0  # Computed: (clicks / impressions) * 100
    roas: float = 0.0  # Computed: revenue / spend
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_computed(cls, obj):
        """Populate computed fields."""
        ctr = (obj.clicks / obj.impressions * 100) if obj.impressions > 0 else 0.0
        roas = (obj.revenue / obj.spend) if obj.spend > 0 else 0.0
        return cls(
            id=obj.id,
            ts=obj.ts,
            level=obj.level,
            entity_id=obj.entity_id,
            impressions=obj.impressions,
            clicks=obj.clicks,
            spend=obj.spend,
            conversions=obj.conversions,
            revenue=obj.revenue,
            ctr=round(ctr, 2),
            roas=round(roas, 2),
            created_at=obj.created_at,
        )


class MetricSnapshotListResponse(BaseModel):
    items: List[MetricSnapshotResponse]
    total: int
    page: int
    limit: int