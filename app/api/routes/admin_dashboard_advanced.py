# app/api/routes/admin_dashboard_advanced.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta, date
from typing import List

from app.db.base import get_db
from app.db.models.user import User
from app.db.models.booking import Booking
from app.db.models.service import Service
from app.db.models.category import Category
from app.schemas.admin_dashboard_advanced import (
    AdminAdvancedResponse,
    ProviderGrowthPoint,
    MonthlyRevenuePoint,
    CategoryDistributionItem,
    LeaderboardItem,
    HeatmapPoint,
)
from app.core.security import get_current_user

router = APIRouter(prefix="/admin/dashboard/advanced", tags=["admin-dashboard-advanced"])

def require_admin(current_user: User):
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return True

@router.get("", response_model=AdminAdvancedResponse)
def admin_dashboard_advanced(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    now = datetime.utcnow()
    today = now.date()

    # Basic KPIs
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_providers = db.query(func.count(User.id)).filter(User.role == "provider").scalar() or 0
    total_services = db.query(func.count(Service.id)).scalar() or 0
    total_bookings = db.query(func.count(Booking.id)).scalar() or 0

    # 1) Provider growth last 30 days (group by day)
    start_30 = now - timedelta(days=29)
    raw = (
        db.query(
            func.date_trunc('day', User.created_at).label('day'),
            func.count(User.id).label('cnt')
        )
        .filter(User.role == "provider", User.created_at >= start_30)
        .group_by(func.date_trunc('day', User.created_at))
        .order_by(func.date_trunc('day', User.created_at))
        .all()
    )
    # map raw into day->count for 30-day window
    day_map = {r.day.date(): int(r.cnt) for r in raw}
    provider_growth = []
    for i in range(29, -1, -1):
        d = (now - timedelta(days=i)).date()
        provider_growth.append(ProviderGrowthPoint(date=datetime.combine(d, datetime.min.time()), new_providers=day_map.get(d, 0)))

    # 2) Monthly revenue last 12 months
    months = []
    for i in range(11, -1, -1):
        # compute month start by subtracting months - approximate by month arithmetic
        ref = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        months.append((ref.year, ref.month))
    monthly_revenue = []
    for y, m in months:
        start = datetime(y, m, 1)
        if m == 12:
            end = datetime(y+1, 1, 1)
        else:
            end = datetime(y, m+1, 1)
        total = db.query(func.coalesce(func.sum(Booking.amount), 0)).filter(
            Booking.status == "completed",
            Booking.created_at >= start,
            Booking.created_at < end
        ).scalar() or 0.0
        monthly_revenue.append(MonthlyRevenuePoint(year=y, month=m, total_earnings=float(total)))

    # 3) Category distribution - bookings count & earnings (top 10)
    cat_rows = (
        db.query(
            Service.category_id,
            func.count(Booking.id).label("bookings_count"),
            func.coalesce(func.sum(Booking.amount), 0).label("earnings")
        )
        .join(Booking, Booking.service_id == Service.id)
        .filter(Booking.status == "completed")
        .group_by(Service.category_id)
        .order_by(desc("bookings_count"))
        .limit(20)
        .all()
    )
    category_distribution = []
    for cat_id, cnt, earn in cat_rows:
        cat = db.query(Category).filter(Category.id == cat_id).first()
        category_distribution.append(CategoryDistributionItem(
            category_id=int(cat_id),
            category_name=cat.name if cat else None,
            bookings_count=int(cnt or 0),
            earnings=float(earn or 0.0)
        ))

    # 4) Provider leaderboard - hybrid score (rating * log(1 + rating_count) + normalized earnings)
    # Fetch top providers by completed earnings, then compute score
    prov_raw = (
        db.query(
            Booking.provider_id,
            func.coalesce(func.sum(Booking.amount), 0).label("earnings"),
            func.count(Booking.id).label("completed_count")
        )
        .filter(Booking.status == "completed")
        .group_by(Booking.provider_id)
        .order_by(desc("earnings"))
        .limit(50)
        .all()
    )
    leaderboard = []
    # compute max earnings for normalization
    max_earn = max([r.earnings for r in prov_raw], default=1)
    for provider_id, earnings, completed_count in prov_raw:
        prov = db.query(User).filter(User.id == provider_id).first()
        avg_rating = getattr(prov, "avg_rating", 0) or 0
        rating_count = getattr(prov, "rating_count", 0) or 0
        # hybrid score: weight rating and earnings
        # score = (avg_rating * log(1 + rating_count)) * 0.6 + (earnings / max_earn) * 0.4
        # avoid import math inside loop: import here
        import math
        rating_component = avg_rating * math.log(1 + rating_count)
        earnings_component = (earnings / max_earn) if max_earn > 0 else 0
        score = rating_component * 0.6 + earnings_component * 0.4
        leaderboard.append(LeaderboardItem(
            provider_id=int(provider_id),
            provider_name=prov.name if prov else None,
            avg_rating=float(avg_rating),
            rating_count=int(rating_count),
            total_earnings=float(earnings or 0.0),
            completed_bookings=int(completed_count or 0),
            score=float(score)
        ))
    # sort by score desc and take top 20
    leaderboard.sort(key=lambda x: x.score, reverse=True)
    leaderboard = leaderboard[:20]

    # 5) Bookings heatmap (weekday x hour) last 30 days
    # weekday: 1..7 using EXTRACT(isodow)
    heat_rows = (
        db.query(
            func.extract('isodow', Booking.created_at).label('weekday'),
            func.extract('hour', Booking.created_at).label('hour'),
            func.count(Booking.id).label('cnt')
        )
        .filter(Booking.created_at >= start_30)
        .group_by('weekday', 'hour')
        .all()
    )
    heatmap = []
    for weekday, hour, cnt in heat_rows:
        heatmap.append(HeatmapPoint(weekday=int(weekday), hour=int(hour), bookings=int(cnt)))

    # 6) Cancellation rate
    total_bookings_completed_or_canceled = db.query(func.count(Booking.id)).filter(Booking.status.in_(["completed","canceled"])).scalar() or 0
    canceled_count = db.query(func.count(Booking.id)).filter(Booking.status == "canceled").scalar() or 0
    cancellation_rate = (int(canceled_count) / int(total_bookings_completed_or_canceled) * 100.0) if total_bookings_completed_or_canceled > 0 else 0.0

    return AdminAdvancedResponse(
        total_users=int(total_users),
        total_providers=int(total_providers),
        total_services=int(total_services),
        total_bookings=int(total_bookings),
        provider_growth_last_30_days=provider_growth,
        monthly_revenue_last_12_months=monthly_revenue,
        category_distribution=category_distribution,
        provider_leaderboard=leaderboard,
        bookings_heatmap=heatmap,
        cancellation_rate_percent=float(round(cancellation_rate,2)),
    )
