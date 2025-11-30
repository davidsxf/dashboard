from django.db import models

class ResearchTeam(models.Model):
    """科研创新团队"""
    name = models.CharField(max_length=100, verbose_name='团队名称')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, verbose_name='所属部门')
    leader = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='leading_teams', verbose_name='团队负责人')
    description = models.TextField(blank=True, verbose_name='团队描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '科研创新团队'
        verbose_name_plural = '科研创新团队管理'
    
    def __str__(self):
        return self.name
