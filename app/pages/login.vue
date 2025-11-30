<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import type { LoginRequest } from '~/types/hr';
import { useAuth } from '~/composables/useAuth';

const router = useRouter();
const { login, isAuthenticated } = useAuth();
const loading = ref(false);
const error = ref<string | null>(null);

const form = ref<LoginRequest>({
  username: '',
  password: ''
});

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    await login(form.value);
    router.push('/');
  } catch (err: any) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码';
  } finally {
    loading.value = false;
  }
};

// 如果已经认证，跳转到首页
if (isAuthenticated.value) {
  router.push('/');
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
    <div class="w-full max-w-md p-8 space-y-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">人事管理系统</h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">请登录您的账户</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            placeholder="请输入用户名"
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            placeholder="请输入密码"
          />
        </div>
        
        <div v-if="error" class="p-3 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-md">
          {{ error }}
        </div>
        
        <div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="animate-spin mr-2">⏳</span>
            登录
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
