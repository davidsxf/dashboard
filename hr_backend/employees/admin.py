from django.contrib import admin
from .models import Employee, PoliticalStatus, PositionLevel, ProfessionalTitle, EducationLevel, DegreeLevel

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """员工模型的Admin配置"""
    list_display = ['employee_id', 'name', 'department', 'current_position', 'is_active', 'created_at']
    list_filter = ['department', 'is_active', 'political_status', 'professional_title']
    search_fields = ['employee_id', 'name', 'id_card_number', 'mobile_phone', 'email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'age']
    fieldsets = (
        ('基本信息', {
            'fields': ('employee_id', 'name', 'gender', 'department', 'team', 'nation', 'id_card_number', 'birthday', 'native_place', 'birth_place')
        }),
        ('政治面貌', {
            'fields': ('political_status', 'party_join_date', 'democratic_party', 'democratic_party_join_date')
        }),
        ('职务信息', {
            'fields': ('current_position', 'position_appointment_date', 'position_level')
        }),
        ('职称信息', {
            'fields': ('professional_title', 'title_appointment_date', 'technical_position', 'technical_position_start_date', 'special_appointment', 'special_appointment_start_date')
        }),
        ('教育背景', {
            'fields': ('full_time_school', 'full_time_major', 'full_time_education', 'full_time_degree', 'full_time_graduation_date',
                      'in_service_school', 'in_service_major', 'in_service_education', 'in_service_degree',
                      'highest_education', 'highest_degree', 'in_service_graduation_date')
        }),
        ('工作信息', {
            'fields': ('work_start_date', 'join_institute_date', 'institute_household')
        }),
        ('联系方式', {
            'fields': ('office_phone', 'mobile_phone', 'email')
        }),
        ('系统信息', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_at')
        })
    )

# 枚举类型不需要注册到admin，它们会作为模型字段的选择项自动显示
