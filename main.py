from fastapi import FastAPI

from controllers.fundamentals import router as fundamentals_router


app = FastAPI(title="FastAPI Fundamentals - In-Memory CRUD")
app.include_router(fundamentals_router)
