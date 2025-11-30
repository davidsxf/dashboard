from ninja import NinjaAPI
from django.conf import settings

api = NinjaAPI(
    title="人事系统API",
    description="人事信息管理系统API",
    version="1.0.0",
    urls_namespace="api"
)

from . import auth, employees, departments, teams

api.add_router("/auth/", auth.router)
api.add_router("/employees/", employees.router)
api.add_router("/departments/", departments.router)
api.add_router("/teams/", teams.router)
