import uvicorn
from fastapi import FastAPI

from database import engine
from models import Base
from routers import listings, auth, users, admin, reviews

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(listings.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(reviews.router)

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)