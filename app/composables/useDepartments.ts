import { ref, computed } from 'vue';
import type { Department, DepartmentTreeNode, PaginationQuery } from '~/types/hr';
import { useAuth } from './useAuth';

export const useDepartments = () => {
  const { accessToken, refresh } = useAuth();
  const departments = ref<Department[]>([]);
  const departmentTree = ref<DepartmentTreeNode[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const pageSize = ref(10);
  const total = ref(0);

  // 获取部门列表
  const fetchDepartments = async (filters: Record<string, any> = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const query = {
        page: currentPage.value,
        page_size: pageSize.value,
        ...filters
      };
      
      const response = await $fetch<Department[]>('/api/departments/', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        query
      });
      
      departments.value = response;
      total.value = response.length;
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch departments';
      
      // 尝试刷新令牌并重试
      if (err.status === 401) {
        await refresh();
        return fetchDepartments(filters);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 获取部门树
  const fetchDepartmentTree = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<DepartmentTreeNode[]>('/api/departments/tree', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      });
      
      departmentTree.value = response;
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch department tree';
      
      if (err.status === 401) {
        await refresh();
        return fetchDepartmentTree();
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 获取单个部门
  const fetchDepartment = async (id: number) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<Department>(`/api/departments/${id}`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      });
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch department';
      
      if (err.status === 401) {
        await refresh();
        return fetchDepartment(id);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 创建部门
  const createDepartment = async (departmentData: Partial<Department>) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<Department>('/api/departments/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        body: departmentData
      });
      
      departments.value.push(response);
      total.value++;
      
      // 重新获取部门树
      await fetchDepartmentTree();
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to create department';
      
      if (err.status === 401) {
        await refresh();
        return createDepartment(departmentData);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 更新部门
  const updateDepartment = async (id: number, departmentData: Partial<Department>) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<Department>(`/api/departments/${id}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        body: departmentData
      });
      
      // 更新本地列表
      const index = departments.value.findIndex(dept => dept.id === id);
      if (index !== -1) {
        departments.value[index] = response;
      }
      
      // 重新获取部门树
      await fetchDepartmentTree();
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to update department';
      
      if (err.status === 401) {
        await refresh();
        return updateDepartment(id, departmentData);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 删除部门
  const deleteDepartment = async (id: number) => {
    loading.value = true;
    error.value = null;
    
    try {
      await $fetch(`/api/departments/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      });
      
      // 从本地列表中移除
      departments.value = departments.value.filter(dept => dept.id !== id);
      total.value--;
      
      // 重新获取部门树
      await fetchDepartmentTree();
      
      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to delete department';
      
      if (err.status === 401) {
        await refresh();
        return deleteDepartment(id);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 分页相关计算属性
  const totalPages = computed(() => Math.ceil(total.value / pageSize.value));
  const hasNextPage = computed(() => currentPage.value < totalPages.value);
  const hasPrevPage = computed(() => currentPage.value > 1);

  // 切换页码
  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page;
      fetchDepartments();
    }
  };

  // 切换页大小
  const changePageSize = (size: number) => {
    pageSize.value = size;
    currentPage.value = 1;
    fetchDepartments();
  };

  return {
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
    fetchDepartment,
    createDepartment,
    updateDepartment,
    deleteDepartment,
    goToPage,
    changePageSize
  };
};
