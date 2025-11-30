from django.http import JsonResponse
from django.conf import settings
from jose import jwt, JWTError
from django.contrib.auth.models import User


def jwt_auth_middleware(get_response):
    """JWT认证中间件"""
    def middleware(request):
        # 跳过认证的路径
        if request.path.startswith('/api/auth/'):
            return get_response(request)
        
        # 获取Authorization头
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return JsonResponse({'detail': '未提供认证令牌'}, status=401)
        
        try:
            # 解析令牌
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return JsonResponse({'detail': '无效的令牌类型'}, status=401)
            
            # 解码令牌
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            if payload.get('type') != 'access':
                return JsonResponse({'detail': '无效的令牌类型'}, status=401)
            
            # 获取用户
            user_id = payload.get('user_id')
            if not user_id:
                return JsonResponse({'detail': '无效的令牌'}, status=401)
            
            user = User.objects.get(id=user_id)
            request.user = user
            
        except ValueError:
            return JsonResponse({'detail': '无效的认证头格式'}, status=401)
        except JWTError:
            return JsonResponse({'detail': '无效的令牌'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'detail': '用户不存在'}, status=401)
        
        return get_response(request)
    
    return middleware
