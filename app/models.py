from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float, Date, Index
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    facebook_accounts = relationship("FacebookAccount", back_populates="user")


class FacebookAccount(Base):
    __tablename__ = "facebook_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    ad_account_id = Column(String(50), nullable=False, index=True)  # e.g., act_123456789
    access_token = Column(Text, nullable=False)  # TODO: Encrypt in production
    token_type = Column(String(50), default="Bearer", nullable=False)
    expires_at = Column(DateTime, nullable=True)  # UTC datetime when token expires
    is_system_user = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="facebook_accounts")
    metric_snapshots = relationship("MetricSnapshot", back_populates="facebook_account")

    __table_args__ = (
        Index("idx_user_ad_account", "user_id", "ad_account_id"),
    )


class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    facebook_account_id = Column(Integer, ForeignKey("facebook_accounts.id"), nullable=False, index=True)
    ts = Column(Date, nullable=False, index=True)  # Date of the metric
    level = Column(String(20), nullable=False, index=True)  # account, campaign, adset, ad
    entity_id = Column(String(50), nullable=False, index=True)  # ID of the entity (campaign_id, adset_id, etc.)
    impressions = Column(Integer, default=0, nullable=False)
    clicks = Column(Integer, default=0, nullable=False)
    spend = Column(Float, default=0.0, nullable=False)
    conversions = Column(Integer, default=0, nullable=False)
    revenue = Column(Float, default=0.0, nullable=False)
    raw = Column(Text, nullable=True)  # JSON string of raw Graph API response
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    facebook_account = relationship("FacebookAccount", back_populates="metric_snapshots")

    __table_args__ = (
        Index("idx_unique_metric", "facebook_account_id", "ts", "entity_id", "level", unique=True),
        Index("idx_ts_level", "ts", "level"),
    )