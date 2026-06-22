import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from config import limiter
from routers import listings, auth, users, admin, reviews, favorites

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(listings.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(reviews.router)
app.include_router(favorites.router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)