from ninja import Router, Query
from typing import List, Optional
from pydantic import BaseModel
from departments.models import Department
from employees.models import Employee

router = Router()

class DepartmentBase(BaseModel):
    name: str
    parent_department_id: Optional[int] = None
    leader_id: Optional[int] = None
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int
    parent_department_name: Optional[str] = None
    leader_name: Optional[str] = None
    created_at: str
    updated_at: str
    employee_count: int = 0

    class Config:
        from_attributes = True

class DepartmentQuery(BaseModel):
    name: Optional[str] = None
    page: int = 1
    page_size: int = 10


@router.get("/", response=List[DepartmentOut])
def list_departments(request, q: DepartmentQuery = Query(...)):
    """获取部门列表"""
    queryset = Department.objects.all()
    
    # 过滤条件
    if q.name:
        queryset = queryset.filter(name__icontains=q.name)
    
    # 分页
    offset = (q.page - 1) * q.page_size
    departments = queryset[offset:offset + q.page_size]
    
    # 转换为响应格式
    result = []
    for dept in departments:
        result.append({
            "id": dept.id,
            "name": dept.name,
            "parent_department_id": dept.parent_department.id if dept.parent_department else None,
            "parent_department_name": dept.parent_department.name if dept.parent_department else None,
            "leader_id": dept.leader.id if dept.leader else None,
            "leader_name": dept.leader.name if dept.leader else None,
            "description": dept.description,
            "created_at": dept.created_at.isoformat(),
            "updated_at": dept.updated_at.isoformat(),
            "employee_count": dept.employee_set.count()
        })
    
    return result


@router.get("/{department_id}", response=DepartmentOut)
def get_department(request, department_id: int):
    """获取单个部门信息"""
    dept = Department.objects.get(id=department_id)
    return {
        "id": dept.id,
        "name": dept.name,
        "parent_department_id": dept.parent_department.id if dept.parent_department else None,
        "parent_department_name": dept.parent_department.name if dept.parent_department else None,
        "leader_id": dept.leader.id if dept.leader else None,
        "leader_name": dept.leader.name if dept.leader else None,
        "description": dept.description,
        "created_at": dept.created_at.isoformat(),
        "updated_at": dept.updated_at.isoformat(),
        "employee_count": dept.employee_set.count()
    }


@router.post("/", response=DepartmentOut)
def create_department(request, data: DepartmentCreate):
    """创建部门"""
    parent_department = Department.objects.get(id=data.parent_department_id) if data.parent_department_id else None
    leader = Employee.objects.get(id=data.leader_id) if data.leader_id else None
    
    department = Department.objects.create(
        name=data.name,
        parent_department=parent_department,
        leader=leader,
        description=data.description
    )
    
    return {
        "id": department.id,
        "name": department.name,
        "parent_department_id": department.parent_department.id if department.parent_department else None,
        "parent_department_name": department.parent_department.name if department.parent_department else None,
        "leader_id": department.leader.id if department.leader else None,
        "leader_name": department.leader.name if department.leader else None,
        "description": department.description,
        "created_at": department.created_at.isoformat(),
        "updated_at": department.updated_at.isoformat(),
        "employee_count": 0
    }


@router.put("/{department_id}", response=DepartmentOut)
def update_department(request, department_id: int, data: DepartmentUpdate):
    """更新部门信息"""
    department = Department.objects.get(id=department_id)
    parent_department = Department.objects.get(id=data.parent_department_id) if data.parent_department_id else None
    leader = Employee.objects.get(id=data.leader_id) if data.leader_id else None
    
    # 更新字段
    department.name = data.name
    department.parent_department = parent_department
    department.leader = leader
    department.description = data.description
    
    department.save()
    
    return {
        "id": department.id,
        "name": department.name,
        "parent_department_id": department.parent_department.id if department.parent_department else None,
        "parent_department_name": department.parent_department.name if department.parent_department else None,
        "leader_id": department.leader.id if department.leader else None,
        "leader_name": department.leader.name if department.leader else None,
        "description": department.description,
        "created_at": department.created_at.isoformat(),
        "updated_at": department.updated_at.isoformat(),
        "employee_count": department.employee_set.count()
    }


@router.delete("/{department_id}")
def delete_department(request, department_id: int):
    """删除部门"""
    department = Department.objects.get(id=department_id)
    department.delete()
    return {"detail": "部门删除成功"}


@router.get("/tree")
def get_department_tree(request):
    """获取部门树状结构"""
    def build_tree(departments, parent_id=None):
        """递归构建部门树"""
        tree = []
        for dept in departments:
            if dept.parent_department_id == parent_id:
                children = build_tree(departments, dept.id)
                node = {
                    "id": dept.id,
                    "name": dept.name,
                    "leader_id": dept.leader_id,
                    "leader_name": dept.leader.name if dept.leader else None,
                    "employee_count": dept.employee_set.count(),
                    "children": children
                }
                tree.append(node)
        return tree
    
    departments = Department.objects.all()
    return build_tree(departments)
