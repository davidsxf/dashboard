<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useEmployees } from '~/composables/useEmployees';

const { 
  employees, 
  loading, 
  error, 
  currentPage, 
  pageSize, 
  total, 
  totalPages, 
  hasNextPage, 
  hasPrevPage, 
  fetchEmployees, 
  goToPage, 
  changePageSize 
} = useEmployees();

const searchQuery = ref('');

// 初始化加载员工数据
onMounted(() => {
  fetchEmployees();
});

// 搜索员工
const handleSearch = () => {
  fetchEmployees({ name: searchQuery.value });
};

// 重置搜索
const resetSearch = () => {
  searchQuery.value = '';
  fetchEmployees();
};
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar title="员工管理">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
        
        <template #right>
          <div class="flex space-x-4">
            <button 
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              添加员工
            </button>
            <button 
              class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              导出数据
            </button>
          </div>
        </template>
      </UDashboardNavbar>
    </template>
    
    <template #body>
      <div class="mb-6">
        <p class="text-sm text-gray-600 dark:text-gray-400">管理所有员工信息</p>
      </div>
      
      <!-- 搜索栏 -->
      <div class="mb-6">
        <div class="flex space-x-4">
          <div class="flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索员工姓名..."
              class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>
          <div class="flex space-x-2">
            <button 
              @click="handleSearch"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              搜索
            </button>
            <button 
              @click="resetSearch"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 dark:bg-gray-700 dark:text-gray-300"
            >
              重置
            </button>
          </div>
        </div>
      </div>
      
      <!-- 错误提示 -->
      <div v-if="error" class="mb-6 p-4 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-md">
        {{ error }}
      </div>
      
      <!-- 员工列表 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                员工编号
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                姓名
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                部门
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                职位
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                手机
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                状态
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="employee in employees" :key="employee.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ employee.employee_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ employee.name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ employee.department_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ employee.current_position || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ employee.mobile_phone || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="[
                  'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                  employee.is_active 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' 
                    : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                ]">
                  {{ employee.is_active ? '在职' : '离职' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-2">
                  <button class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                    查看
                  </button>
                  <button class="text-yellow-600 hover:text-yellow-900 dark:text-yellow-400 dark:hover:text-yellow-300">
                    编辑
                  </button>
                  <button class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300">
                    删除
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="p-4 text-center text-gray-600 dark:text-gray-400">
          加载中...
        </div>
        
        <!-- 空状态 -->
        <div v-else-if="employees.length === 0" class="p-8 text-center text-gray-600 dark:text-gray-400">
          没有找到员工数据
        </div>
      </div>
      
      <!-- 分页 -->
      <div v-if="total > 0" class="mt-6 flex justify-between items-center">
        <div class="text-sm text-gray-600 dark:text-gray-400">
          显示 {{ (currentPage - 1) * pageSize + 1 }} 到 {{ Math.min(currentPage * pageSize, total) }} 条，共 {{ total }} 条记录
        </div>
        <div class="flex items-center space-x-2">
          <select 
            v-model="pageSize" 
            @change="changePageSize(parseInt(pageSize))"
            class="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          >
            <option value="10">10条/页</option>
            <option value="20">20条/页</option>
            <option value="50">50条/页</option>
            <option value="100">100条/页</option>
          </select>
          <div class="flex items-center space-x-1">
            <button 
              @click="goToPage(currentPage - 1)"
              :disabled="!hasPrevPage"
              class="px-3 py-1 border border-gray-300 rounded-md text-sm hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-600 dark:text-white"
            >
              上一页
            </button>
            <span class="px-3 py-1 text-sm text-gray-600 dark:text-gray-400">
              {{ currentPage }} / {{ totalPages }}
            </span>
            <button 
              @click="goToPage(currentPage + 1)"
              :disabled="!hasNextPage"
              class="px-3 py-1 border border-gray-300 rounded-md text-sm hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-600 dark:text-white"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
