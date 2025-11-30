import { ref, computed } from 'vue';
import type { ResearchTeam, PaginationQuery } from '~/types/hr';
import { useAuth } from './useAuth';

export const useTeams = () => {
  const { accessToken, refresh } = useAuth();
  const teams = ref<ResearchTeam[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const pageSize = ref(10);
  const total = ref(0);

  // 获取科研团队列表
  const fetchTeams = async (filters: Record<string, any> = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const query = {
        page: currentPage.value,
        page_size: pageSize.value,
        ...filters
      };
      
      const response = await $fetch<ResearchTeam[]>('/api/teams/', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        query
      });
      
      teams.value = response;
      total.value = response.length;
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch teams';
      
      // 尝试刷新令牌并重试
      if (err.status === 401) {
        await refresh();
        return fetchTeams(filters);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 获取单个科研团队
  const fetchTeam = async (id: number) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<ResearchTeam>(`/api/teams/${id}`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      });
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch team';
      
      if (err.status === 401) {
        await refresh();
        return fetchTeam(id);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 创建科研团队
  const createTeam = async (teamData: Partial<ResearchTeam>) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<ResearchTeam>('/api/teams/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        body: teamData
      });
      
      teams.value.push(response);
      total.value++;
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to create team';
      
      if (err.status === 401) {
        await refresh();
        return createTeam(teamData);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 更新科研团队
  const updateTeam = async (id: number, teamData: Partial<ResearchTeam>) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await $fetch<ResearchTeam>(`/api/teams/${id}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        },
        body: teamData
      });
      
      // 更新本地列表
      const index = teams.value.findIndex(team => team.id === id);
      if (index !== -1) {
        teams.value[index] = response;
      }
      
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to update team';
      
      if (err.status === 401) {
        await refresh();
        return updateTeam(id, teamData);
      }
      
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // 删除科研团队
  const deleteTeam = async (id: number) => {
    loading.value = true;
    error.value = null;
    
    try {
      await $fetch(`/api/teams/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      });
      
      // 从本地列表中移除
      teams.value = teams.value.filter(team => team.id !== id);
      total.value--;
      
      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to delete team';
      
      if (err.status === 401) {
        await refresh();
        return deleteTeam(id);
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
      fetchTeams();
    }
  };

  // 切换页大小
  const changePageSize = (size: number) => {
    pageSize.value = size;
    currentPage.value = 1;
    fetchTeams();
  };

  return {
    teams,
    loading,
    error,
    currentPage,
    pageSize,
    total,
    totalPages,
    hasNextPage,
    hasPrevPage,
    fetchTeams,
    fetchTeam,
    createTeam,
    updateTeam,
    deleteTeam,
    goToPage,
    changePageSize
  };
};
