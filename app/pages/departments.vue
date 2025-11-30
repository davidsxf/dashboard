<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useDepartments } from '~/composables/useDepartments';

const { 
  departments, 
  departmentTree, 
  loading, 
  error, 
  currentPage, 
  pageSize, 
  total, 
  totalPages, 
  hasNextPage, 
  hasPrevPage, 
  fetchDepartments, 
  fetchDepartmentTree,
  goToPage, 
  changePageSize 
} = useDepartments();

const searchQuery = ref('');
const showTree = ref(false);

// 初始化加载部门数据
onMounted(() => {
  fetchDepartments();
  fetchDepartmentTree();
});

// 搜索部门
const handleSearch = () => {
  fetchDepartments({ name: searchQuery.value });
};

// 重置搜索
const resetSearch = () => {
  searchQuery.value = '';
  fetchDepartments();
};

// 切换显示方式
const toggleView = () => {
  showTree.value = !showTree.value;
};
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar title="部门管理">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
        
        <template #right>
          <div class="flex space-x-4">
            <button 
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              添加部门
            </button>
            <button 
              @click="toggleView"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 dark:bg-gray-700 dark:text-gray-300"
            >
              {{ showTree ? '列表视图' : '树状视图' }}
            </button>
          </div>
        </template>
      </UDashboardNavbar>
    </template>
    
    <template #body>
      <div class="mb-6">
        <p class="text-sm text-gray-600 dark:text-gray-400">管理所有部门信息</p>
      </div>
      
      <!-- 搜索栏 -->
      <div class="mb-6">
        <div class="flex space-x-4">
          <div class="flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索部门名称..."
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
      
      <!-- 树状视图 -->
      <div v-if="showTree" class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div v-if="loading" class="p-4 text-center text-gray-600 dark:text-gray-400">
          加载中...
        </div>
        <div v-else-if="departmentTree.length === 0" class="p-8 text-center text-gray-600 dark:text-gray-400">
          没有找到部门数据
        </div>
        <div v-else class="p-4">
          <!-- 简单的树状视图实现 -->
          <div class="space-y-2">
            <template v-for="dept in departmentTree" :key="dept.id">
              <div class="flex items-center space-x-2 p-2 bg-gray-50 dark:bg-gray-700 rounded-md">
                <span class="text-gray-900 dark:text-white font-medium">{{ dept.name }}</span>
                <span class="text-xs text-gray-500 dark:text-gray-400">({{ dept.employee_count }}人)</span>
                <div class="ml-auto flex space-x-2">
                  <button class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 text-sm">
                    查看
                  </button>
                  <button class="text-yellow-600 hover:text-yellow-900 dark:text-yellow-400 dark:hover:text-yellow-300 text-sm">
                    编辑
                  </button>
                </div>
              </div>
              <!-- 子部门 -->
              <div v-if="dept.children.length > 0" class="ml-6 space-y-2">
                <template v-for="child in dept.children" :key="child.id">
                  <div class="flex items-center space-x-2 p-2 bg-gray-50 dark:bg-gray-700 rounded-md">
                    <span class="text-gray-900 dark:text-white">{{ child.name }}</span>
                    <span class="text-xs text-gray-500 dark:text-gray-400">({{ child.employee_count }}人)</span>
                    <div class="ml-auto flex space-x-2">
                      <button class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 text-sm">
                        查看
                      </button>
                      <button class="text-yellow-600 hover:text-yellow-900 dark:text-yellow-400 dark:hover:text-yellow-300 text-sm">
                        编辑
                      </button>
                    </div>
                  </div>
                </template>
              </div>
            </template>
          </div>
        </div>
      </div>
      
      <!-- 列表视图 -->
      <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                部门名称
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                上级部门
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                部门负责人
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                员工数量
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="dept in departments" :key="dept.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ dept.name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ dept.parent_department_name || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ dept.leader_name || '-' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ dept.employee_count }}
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
        <div v-else-if="departments.length === 0" class="p-8 text-center text-gray-600 dark:text-gray-400">
          没有找到部门数据
        </div>
      </div>
      
      <!-- 分页 -->
      <div v-if="!showTree && total > 0" class="mt-6 flex justify-between items-center">
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
