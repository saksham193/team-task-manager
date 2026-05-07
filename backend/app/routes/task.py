from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Task, Team, TeamMember, TeamMemberRole, User
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(tags=["tasks"])


def _can_edit_task(task: Task, user: User, db: Session) -> bool:
    if task.created_by == user.id or task.assigned_to == user.id:
        return True
    if task.team.owner_id == user.id:
        return True
    admin_membership = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == task.team_id, TeamMember.user_id == user.id, TeamMember.role == TeamMemberRole.ADMIN)
        .first()
    )
    return admin_membership is not None


def _can_delete_task(task: Task, user: User, db: Session) -> bool:
    if task.created_by == user.id:
        return True
    if task.team.owner_id == user.id:
        return True
    return (
        db.query(TeamMember)
        .filter(TeamMember.team_id == task.team_id, TeamMember.user_id == user.id, TeamMember.role == TeamMemberRole.ADMIN)
        .first()
        is not None
    )


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    team = db.query(Team).filter(Team.id == task_data.team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    membership = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team.id, TeamMember.user_id == current_user.id)
        .first()
    )
    if membership is None and team.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only team members can create tasks")

    if task_data.assigned_to is not None:
        assignee_membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == team.id, TeamMember.user_id == task_data.assigned_to)
            .first()
        )
        if assignee_membership is None and task_data.assigned_to != team.owner_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned user must be a team member")

    task = Task(
        title=task_data.title.strip(),
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        assigned_to=task_data.assigned_to,
        team_id=task_data.team_id,
        created_by=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks", response_model=list[TaskResponse])
def get_assigned_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tasks = db.query(Task).filter(Task.assigned_to == current_user.id).all()
    return tasks


@router.get("/teams/{team_id}/tasks", response_model=list[TaskResponse])
def get_team_tasks(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    membership = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team.id, TeamMember.user_id == current_user.id)
        .first()
    )
    if membership is None and team.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only team members can view tasks")

    return db.query(Task).filter(Task.team_id == team_id).all()


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if not _can_edit_task(task, current_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission to update this task")

    if task_data.title is not None:
        task.title = task_data.title.strip()
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.assigned_to is not None:
        assignee_membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == task.team_id, TeamMember.user_id == task_data.assigned_to)
            .first()
        )
        if assignee_membership is None and task_data.assigned_to != task.team.owner_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned user must be a team member")
        task.assigned_to = task_data.assigned_to

    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if not _can_delete_task(task, current_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission to delete this task")

    db.delete(task)
    db.commit()
    return None
