from django.db import models
from django.contrib.auth.models import User

# 政治面貌枚举
class PoliticalStatus(models.TextChoices):
    PARTY_MEMBER = 'party_member', '中共党员'
    DEMOCRATIC_PARTY = 'democratic_party', '民主党派'
    MASSES = 'masses', '群众'
    OTHER = 'other', '其他'

# 职务级别枚举
class PositionLevel(models.TextChoices):
    LEVEL_4 = 'level_1', '副局级'
    LEVEL_5 = 'level_2', '正处级'
    LEVEL_6 = 'level_3', '副处级'
    LEVEL_7 = 'level_4', '正科级'
    LEVEL_8 = 'level_5', '副科级'
    LEVEL_9 = 'level_6', '科员'
    OTHER = 'other', '其他'

# 职称枚举
class ProfessionalTitle(models.TextChoices):
    SENIOR_RESEARCHER = 'senior_researcher', '研究员（正高级）'
    ASSOCIATE_RESEARCHER = 'associate_researcher', '副研究员（副高级）'
    RESEARCH_ASSISTANT = 'research_assistant', '助理研究员（中级）'
    RESEARCH_INTERN = 'research_intern', '研究实习员（初级）'
    OTHER = 'other', '其他'

# 学历枚举
class EducationLevel(models.TextChoices):
    DOCTOR = 'doctor', '博士研究生'
    MASTER = 'master', '硕士研究生'
    BACHELOR = 'bachelor', '本科'
    JUNIOR_COLLEGE = 'junior_college', '专科'
    HIGH_SCHOOL = 'high_school', '高中'
    OTHER = 'other', '其他'

# 学位枚举
class DegreeLevel(models.TextChoices):
    DOCTORATE = 'doctorate', '博士'
    MASTER = 'master', '硕士'
    BACHELOR = 'bachelor', '学士'
    OTHER = 'other', '其他'
    NONE = 'none', '无'

class Employee(models.Model):
    """员工基本信息"""
    # 基本信息
    employee_id = models.CharField(max_length=20, unique=True, verbose_name='员工编号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, verbose_name='所在部门')
    team = models.ForeignKey('teams.ResearchTeam', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属科研创新团队')
    gender = models.BooleanField(choices=((True, '男'), (False, '女')), verbose_name='性别')
    nation = models.CharField(max_length=20, blank=True, verbose_name='民族')
    household_register = models.CharField(max_length=100, blank=True,null=True, verbose_name='户籍所在地')
    id_card_number = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    birthday = models.DateField(verbose_name='出生日期', null=True, blank=True)
    native_place = models.CharField(max_length=100, blank=True, null=True, verbose_name='籍贯')
    birth_place = models.CharField(max_length=100, blank=True, null=True, verbose_name='出生地')
    
    # 政治面貌
    political_status = models.CharField(max_length=20, choices=PoliticalStatus.choices, default=PoliticalStatus.MASSES, verbose_name='政治面貌')
    party_join_date = models.DateField(null=True, blank=True, verbose_name='入党时间')
    democratic_party = models.BooleanField(default=False, verbose_name='是否民主党派')
    democratic_party_join_date = models.DateField(null=True, blank=True, verbose_name='加入民主党派时间')
    
    # 职务信息
    current_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='现任管理职务')
    position_appointment_date = models.DateField(null=True, blank=True, verbose_name='任现职务时间')
    position_level = models.CharField(max_length=20, choices=PositionLevel.choices, blank=True, null=True, verbose_name='现任职务级别')
    
    
    # 职称信息
    professional_title = models.CharField(max_length=20, choices=ProfessionalTitle.choices, blank=True, null=True, verbose_name='职称')
    title_appointment_date = models.DateField(null=True, blank=True, verbose_name='职称定职时间')
    technical_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='现聘专技岗位')
    technical_position_start_date = models.DateField(null=True, blank=True, verbose_name='专技岗起聘时间')
    special_appointment = models.CharField(max_length=100, blank=True, null=True, verbose_name='特聘岗位')
    special_appointment_start_date = models.DateField(null=True, blank=True, verbose_name='特聘岗位起聘时间')
    
    # 全日制教育
    full_time_school = models.CharField(max_length=100, blank=True, null=True, verbose_name='全日制毕业院校')
    full_time_major = models.CharField(max_length=100, blank=True, null=True, verbose_name='全日制所学专业')
    full_time_education = models.CharField(max_length=20, choices=EducationLevel.choices, blank=True, null=True, verbose_name='全日制最高学历')
    full_time_degree = models.CharField(max_length=20, choices=DegreeLevel.choices, default=DegreeLevel.NONE, null=True, blank=True, verbose_name='全日制最后学位')
    full_time_graduation_date = models.DateField(null=True, blank=True, verbose_name='全日制毕业（获学位）时间')
    
    # 在职教育
    in_service_school = models.CharField(max_length=100, blank=True, null=True, verbose_name='在职学习毕业院校')
    in_service_major = models.CharField(max_length=100, blank=True, null=True, verbose_name='在职学习所学专业')
    in_service_education = models.CharField(max_length=20, choices=EducationLevel.choices, blank=True, null=True, verbose_name='在职学习所获学历')
    in_service_degree = models.CharField(max_length=20, choices=DegreeLevel.choices, default=DegreeLevel.NONE, null=True, blank=True, verbose_name='在职学习所获学位')
    highest_education = models.CharField(max_length=20, choices=EducationLevel.choices, blank=True, null=True, verbose_name='最高学历')
    highest_degree = models.CharField(max_length=20, choices=DegreeLevel.choices, default=DegreeLevel.NONE, null=True, blank=True, verbose_name='最高学位')
    in_service_graduation_date = models.DateField(null=True, blank=True, verbose_name='在职学习毕业（获学位）时间')
    
    # 工作信息
    work_start_date = models.DateField(verbose_name='参加工作时间', null=True, blank=True)
    join_institute_date = models.DateField(verbose_name='入所编制时间', null=True, blank=True)
    institute_household = models.BooleanField(default=False, verbose_name='是否所集户户口')
    
    # 联系方式
    office_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='办公电话')
    mobile_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='电子邮箱')
    
    # 系统信息
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_employees', verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否在职')
    
    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工管理'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.employee_id} - {self.name}'
    
    @property
    def age(self):
        """计算年龄"""
        from datetime import date
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
