import uvicorn
from fastapi import FastAPI

from routers import listings, auth, users, admin, reviews, favorites

app = FastAPI()

app.include_router(listings.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(reviews.router)
app.include_router(favorites.router)

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)