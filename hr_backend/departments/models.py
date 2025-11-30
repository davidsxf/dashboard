from django.db import models

class Department(models.Model):
    """部门信息"""
    name = models.CharField(max_length=100, verbose_name='部门名称')
    parent_department = models.ForeignKey('self', on_delete=models.CASCADE, 
                                         null=True, blank=True, verbose_name="上级部门")
                                         
    leader = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='leading_departments', verbose_name='部门负责人')
    description = models.TextField(blank=True, verbose_name='部门描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门管理'
    
    def __str__(self):
        return self.name
