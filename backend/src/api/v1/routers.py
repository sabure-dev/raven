from api.v1.users import router as router_users
from api.v1.auth import router as router_auth
from api.v1.sneaker_model import router as router_sneaker_model
from api.v1.sneaker_variant import router as router_sneaker_variant

all_routers = [router_users, router_auth, router_sneaker_model, router_sneaker_variant]
