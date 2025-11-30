import { ref, computed } from 'vue';
import type { Employee, PaginationQuery } from '~/types/hr';
import { useAuth } from './useAuth';

export const useEmployees = () => {
  const { accessToken, refresh } = useAuth();
  const employees = ref<Employee[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const pageSize = ref(10);
  const total = ref(0);

  // 获取员工列表
  const fetchEmployees = async (filters: Record<string, any> = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const query = {
        page: currentPage.value,
        page_size: pageSize.value,
        ...filters
      };
      
      const response = await $fetch<Employee[]>('/api/employees/', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        query
      });
      
      employees.value = response;
      // 假设API返回的响应头中包含total计数，这里简化处理
      total.value = response.length;
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch employees';
      
      // 尝试刷新令牌并重试
      if (err.status === 401) {
        await refresh();
        return fetchEmployees(filters);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 获取单个员工
  const fetchEmployee = async (id: number) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<Employee>(`/api/employees/${id}`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      });
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch employee';
      
      if (err.status === 401) {
        await refresh();
        return fetchEmployee(id);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 创建员工
  const createEmployee = async (employeeData: Partial<Employee>) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<Employee>('/api/employees/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        body: employeeData
      });
      
      employees.value.push(response);
      total.value++;
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to create employee';
      
      if (err.status === 401) {
        await refresh();
        return createEmployee(employeeData);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 更新员工
  const updateEmployee = async (id: number, employeeData: Partial<Employee>) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<Employee>(`/api/employees/${id}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        body: employeeData
      });
      
      // 更新本地列表
      const index = employees.value.findIndex(emp => emp.id === id);
      if (index !== -1) {
        employees.value[index] = response;
      }
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to update employee';
      
      if (err.status === 401) {
        await refresh();
        return updateEmployee(id, employeeData);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 删除员工
  const deleteEmployee = async (id: number) => {
    loading.value = true;
    error.value = null;
    
    try {
      await $fetch(`/api/employees/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      });
      
      // 从本地列表中移除
      employees.value = employees.value.filter(emp => emp.id !== id);
      total.value--;
      
      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to delete employee';
      
      if (err.status === 401) {
        await refresh();
        return deleteEmployee(id);
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
      fetchEmployees();
    }
  };

  // 切换页大小
  const changePageSize = (size: number) => {
    pageSize.value = size;
    currentPage.value = 1;
    fetchEmployees();
  };

  return {
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
    fetchEmployee,
    createEmployee,
    updateEmployee,
    deleteEmployee,
    goToPage,
    changePageSize
  };
};
