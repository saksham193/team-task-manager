from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Task, Team, TeamMember
from app.schemas import DashboardStatsResponse, TaskResponse
from app.models import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    total_teams = db.query(Team).filter(Team.owner_id == current_user.id).count()
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    pending_tasks = db.query(Task).filter(Task.status == "todo").count()
    in_progress_tasks = db.query(Task).filter(Task.status == "in_progress").count()

    return DashboardStatsResponse(
        total_teams=total_teams,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
    )


@router.get("/recent-tasks", response_model=list[TaskResponse])
def get_recent_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    team_ids = (
        db.query(TeamMember.team_id)
        .filter(TeamMember.user_id == current_user.id)
        .subquery()
    )

    tasks = (
        db.query(Task)
        .filter(Task.team_id.in_(team_ids))
        .order_by(Task.created_at.desc())
        .limit(5)
        .all()
    )

    return tasks
