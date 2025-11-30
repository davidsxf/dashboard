<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import { useRouter } from 'vue-router'
import { useAuth } from '~/composables/useAuth'

const route = useRoute()
const toast = useToast()
const router = useRouter()
const { isAuthenticated, logout } = useAuth()

const open = ref(false)

// 导航菜单
const links = [[{
  label: '首页',
  icon: 'i-lucide-house',
  to: '/',
  onSelect: () => {
    open.value = false
  }
}, {
  label: '员工管理',
  icon: 'i-lucide-users',
  to: '/employees',
  onSelect: () => {
    open.value = false
  }
}, {
  label: '部门管理',
  icon: 'i-lucide-building',
  to: '/departments',
  onSelect: () => {
    open.value = false
  }
}, {
  label: '科研团队',
  icon: 'i-lucide-users-round',
  to: '/teams',
  onSelect: () => {
    open.value = false
  }
}, {
  label: '系统设置',
  to: '/settings',
  icon: 'i-lucide-settings',
  defaultOpen: true,
  type: 'trigger',
  children: [{
    label: '用户管理',
    to: '/settings/users',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: '角色权限',
    to: '/settings/roles',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: '系统配置',
    to: '/settings',
    exact: true,
    onSelect: () => {
      open.value = false
    }
  }]
}], [{
  label: '退出登录',
  icon: 'i-lucide-log-out',
  onClick: async () => {
    await logout()
    router.push('/login')
  }
}]] satisfies NavigationMenuItem[][]

const groups = computed(() => [{
  id: 'links',
  label: '导航',
  items: links.flat()
}])

// 检查登录状态
onMounted(async () => {
  // 除了登录页面，其他页面需要登录
  if (!isAuthenticated.value && route.path !== '/login') {
    router.push('/login')
  }
})
</script>

<template>
  <UDashboardGroup unit="rem">
    <UDashboardSidebar
      id="default"
      v-model:open="open"
      collapsible
      resizable
      class="bg-elevated/25"
      :ui="{ footer: 'lg:border-t lg:border-default' }"
    >
      <template #header="{ collapsed }">
        <TeamsMenu :collapsed="collapsed" />
      </template>

      <template #default="{ collapsed }">
        <UDashboardSearchButton :collapsed="collapsed" class="bg-transparent ring-default" />

        <UNavigationMenu
          :collapsed="collapsed"
          :items="links[0]"
          orientation="vertical"
          tooltip
          popover
        />

        <UNavigationMenu
          :collapsed="collapsed"
          :items="links[1]"
          orientation="vertical"
          tooltip
          class="mt-auto"
        />
      </template>

      <template #footer="{ collapsed }">
        <UserMenu :collapsed="collapsed" />
      </template>
    </UDashboardSidebar>

    <UDashboardSearch :groups="groups" />

    <slot />

    <NotificationsSlideover />
  </UDashboardGroup>
</template>
