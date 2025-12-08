# app/schemas/admin_dashboard_advanced.py
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class ProviderGrowthPoint(BaseModel):
    date: datetime
    new_providers: int

class MonthlyRevenuePoint(BaseModel):
    year: int
    month: int
    total_earnings: float

class CategoryDistributionItem(BaseModel):
    category_id: int
    category_name: Optional[str]
    bookings_count: int
    earnings: float

class LeaderboardItem(BaseModel):
    provider_id: int
    provider_name: Optional[str]
    avg_rating: Optional[float]
    rating_count: int
    total_earnings: float
    completed_bookings: int
    score: float  # hybrid score used for ranking

class HeatmapPoint(BaseModel):
    weekday: int   # 1..7
    hour: int      # 0..23
    bookings: int

class AdminAdvancedResponse(BaseModel):
    # keep previous high-level KPIs block
    total_users: int
    total_providers: int
    total_services: int
    total_bookings: int

    provider_growth_last_30_days: List[ProviderGrowthPoint]
    monthly_revenue_last_12_months: List[MonthlyRevenuePoint]
    category_distribution: List[CategoryDistributionItem]
    provider_leaderboard: List[LeaderboardItem]
    bookings_heatmap: List[HeatmapPoint]
    cancellation_rate_percent: float

    class Config:
        from_attributes = True
