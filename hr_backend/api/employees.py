from ninja import Router, Query
from typing import List, Optional
from pydantic import BaseModel
from employees.models import Employee, PoliticalStatus, PositionLevel, ProfessionalTitle, EducationLevel, DegreeLevel
from departments.models import Department
from teams.models import ResearchTeam
from django.db.models import Q

router = Router()

class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    gender: bool
    department_id: int
    team_id: Optional[int] = None
    nation: Optional[str] = None
    household_register: Optional[str] = None
    id_card_number: str
    birthday: Optional[str] = None
    native_place: Optional[str] = None
    birth_place: Optional[str] = None
    political_status: str = PoliticalStatus.MASSES
    party_join_date: Optional[str] = None
    democratic_party: bool = False
    democratic_party_join_date: Optional[str] = None
    current_position: Optional[str] = None
    position_appointment_date: Optional[str] = None
    position_level: Optional[str] = None
    professional_title: Optional[str] = None
    title_appointment_date: Optional[str] = None
    technical_position: Optional[str] = None
    technical_position_start_date: Optional[str] = None
    special_appointment: Optional[str] = None
    special_appointment_start_date: Optional[str] = None
    full_time_school: Optional[str] = None
    full_time_major: Optional[str] = None
    full_time_education: Optional[str] = None
    full_time_degree: str = DegreeLevel.NONE
    full_time_graduation_date: Optional[str] = None
    in_service_school: Optional[str] = None
    in_service_major: Optional[str] = None
    in_service_education: Optional[str] = None
    in_service_degree: str = DegreeLevel.NONE
    highest_education: Optional[str] = None
    highest_degree: str = DegreeLevel.NONE
    in_service_graduation_date: Optional[str] = None
    work_start_date: Optional[str] = None
    join_institute_date: Optional[str] = None
    institute_household: bool = False
    office_phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: int
    department_name: str
    team_name: Optional[str] = None
    created_at: str
    updated_at: str
    age: Optional[int] = None

    class Config:
        from_attributes = True

class EmployeeQuery(BaseModel):
    name: Optional[str] = None
    employee_id: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None
    page: int = 1
    page_size: int = 10


@router.get("/", response=List[EmployeeOut])
def list_employees(request, q: EmployeeQuery = Query(...)):
    """获取员工列表"""
    queryset = Employee.objects.all()
    
    # 过滤条件
    if q.name:
        queryset = queryset.filter(name__icontains=q.name)
    if q.employee_id:
        queryset = queryset.filter(employee_id__icontains=q.employee_id)
    if q.department_id:
        queryset = queryset.filter(department_id=q.department_id)
    if q.is_active is not None:
        queryset = queryset.filter(is_active=q.is_active)
    
    # 分页
    offset = (q.page - 1) * q.page_size
    employees = queryset[offset:offset + q.page_size]
    
    # 转换为响应格式
    result = []
    for emp in employees:
        result.append({
            **emp.__dict__,
            "department_name": emp.department.name,
            "team_name": emp.team.name if emp.team else None,
            "created_at": emp.created_at.isoformat(),
            "updated_at": emp.updated_at.isoformat(),
            "age": emp.age if emp.birthday else None
        })
    
    return result


