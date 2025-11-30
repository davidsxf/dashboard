from ninja import Router, Query
from typing import List, Optional
from pydantic import BaseModel
from teams.models import ResearchTeam
from departments.models import Department
from employees.models import Employee

router = Router()

class TeamBase(BaseModel):
    name: str
    department_id: int
    leader_id: Optional[int] = None
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    pass

class TeamOut(TeamBase):
    id: int
    department_name: str
    leader_name: Optional[str] = None
    created_at: str
    updated_at: str
    employee_count: int = 0

    class Config:
        from_attributes = True

class TeamQuery(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None
    page: int = 1
    page_size: int = 10


@router.get("/", response=List[TeamOut])
def list_teams(request, q: TeamQuery = Query(...)):
    """获取科研团队列表"""
    queryset = ResearchTeam.objects.all()
    
    # 过滤条件
    if q.name:
        queryset = queryset.filter(name__icontains=q.name)
    if q.department_id:
        queryset = queryset.filter(department_id=q.department_id)
    
    # 分页
    offset = (q.page - 1) * q.page_size
    teams = queryset[offset:offset + q.page_size]
    
    # 转换为响应格式
    result = []
    for team in teams:
        result.append({
            "id": team.id,
            "name": team.name,
            "department_id": team.department.id,
            "department_name": team.department.name,
            "leader_id": team.leader.id if team.leader else None,
            "leader_name": team.leader.name if team.leader else None,
            "description": team.description,
            "created_at": team.created_at.isoformat(),
            "updated_at": team.updated_at.isoformat(),
            "employee_count": team.employee_set.count()
        })
    
    return result


@router.get("/{team_id}", response=TeamOut)
def get_team(request, team_id: int):
    """获取单个科研团队信息"""
    team = ResearchTeam.objects.get(id=team_id)
    return {
        "id": team.id,
        "name": team.name,
        "department_id": team.department.id,
        "department_name": team.department.name,
        "leader_id": team.leader.id if team.leader else None,
        "leader_name": team.leader.name if team.leader else None,
        "description": team.description,
        "created_at": team.created_at.isoformat(),
        "updated_at": team.updated_at.isoformat(),
        "employee_count": team.employee_set.count()
    }


@router.post("/", response=TeamOut)
def create_team(request, data: TeamCreate):
    """创建科研团队"""
    department = Department.objects.get(id=data.department_id)
    leader = Employee.objects.get(id=data.leader_id) if data.leader_id else None
    
    team = ResearchTeam.objects.create(
        name=data.name,
        department=department,
        leader=leader,
        description=data.description
    )
    
    return {
        "id": team.id,
        "name": team.name,
        "department_id": team.department.id,
        "department_name": team.department.name,
        "leader_id": team.leader.id if team.leader else None,
        "leader_name": team.leader.name if team.leader else None,
        "description": team.description,
        "created_at": team.created_at.isoformat(),
        "updated_at": team.updated_at.isoformat(),
        "employee_count": 0
    }


@router.put("/{team_id}", response=TeamOut)
def update_team(request, team_id: int, data: TeamUpdate):
    """更新科研团队信息"""
    team = ResearchTeam.objects.get(id=team_id)
    department = Department.objects.get(id=data.department_id)
    leader = Employee.objects.get(id=data.leader_id) if data.leader_id else None
    
    # 更新字段
    team.name = data.name
    team.department = department
    team.leader = leader
    team.description = data.description
    
    team.save()
    
    return {
        "id": team.id,
        "name": team.name,
        "department_id": team.department.id,
        "department_name": team.department.name,
        "leader_id": team.leader.id if team.leader else None,
        "leader_name": team.leader.name if team.leader else None,
        "description": team.description,
        "created_at": team.created_at.isoformat(),
        "updated_at": team.updated_at.isoformat(),
        "employee_count": team.employee_set.count()
    }


@router.delete("/{team_id}")
def delete_team(request, team_id: int):
    """删除科研团队"""
    team = ResearchTeam.objects.get(id=team_id)
    team.delete()
    return {"detail": "科研团队删除成功"}
