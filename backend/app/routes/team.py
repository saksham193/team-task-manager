from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Team, TeamMember, TeamMemberRole, User
from app.schemas import TeamCreate, TeamMemberCreate, TeamMemberResponse, TeamResponse

router = APIRouter(prefix="/teams", tags=["teams"])


def _is_team_admin(team: Team, user: User) -> bool:
    if team.owner_id == user.id:
        return True
    return any(member.user_id == user.id and member.role == TeamMemberRole.ADMIN for member in team.members)


def _is_team_member(team: Team, user: User) -> bool:
    if team.owner_id == user.id:
        return True
    return any(member.user_id == user.id for member in team.members)


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    team = Team(
        name=team_data.name.strip(),
        description=team_data.description,
        owner_id=current_user.id,
    )
    db.add(team)
    db.commit()
    db.refresh(team)

    owner_membership = TeamMember(
        user_id=current_user.id,
        team_id=team.id,
        role=TeamMemberRole.ADMIN,
    )
    db.add(owner_membership)
    db.commit()

    return team


@router.get("/", response_model=list[TeamResponse])
def list_teams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    teams = (
        db.query(Team)
        .join(TeamMember, Team.id == TeamMember.team_id)
        .filter(
            (Team.owner_id == current_user.id)
            | (TeamMember.user_id == current_user.id)
        )
        .distinct()
        .all()
    )
    return teams


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if not _is_team_member(team, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return team


@router.post("/{team_id}/members", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED)
def add_team_member(
    team_id: int,
    member_data: TeamMemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    if not _is_team_admin(team, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only team owner or admin can add members")

    user = db.query(User).filter(User.id == member_data.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    existing = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == member_data.user_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a team member")

    role_value = (member_data.role or "member").lower()
    try:
        role = TeamMemberRole(role_value)
    except ValueError:
        role = TeamMemberRole.MEMBER

    membership = TeamMember(
        user_id=member_data.user_id,
        team_id=team_id,
        role=role,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get("/{team_id}/members", response_model=list[TeamMemberResponse])
def list_team_members(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if not _is_team_member(team, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return team.members
