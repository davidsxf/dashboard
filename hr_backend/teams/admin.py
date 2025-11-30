from django.contrib import admin
from .models import ResearchTeam

@admin.register(ResearchTeam)
class ResearchTeamAdmin(admin.ModelAdmin):
    """科研团队模型的Admin配置"""
    list_display = ['name', 'department', 'leader', 'member_count', 'created_at']
    list_filter = ['department']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at', 'member_count']
    fieldsets = (
        ('团队信息', {
            'fields': ('name', 'department', 'leader', 'description')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    def member_count(self, obj):
        """计算团队成员数量"""
        return obj.employee_set.count()
    
    member_count.short_description = '成员数量'