@router.get("/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    """获取单个员工信息"""
    emp = Employee.objects.get(id=employee_id)
    return {
        **emp.__dict__,
        "department_name": emp.department.name,
        "team_name": emp.team.name if emp.team else None,
        "created_at": emp.created_at.isoformat(),
        "updated_at": emp.updated_at.isoformat(),
        "age": emp.age if emp.birthday else None
    }


@router.post("/", response=EmployeeOut)
def create_employee(request, data: EmployeeCreate):
    """创建员工"""
    department = Department.objects.get(id=data.department_id)
    team = ResearchTeam.objects.get(id=data.team_id) if data.team_id else None
    
    employee = Employee.objects.create(
        employee_id=data.employee_id,
        name=data.name,
        gender=data.gender,
        department=department,
        team=team,
        nation=data.nation,
        household_register=data.household_register,
        id_card_number=data.id_card_number,
        birthday=data.birthday,
        native_place=data.native_place,
        birth_place=data.birth_place,
        political_status=data.political_status,
        party_join_date=data.party_join_date,
        democratic_party=data.democratic_party,
        democratic_party_join_date=data.democratic_party_join_date,
        current_position=data.current_position,
        position_appointment_date=data.position_appointment_date,
        position_level=data.position_level,
        professional_title=data.professional_title,
        title_appointment_date=data.title_appointment_date,
        technical_position=data.technical_position,
        technical_position_start_date=data.technical_position_start_date,
        special_appointment=data.special_appointment,
        special_appointment_start_date=data.special_appointment_start_date,
        full_time_school=data.full_time_school,
        full_time_major=data.full_time_major,
        full_time_education=data.full_time_education,
        full_time_degree=data.full_time_degree,
        full_time_graduation_date=data.full_time_graduation_date,
        in_service_school=data.in_service_school,
        in_service_major=data.in_service_major,
        in_service_education=data.in_service_education,
        in_service_degree=data.in_service_degree,
        highest_education=data.highest_education,
        highest_degree=data.highest_degree,
        in_service_graduation_date=data.in_service_graduation_date,
        work_start_date=data.work_start_date,
        join_institute_date=data.join_institute_date,
        institute_household=data.institute_household,
        office_phone=data.office_phone,
        mobile_phone=data.mobile_phone,
        email=data.email,
        is_active=data.is_active,
        created_by=request.user
    )
    
    return {
        **employee.__dict__,
        "department_name": employee.department.name,
        "team_name": employee.team.name if employee.team else None,
        "created_at": employee.created_at.isoformat(),
        "updated_at": employee.updated_at.isoformat(),
        "age": employee.age if employee.birthday else None
    }


@router.put("/{employee_id}", response=EmployeeOut)
def update_employee(request, employee_id: int, data: EmployeeUpdate):
    """更新员工信息"""
    employee = Employee.objects.get(id=employee_id)
    department = Department.objects.get(id=data.department_id)
    team = ResearchTeam.objects.get(id=data.team_id) if data.team_id else None
    
    # 更新字段
    employee.employee_id = data.employee_id
    employee.name = data.name
    employee.gender = data.gender
    employee.department = department
    employee.team = team
    employee.nation = data.nation
    employee.household_register = data.household_register
    employee.id_card_number = data.id_card_number
    employee.birthday = data.birthday
    employee.native_place = data.native_place
    employee.birth_place = data.birth_place
    employee.political_status = data.political_status
    employee.party_join_date = data.party_join_date
    employee.democratic_party = data.democratic_party
    employee.democratic_party_join_date = data.democratic_party_join_date
    employee.current_position = data.current_position
    employee.position_appointment_date = data.position_appointment_date
    employee.position_level = data.position_level
    employee.professional_title = data.professional_title
    employee.title_appointment_date = data.title_appointment_date
    employee.technical_position = data.technical_position
    employee.technical_position_start_date = data.technical_position_start_date
    employee.special_appointment = data.special_appointment
    employee.special_appointment_start_date = data.special_appointment_start_date
    employee.full_time_school = data.full_time_school
    employee.full_time_major = data.full_time_major
    employee.full_time_education = data.full_time_education
    employee.full_time_degree = data.full_time_degree
    employee.full_time_graduation_date = data.full_time_graduation_date
    employee.in_service_school = data.in_service_school
    employee.in_service_major = data.in_service_major
    employee.in_service_education = data.in_service_education
    employee.in_service_degree = data.in_service_degree
    employee.highest_education = data.highest_education
    employee.highest_degree = data.highest_degree
    employee.in_service_graduation_date = data.in_service_graduation_date
    employee.work_start_date = data.work_start_date
    employee.join_institute_date = data.join_institute_date
    employee.institute_household = data.institute_household
    employee.office_phone = data.office_phone
    employee.mobile_phone = data.mobile_phone
    employee.email = data.email
    employee.is_active = data.is_active
    
    employee.save()
    
    return {
        **employee.__dict__,
        "department_name": employee.department.name,
        "team_name": employee.team.name if employee.team else None,
        "created_at": employee.created_at.isoformat(),
        "updated_at": employee.updated_at.isoformat(),
        "age": employee.age if employee.birthday else None
    }


@router.delete("/{employee_id}")
def delete_employee(request, employee_id: int):
    """删除员工"""
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return {"detail": "员工删除成功"}
