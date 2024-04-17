from fastapi import FastAPI

from api.routers import all_routers

app = FastAPI(
    title="FSP Service",
    description="FSP Service — это FastAPI приложение, которое помогает пользователю находить кратчайшее расстояние между городами.",
)


for router in all_routers:
    app.include_router(router)
