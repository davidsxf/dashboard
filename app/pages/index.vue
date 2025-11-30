<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'
import { useEmployees } from '~/composables/useEmployees'
import { useDepartments } from '~/composables/useDepartments'
import { useTeams } from '~/composables/useTeams'

const { isNotificationsSlideoverOpen } = useDashboard()
const { employees } = useEmployees()
const { departments } = useDepartments()
const { teams } = useTeams()

// 操作菜单
const items = [[{
  label: '添加员工',
  icon: 'i-lucide-user-plus',
  to: '/employees'
}, {
  label: '添加部门',
  icon: 'i-lucide-building',
  to: '/departments'
}, {
  label: '添加科研团队',
  icon: 'i-lucide-users-round',
  to: '/teams'
}]] satisfies DropdownMenuItem[][]
</script>

<template>
  <UDashboardPanel id="home">
    <template #header>
      <UDashboardNavbar title="人事管理系统" :ui="{ right: 'gap-3' }">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UTooltip text="通知" :shortcuts="['N']">
            <UButton
              color="neutral"
              variant="ghost"
              square
              @click="isNotificationsSlideoverOpen = true"
            >
              <UChip color="error" inset>
                <UIcon name="i-lucide-bell" class="size-5 shrink-0" />
              </UChip>
            </UButton>
          </UTooltip>

          <UDropdownMenu :items="items">
            <UButton icon="i-lucide-plus" size="md" class="rounded-full" />
          </UDropdownMenu>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <UCard v-for="stat in [
          { title: '员工总数', value: employees.length, icon: 'i-lucide-users', color: 'primary' },
          { title: '部门数量', value: departments.length, icon: 'i-lucide-building', color: 'secondary' },
          { title: '科研团队', value: teams.length, icon: 'i-lucide-users-round', color: 'tertiary' },
          { title: '在职员工', value: employees.filter(emp => emp.is_active).length, icon: 'i-lucide-check-circle', color: 'success' }
        ]" :key="stat.title">
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ stat.title }}</h3>
              <UIcon :name="stat.icon" class="size-5 text-gray-400 dark:text-gray-500" />
            </div>
          </template>
          <div class="text-3xl font-bold text-gray-900 dark:text-white">{{ stat.value }}</div>
        </UCard>
      </div>

      <!-- 主要内容区域 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 最近添加的员工 -->
        <div class="lg:col-span-2">
          <UCard>
            <template #header>
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-semibold">最近添加的员工</h3>
                <UButton size="sm" variant="ghost" to="/employees">
                  查看全部
                  <UIcon name="i-lucide-arrow-right" class="ml-1 size-4" />
                </UButton>
              </div>
            </template>
            <table class="w-full">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">姓名</th>
                  <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">部门</th>
                  <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">职位</th>
                  <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">入职日期</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="emp in employees.slice(0, 5)" :key="emp.id" class="border-b hover:bg-gray-50 dark:hover:bg-gray-800">
                  <td class="py-3 px-4 text-sm font-medium text-gray-900 dark:text-white">{{ emp.name }}</td>
                  <td class="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">{{ emp.department_name }}</td>
                  <td class="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">{{ emp.current_position || '-' }}</td>
                  <td class="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">{{ emp.join_institute_date }}</td>
                </tr>
              </tbody>
            </table>
          </UCard>
        </div>

        <!-- 部门分布 -->
        <div>
          <UCard>
            <template #header>
              <h3 class="text-lg font-semibold">部门分布</h3>
            </template>
            <div class="space-y-4">
              <div v-for="dept in departments" :key="dept.id" class="flex items-center justify-between">
                <div class="flex items-center">
                  <UIcon name="i-lucide-building" class="size-4 text-gray-400 dark:text-gray-500 mr-2" />
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ dept.name }}</span>
                </div>
                <UChip :color="'primary'" variant="outline">{{ dept.employee_count }}人</UChip>
              </div>
            </div>
          </UCard>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
