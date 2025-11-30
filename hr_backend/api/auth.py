from ninja import Router, Form
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import BaseModel
from django.http import JsonResponse

router = Router()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str


def create_access_token(user_id: int) -> str:
    """创建访问令牌"""
    expire = datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TOKEN_LIFETIME)
    payload = {
        "user_id": user_id,
        "exp": expire,
        "type": "access"
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    """创建刷新令牌"""
    expire = datetime.utcnow() + timedelta(seconds=settings.JWT_REFRESH_TOKEN_LIFETIME)
    payload = {
        "user_id": user_id,
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """解码令牌"""
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


@router.post("/login", response=TokenResponse)
def login(request, data: LoginRequest):
    """用户登录"""
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return JsonResponse({"detail": "用户名或密码错误"}, status=401)
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response=TokenResponse)
def refresh_token(request, data: RefreshTokenRequest):
    """刷新访问令牌"""
    payload = decode_token(data.refresh_token)
    if not payload or payload["type"] != "refresh":
        return JsonResponse({"detail": "无效的刷新令牌"}, status=401)
    
    access_token = create_access_token(payload["user_id"])
    refresh_token = create_refresh_token(payload["user_id"])
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(request):
    """用户登出"""
    # JWT是无状态的，登出只需客户端删除令牌即可
    return {"detail": "登出成功"}
