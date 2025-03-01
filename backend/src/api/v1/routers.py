from api.v1.users import router as router_users
from api.v1.auth import router as router_auth

all_routers = [
    router_users,
    router_auth
]
