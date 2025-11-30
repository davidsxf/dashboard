from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """部门模型的Admin配置"""
    list_display = ['name', 'parent_department', 'leader', 'employee_count', 'created_at']
    list_filter = ['parent_department']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at', 'employee_count']
    fieldsets = (
        ('部门信息', {
            'fields': ('name', 'parent_department', 'leader', 'description')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    def employee_count(self, obj):
        """计算部门员工数量"""
        return obj.employee_set.count()
    
    employee_count.short_description = '员工数量'
