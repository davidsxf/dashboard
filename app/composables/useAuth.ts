import { ref } from 'vue';
import { useCookie } from '#app';
import type { LoginRequest, TokenResponse } from '~/types/hr';

export const useAuth = () => {
  const isAuthenticated = ref(false);
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  
  // 使用Cookie存储令牌
  const accessTokenCookie = useCookie('access_token', { 
    maxAge: 60 * 60, // 1小时
    secure: process.env.NODE_ENV === 'production',
    httpOnly: false // 允许客户端访问
  });
  
  const refreshTokenCookie = useCookie('refresh_token', { 
    maxAge: 24 * 60 * 60, // 24小时
    secure: process.env.NODE_ENV === 'production',
    httpOnly: false // 允许客户端访问
  });

  // 从Cookie加载令牌
  const loadTokens = () => {
    const savedAccessToken = accessTokenCookie.value;
    const savedRefreshToken = refreshTokenCookie.value;
    
    if (savedAccessToken && savedRefreshToken) {
      accessToken.value = savedAccessToken;
      refreshToken.value = savedRefreshToken;
      isAuthenticated.value = true;
    }
  };

  // 保存令牌到Cookie
  const saveTokens = (tokens: TokenResponse) => {
    accessTokenCookie.value = tokens.access_token;
    refreshTokenCookie.value = tokens.refresh_token;
    accessToken.value = tokens.access_token;
    refreshToken.value = tokens.refresh_token;
    isAuthenticated.value = true;
  };

  // 清除令牌
  const clearTokens = () => {
    accessTokenCookie.value = null;
    refreshTokenCookie.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    isAuthenticated.value = false;
  };

  // 登录
  const login = async (credentials: LoginRequest) => {
    try {
      const response = await $fetch<TokenResponse>('/api/auth/login', {
        method: 'POST',
        body: credentials
      });
      
      saveTokens(response);
      return response;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  // 登出
  const logout = async () => {
    try {
      await $fetch('/api/auth/logout', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      clearTokens();
    }
  };

  // 刷新令牌
  const refresh = async () => {
    try {
      const response = await $fetch<TokenResponse>('/api/auth/refresh', {
        method: 'POST',
        body: { refresh_token: refreshToken.value }
      });
      
      saveTokens(response);
      return response;
    } catch (error) {
      console.error('Token refresh failed:', error);
      clearTokens();
      throw error;
    }
  };

  // 初始化时加载令牌
  loadTokens();

  return {
    isAuthenticated,
    accessToken,
    refreshToken,
    login,
    logout,
    refresh
  };
};
