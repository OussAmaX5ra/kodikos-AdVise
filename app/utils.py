"""
Utility functions for metrics calculations and formatting.
"""
from typing import List, Dict, Any
from app.models import MetricSnapshot


def calculate_ctr(clicks: int, impressions: int) -> float:
    """
    Calculate click-through rate (CTR).

    Args:
        clicks: Number of clicks
        impressions: Number of impressions

    Returns:
        CTR as a percentage (0-100)
    """
    if impressions == 0:
        return 0.0
    return round((clicks / impressions) * 100, 2)


def calculate_roas(revenue: float, spend: float) -> float:
    """
    Calculate return on ad spend (ROAS).

    Args:
        revenue: Total revenue
        spend: Total ad spend

    Returns:
        ROAS as a ratio (e.g., 4.5 means $4.50 revenue per $1 spent)
    """
    if spend == 0:
        return 0.0
    return round(revenue / spend, 2)


def enrich_metric_with_computed_fields(metric: MetricSnapshot) -> Dict[str, Any]:
    """
    Add computed fields (CTR, ROAS) to a metric snapshot.

    Args:
        metric: MetricSnapshot object

    Returns:
        Dictionary with all fields including computed ones
    """
    return {
        "id": metric.id,
        "account_id": metric.account_id,
        "ts": metric.ts,
        "spend": metric.spend,
        "impressions": metric.impressions,
        "clicks": metric.clicks,
        "conversions": metric.conversions,
        "revenue": metric.revenue,
        "ctr": calculate_ctr(metric.clicks, metric.impressions),
        "roas": calculate_roas(metric.revenue, metric.spend),
    }


def format_metrics_summary(metrics: List[MetricSnapshot]) -> str:
    """
    Format metrics list into a concise text summary for LLM context.

    Args:
        metrics: List of MetricSnapshot objects (newest first)

    Returns:
        Formatted string summary
    """
    if not metrics:
        return "No metrics available."

    # Calculate aggregates
    total_spend = sum(m.spend for m in metrics)
    total_impressions = sum(m.impressions for m in metrics)
    total_clicks = sum(m.clicks for m in metrics)
    total_conversions = sum(m.conversions for m in metrics)
    total_revenue = sum(m.revenue for m in metrics)

    avg_ctr = calculate_ctr(total_clicks, total_impressions)
    avg_roas = calculate_roas(total_revenue, total_spend)

    summary = f"""Metrics Summary (last {len(metrics)} days):
- Total Spend: ${total_spend:,.2f}
- Total Impressions: {total_impressions:,}
- Total Clicks: {total_clicks:,}
- Total Conversions: {total_conversions:,}
- Total Revenue: ${total_revenue:,.2f}
- Average CTR: {avg_ctr}%
- Average ROAS: {avg_roas}x

Recent daily trends (last 3 days):"""

    for metric in metrics[:3]:
        ctr = calculate_ctr(metric.clicks, metric.impressions)
        roas = calculate_roas(metric.revenue, metric.spend)
        summary += f"\n  {metric.ts}: Spend ${metric.spend:.2f}, CTR {ctr}%, ROAS {roas}x, Conv {metric.conversions}"

    return summary


