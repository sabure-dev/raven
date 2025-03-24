from api.v1.users import router as router_users
from api.v1.auth import router as router_auth
from api.v1.sneaker_model import router as router_sneaker_model

all_routers = [router_users, router_auth, router_sneaker_model]
