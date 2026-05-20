from fastapi import FastAPI
from app.api.routes.user import router as user_router



# Создаем само приложение FastAPI
app = FastAPI(title="Bookly API")

# Подключаем наш роутер пользователей к общему приложению
# Все маршруты из файла user.py теперь будут доступны по адресу /api/v1/users/...
app.include_router(user_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"status": "working", "message": "GOIDAAAAAAA!"}